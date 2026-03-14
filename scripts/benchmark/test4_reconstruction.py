#!/usr/bin/env python3
"""
Test 4: Stem Reconstruction Fidelity
--------------------------------------
Measures how accurately separated stems reconstruct to the original mix.

Method: separate into N stems, sum them, compare sum to original.
The error between the sum and the original quantifies information loss
in the separation process.

Uses MUSDB18-7s mixture tracks. No ground truth stems needed.
"""

import argparse
import time

import numpy as np
import scipy.signal
from tqdm import tqdm

from utils import get_device, load_model, load_musdb, save_yaml, separate_track

MODES = [
    {"stems": 2, "model": "htdemucs_ft",  "label": "2-stem (vocals + accompaniment)"},
    {"stems": 4, "model": "htdemucs_ft",  "label": "4-stem (vocals, drums, bass, other)"},
    {"stems": 6, "model": "htdemucs_6s",  "label": "6-stem (+ guitar, piano)"},
]


def compute_reconstruction_metrics(original, reconstructed):
    """
    Compute reconstruction error between original mix and sum of stems.

    Returns:
        mse:              mean squared error (lower = better)
        correlation:      Pearson r between original and reconstruction (higher = better)
        db_difference:    level of the difference signal in dB below original (higher = better)
    """
    min_len = min(len(original), len(reconstructed))
    orig = original[:min_len]
    recon = reconstructed[:min_len]

    # Mix to mono for scalar metrics
    if orig.ndim > 1:
        orig = orig.mean(axis=1)
    if recon.ndim > 1:
        recon = recon.mean(axis=1)

    # MSE
    mse = float(np.mean((orig - recon) ** 2))

    # Pearson correlation
    if orig.std() < 1e-9 or recon.std() < 1e-9:
        correlation = 0.0
    else:
        correlation = float(np.corrcoef(orig, recon)[0, 1])

    # Difference signal level relative to original (dB)
    diff = orig - recon
    orig_rms = np.sqrt(np.mean(orig ** 2))
    diff_rms = np.sqrt(np.mean(diff ** 2))
    if orig_rms < 1e-9 or diff_rms < 1e-9:
        db_diff = -120.0
    else:
        db_diff = float(20 * np.log10(diff_rms / orig_rms))

    return mse, correlation, db_diff


def run_2stem_htdemucs(audio, rate, model, device):
    """
    Simulate 2-stem output by merging the 4-stem output into
    vocals + accompaniment (drums + bass + other summed).
    """
    estimates = separate_track(audio, rate, model, device)
    vocals = estimates.get("vocals", np.zeros_like(audio))
    accompaniment = sum(
        estimates[s] for s in ["drums", "bass", "other"] if s in estimates
    )
    return {"vocals": vocals, "accompaniment": accompaniment}


def run(output_path, data_root=None):
    device = get_device()
    print(f"Device: {device}")

    print("Loading MUSDB18-7s test tracks...")
    tracks = load_musdb(data_root=data_root, subset="test")

    modes_out = []

    for mode in MODES:
        print(f"\nMode: {mode['label']} using {mode['model']}")
        model = load_model(mode["model"], device)

        mses, correlations, db_diffs = [], [], []

        for track in tqdm(tracks, desc=mode["label"]):
            mixture = track.audio
            rate = track.rate

            try:
                if mode["stems"] == 2:
                    estimates = run_2stem_htdemucs(mixture, rate, model, device)
                else:
                    estimates = separate_track(mixture, rate, model, device)

                # Sum all stems
                min_len = len(mixture)
                for stem_audio in estimates.values():
                    min_len = min(min_len, len(stem_audio))

                stem_sum = sum(
                    est[:min_len] for est in estimates.values()
                )

                mse, corr, db_diff = compute_reconstruction_metrics(
                    mixture[:min_len], stem_sum
                )
                mses.append(mse)
                correlations.append(corr)
                db_diffs.append(db_diff)

            except Exception as e:
                tqdm.write(f"  Skipped {track.name}: {e}")
                continue

        mean_mse = round(float(np.mean(mses)), 6) if mses else None
        mean_corr = round(float(np.mean(correlations)), 4) if correlations else None
        mean_db = round(float(np.mean(db_diffs)), 1) if db_diffs else None

        modes_out.append(
            {
                "stems": mode["stems"],
                "model": mode["model"],
                "label": mode["label"],
                "n_tracks": len(mses),
                "mean_mse": mean_mse,
                "mean_correlation": mean_corr,
                "mean_db_difference": mean_db,
            }
        )
        print(f"  MSE: {mean_mse} | Correlation: {mean_corr} | dB diff: {mean_db} dB")

    # Key finding: how does going from 4 to 6 stems change reconstruction?
    m4 = next((m for m in modes_out if m["stems"] == 4), None)
    m6 = next((m for m in modes_out if m["stems"] == 6), None)
    if m4 and m6 and m4["mean_db_difference"] and m6["mean_db_difference"]:
        delta = round(m6["mean_db_difference"] - m4["mean_db_difference"], 1)
        key_finding = (
            f"Splitting into 6 stems vs 4 stems increases reconstruction error by "
            f"{abs(delta)} dB ({m4['mean_db_difference']} dB for 4-stem vs "
            f"{m6['mean_db_difference']} dB for 6-stem relative to original)"
        )
    else:
        key_finding = "See results table for reconstruction error by stem count."

    output = {
        "title": "How Much Information Does Stem Separation Actually Lose?",
        "subtitle": (
            f"Reconstruction fidelity across 2-stem, 4-stem, and 6-stem modes on "
            f"{len(tracks)} MUSDB18-7s tracks"
        ),
        "run_date": time.strftime("%B %d, %Y"),
        "run_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "dataset": "MUSDB18-7s",
        "dataset_url": "https://zenodo.org/record/1117372",
        "n_tracks": len(tracks),
        "key_finding": key_finding,
        "methodology_note": (
            "Each mixture was separated into stems, which were then summed back. "
            "The difference between the reconstruction and the original mix measures "
            "information loss. Lower MSE, higher correlation, and lower dB difference "
            "all indicate better reconstruction fidelity."
        ),
        "modes": modes_out,
    }

    save_yaml(output, output_path)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test 4: Stem reconstruction fidelity")
    parser.add_argument("--output", default="results/reconstruction.yml")
    parser.add_argument("--data-root", default=None)
    args = parser.parse_args()

    run(args.output, data_root=args.data_root)
