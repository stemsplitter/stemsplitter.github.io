#!/usr/bin/env python3
"""
Test 2: HTDemucs Model Variant Comparison
------------------------------------------
Compares separation quality (SDR) and processing speed across all four
HTDemucs model variants on the full MUSDB18-7s test set.

Also saves per-track results as JSON for use by test3 and test5.
"""

import argparse
import json
import os
import time

import numpy as np
from tqdm import tqdm

from utils import compute_sdr, get_device, load_model, load_musdb, median_sdr, save_yaml, separate_track

MODELS = ["htdemucs", "htdemucs_ft", "htdemucs_6s", "hdemucs_mmi"]
MODEL_LABELS = {
    "htdemucs":    "HTDemucs (base)",
    "htdemucs_ft": "HTDemucs FT (fine-tuned)",
    "htdemucs_6s": "HTDemucs 6S (6-stem)",
    "hdemucs_mmi": "Hybrid Demucs MMI (extended data)",
}
STEMS = ["vocals", "drums", "bass", "other"]


def run(output_path, raw_output_path, data_root=None):
    device = get_device()
    print(f"Device: {device}")

    print("Loading MUSDB18-7s test tracks...")
    tracks = load_musdb(data_root=data_root, subset="test")

    # raw_results[model_name] = list of per-track dicts
    raw_results = {}
    models_out = []

    for model_name in MODELS:
        print(f"\n{'='*50}")
        print(f"Model: {model_name}")
        model = load_model(model_name, device)

        track_results = []

        for track in tqdm(tracks, desc=model_name):
            t_start = time.time()
            refs = {s: track.targets[s].audio for s in STEMS if s in track.targets}

            try:
                estimates = separate_track(track.audio, track.rate, model, device)
            except Exception as e:
                tqdm.write(f"  Skipped {track.name}: {e}")
                continue

            elapsed = time.time() - t_start

            sdr_per_stem = {}
            for stem in STEMS:
                if stem in refs and stem in estimates:
                    sdr = compute_sdr(refs[stem], estimates[stem])
                    sdr_per_stem[stem] = sdr

            # Try to get genre from track metadata
            genre = "Unknown"
            try:
                meta = getattr(track, "metadata", {})
                genre = meta.get("genre", getattr(track, "genre", "Unknown"))
            except Exception:
                pass

            track_results.append(
                {
                    "track": track.name,
                    "genre": genre,
                    "time_seconds": round(elapsed, 2),
                    "sdr": sdr_per_stem,
                }
            )

        raw_results[model_name] = track_results

        # Aggregate
        stem_lists = {s: [] for s in STEMS}
        times = []
        for tr in track_results:
            times.append(tr["time_seconds"])
            for stem in STEMS:
                v = tr["sdr"].get(stem)
                if v is not None:
                    stem_lists[stem].append(v)

        stem_medians = {s: median_sdr(stem_lists[s]) for s in STEMS}
        valid = [v for v in stem_medians.values() if v is not None]
        mean = round(float(np.mean(valid)), 2) if valid else None
        avg_time = round(float(np.mean(times)), 1) if times else None

        models_out.append(
            {
                "id": model_name,
                "label": MODEL_LABELS[model_name],
                "sdr_vocals": stem_medians["vocals"],
                "sdr_drums": stem_medians["drums"],
                "sdr_bass": stem_medians["bass"],
                "sdr_other": stem_medians["other"],
                "sdr_mean": mean,
                "avg_time_seconds": avg_time,
                "n_tracks": len(track_results),
            }
        )

        print(f"  Mean SDR: {mean} dB | Avg time: {avg_time}s/track")

    # Sort by mean SDR descending for display
    models_out_sorted = sorted(
        models_out, key=lambda x: x["sdr_mean"] or -999, reverse=True
    )
    best = models_out_sorted[0] if models_out_sorted else None

    output = {
        "title": "HTDemucs Model Variant Comparison",
        "subtitle": f"SDR and processing speed across 4 model variants on {len(tracks)} MUSDB18-7s test tracks",
        "run_date": time.strftime("%B %d, %Y"),
        "run_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "device": f"Apple M4 MPS" if device == "mps" else device.upper(),
        "dataset": "MUSDB18-7s",
        "dataset_url": "https://zenodo.org/record/1117372",
        "n_tracks": len(tracks),
        "stems": STEMS,
        "key_finding": (
            f"{best['label']} achieves the highest mean SDR at {best['sdr_mean']} dB"
            if best
            else "See results table."
        ),
        "models": models_out,
    }

    save_yaml(output, output_path)

    # Save raw per-track results for test3 and test5
    os.makedirs(os.path.dirname(os.path.abspath(raw_output_path)), exist_ok=True)
    with open(raw_output_path, "w") as f:
        json.dump(raw_results, f, indent=2)
    print(f"  Raw results saved: {raw_output_path}")

    return output, raw_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test 2: Model variant comparison")
    parser.add_argument("--output", default="results/model_comparison.yml")
    parser.add_argument("--raw-output", default="results/raw/test2_tracks.json")
    parser.add_argument("--data-root", default=None)
    args = parser.parse_args()

    run(args.output, args.raw_output, data_root=args.data_root)
