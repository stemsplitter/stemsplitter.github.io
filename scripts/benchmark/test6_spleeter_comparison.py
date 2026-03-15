#!/usr/bin/env python3
"""
Test 6: Spleeter 4-stem vs HTDemucs (base) Head-to-Head
---------------------------------------------------------
Runs both models on all 50 MUSDB18-7s test tracks.
Measures SDR per stem, mean SDR, and per-track processing time.

Spleeter runs on CPU (TensorFlow, no MPS support).
HTDemucs runs on MPS (PyTorch, Apple Silicon GPU).

Key research questions:
  1. How does SDR quality compare in 2026?
  2. How much faster is HTDemucs on Apple Silicon due to MPS?
"""

import argparse
import os
import sys
import time
import tempfile
import warnings

import numpy as np
import soundfile as sf
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Setup import paths -- allow running from scripts/benchmark/ directly
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from utils import compute_sdr, load_musdb, mean_sdr, median_sdr, save_yaml


STEMS_4 = ["vocals", "drums", "bass", "other"]
SPLEETER_STEM_MAP = {
    "vocals": "vocals",
    "accompaniment": None,  # not used
    "drums": "drums",
    "bass": "bass",
    "other": "other",
}


# ---------------------------------------------------------------------------
# Spleeter helpers
# ---------------------------------------------------------------------------

def load_spleeter():
    """Load Spleeter 4-stem separator (downloads model on first run)."""
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    warnings.filterwarnings("ignore")
    from spleeter.separator import Separator  # type: ignore
    sep = Separator("spleeter:4stems")
    print("  Spleeter 4-stem separator ready (TensorFlow CPU)")
    return sep


def separate_spleeter(separator, audio_np, rate=44100):
    """
    Separate a numpy (samples, 2) array using Spleeter.

    Returns dict: stem_name -> numpy (samples, 2)
    Raises on failure.
    """
    # Spleeter.separate() expects (samples, channels) float32 at its native rate
    audio32 = audio_np.astype(np.float32)
    # Convert to mono if single channel
    if audio32.ndim == 1:
        audio32 = np.stack([audio32, audio32], axis=1)
    elif audio32.shape[1] == 1:
        audio32 = np.repeat(audio32, 2, axis=1)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        out = separator.separate(audio32)

    # out is a dict: stem -> (samples, 2) float32
    return out


# ---------------------------------------------------------------------------
# HTDemucs helpers  (reusing utils.py functions)
# ---------------------------------------------------------------------------

def load_htdemucs(device):
    """Load HTDemucs base model."""
    import torch
    from demucs.pretrained import get_model

    model = get_model("htdemucs")
    model.eval()
    model = model.to(device)
    print(f"  HTDemucs (base) ready on {device}")
    return model


def separate_htdemucs(audio_np, rate, model, device):
    """Thin wrapper around utils.separate_track."""
    from utils import separate_track
    return separate_track(audio_np, rate, model, device)


# ---------------------------------------------------------------------------
# Main benchmark loop
# ---------------------------------------------------------------------------

def run(output_path, data_root=None):
    import torch

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"\n{'='*55}")
    print("Test 6: Spleeter vs HTDemucs Head-to-Head")
    print(f"{'='*55}")
    print(f"HTDemucs device: {device}")
    print("Spleeter device: CPU (TensorFlow -- no MPS support)")
    print()

    # Load dataset
    print("Loading MUSDB18-7s test tracks...")
    tracks = load_musdb(data_root=data_root, subset="test")

    # Load models
    print("\nLoading models...")
    print("  [1/2] Spleeter 4-stem...")
    separator = load_spleeter()
    print("  [2/2] HTDemucs base...")
    ht_model = load_htdemucs(device)

    # Per-track results
    spleeter_results = []
    htdemucs_results = []

    for track in tqdm(tracks, desc="Processing tracks"):
        audio = track.audio          # (samples, 2) float64
        rate  = track.rate           # 44100
        refs  = {s: track.targets[s].audio for s in STEMS_4 if s in track.targets}

        # --- Spleeter ---
        try:
            t0 = time.time()
            spl_out = separate_spleeter(separator, audio, rate)
            spl_time = time.time() - t0

            spl_sdr = {}
            for stem in STEMS_4:
                if stem in refs and stem in spl_out:
                    sdr = compute_sdr(refs[stem], spl_out[stem])
                    spl_sdr[stem] = sdr

            spleeter_results.append({
                "track": track.name,
                "time_seconds": round(spl_time, 2),
                "sdr": spl_sdr,
            })
        except Exception as e:
            tqdm.write(f"  Spleeter skipped {track.name}: {e}")

        # --- HTDemucs ---
        try:
            t0 = time.time()
            ht_out = separate_htdemucs(audio, rate, ht_model, device)
            ht_time = time.time() - t0

            ht_sdr = {}
            for stem in STEMS_4:
                if stem in refs and stem in ht_out:
                    sdr = compute_sdr(refs[stem], ht_out[stem])
                    ht_sdr[stem] = sdr

            htdemucs_results.append({
                "track": track.name,
                "time_seconds": round(ht_time, 2),
                "sdr": ht_sdr,
            })
        except Exception as e:
            tqdm.write(f"  HTDemucs skipped {track.name}: {e}")

    # ---------------------------------------------------------------------------
    # Aggregate
    # ---------------------------------------------------------------------------

    def aggregate(results):
        stem_vals = {s: [] for s in STEMS_4}
        times = []
        for r in results:
            times.append(r["time_seconds"])
            for s in STEMS_4:
                v = r["sdr"].get(s)
                if v is not None:
                    stem_vals[s].append(v)
        meds = {s: median_sdr(stem_vals[s]) for s in STEMS_4}
        valid = [v for v in meds.values() if v is not None]
        mean = round(float(np.mean(valid)), 2) if valid else None
        avg_t = round(float(np.mean(times)), 2) if times else None
        return meds, mean, avg_t, len(results)

    spl_meds, spl_mean, spl_time, spl_n = aggregate(spleeter_results)
    ht_meds,  ht_mean,  ht_time,  ht_n  = aggregate(htdemucs_results)

    # Speed-up ratio
    speedup = None
    if spl_time and ht_time and ht_time > 0:
        speedup = round(spl_time / ht_time, 1)

    # SDR advantage for each stem
    head_to_head = []
    for stem in STEMS_4:
        sm = spl_meds.get(stem)
        hm = ht_meds.get(stem)
        winner = None
        delta = None
        if sm is not None and hm is not None:
            delta = round(hm - sm, 2)
            winner = "htdemucs" if delta >= 0 else "spleeter"
        head_to_head.append({
            "stem": stem,
            "spleeter_sdr": sm,
            "htdemucs_sdr": hm,
            "delta_htdemucs_minus_spleeter": delta,
            "winner": winner,
        })

    # Build key finding
    if spl_mean is not None and ht_mean is not None:
        sdr_delta = round(ht_mean - spl_mean, 2)
        sign = "higher" if sdr_delta >= 0 else "lower"
        spd_str = f"{speedup}x faster" if speedup else "faster"
        key_finding = (
            f"HTDemucs (base) scores {abs(sdr_delta)} dB {sign} mean SDR than Spleeter 4-stem "
            f"({ht_mean} dB vs {spl_mean} dB) and runs {spd_str} on Apple M4 thanks to MPS acceleration."
        )
    else:
        key_finding = "See results table for SDR and speed comparison."

    output = {
        "title": "Spleeter vs HTDemucs: Quality and Speed on Apple M4",
        "subtitle": (
            f"Head-to-head comparison on {ht_n} MUSDB18-7s test tracks -- "
            "SDR quality and processing time"
        ),
        "run_date": time.strftime("%B %d, %Y"),
        "run_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "device_htdemucs": f"Apple M4 {device.upper()}",
        "device_spleeter": "Apple M4 CPU (TensorFlow)",
        "dataset": "MUSDB18-7s",
        "dataset_url": "https://zenodo.org/record/1117372",
        "n_tracks": ht_n,
        "stems": STEMS_4,
        "key_finding": key_finding,
        "speedup_ratio": speedup,
        "models": [
            {
                "id": "spleeter_4stems",
                "label": "Spleeter (4-stem)",
                "device": "CPU",
                "sdr_vocals": spl_meds["vocals"],
                "sdr_drums":  spl_meds["drums"],
                "sdr_bass":   spl_meds["bass"],
                "sdr_other":  spl_meds["other"],
                "sdr_mean":   spl_mean,
                "avg_time_seconds": spl_time,
                "n_tracks": spl_n,
            },
            {
                "id": "htdemucs",
                "label": "HTDemucs (base)",
                "device": f"MPS" if device == "mps" else device.upper(),
                "sdr_vocals": ht_meds["vocals"],
                "sdr_drums":  ht_meds["drums"],
                "sdr_bass":   ht_meds["bass"],
                "sdr_other":  ht_meds["other"],
                "sdr_mean":   ht_mean,
                "avg_time_seconds": ht_time,
                "n_tracks": ht_n,
            },
        ],
        "head_to_head": head_to_head,
    }

    save_yaml(output, output_path)

    print(f"\nSpleeter  | mean SDR: {spl_mean} dB | avg time: {spl_time}s")
    print(f"HTDemucs  | mean SDR: {ht_mean} dB | avg time: {ht_time}s")
    if speedup:
        print(f"Speed-up  | HTDemucs is {speedup}x faster on Apple M4 MPS vs Spleeter CPU")

    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test 6: Spleeter vs HTDemucs comparison")
    parser.add_argument("--output", default="results/spleeter_comparison.yml")
    parser.add_argument("--data-root", default=None)
    args = parser.parse_args()

    run(args.output, data_root=args.data_root)
