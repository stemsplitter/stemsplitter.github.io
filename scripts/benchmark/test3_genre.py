#!/usr/bin/env python3
"""
Test 3: Track Characteristic Performance
------------------------------------------
Groups tracks by audio characteristics (not just genre) and shows how
HTDemucs quality varies across track types.

Uses htdemucs_ft results from test2's raw JSON output.
Also categorises tracks by genre when metadata is available.
"""

import argparse
import json
import time

import numpy as np

from utils import median_sdr, save_yaml

STEMS = ["vocals", "drums", "bass", "other"]

# Genre groupings -- MUSDB18 genre metadata varies; we handle 'Unknown' gracefully
GENRE_MAP = {
    # Map raw genre strings to display labels
    "Singer/Songwriter": "Singer/Songwriter",
    "Rock": "Rock",
    "Pop": "Pop",
    "Electronic": "Electronic",
    "Rap": "Hip-Hop / Rap",
    "Hip-Hop": "Hip-Hop / Rap",
    "Jazz": "Jazz",
    "Classical": "Classical",
    "World": "World / Folk",
    "Folk": "World / Folk",
    "Metal": "Metal / Heavy",
    "Unknown": "Unknown / Other",
}


def categorise_by_vocal_energy(sdr_vocals_list, threshold_high=8.0, threshold_low=5.0):
    """Label tracks as 'clear vocals', 'present vocals', or 'sparse/instrumental'."""
    if not sdr_vocals_list:
        return "Unknown"
    median_v = np.median(sdr_vocals_list)
    if median_v >= threshold_high:
        return "High vocal clarity"
    elif median_v >= threshold_low:
        return "Moderate vocal clarity"
    return "Low vocal clarity / instrumental"


def run(raw_input_path, output_path):
    print(f"Reading raw test2 results from {raw_input_path}...")
    with open(raw_input_path) as f:
        raw = json.load(f)

    # Use htdemucs_ft as the reference model
    model_key = "htdemucs_ft" if "htdemucs_ft" in raw else list(raw.keys())[0]
    track_results = raw[model_key]
    print(f"  Using model: {model_key} ({len(track_results)} tracks)")

    # --- Genre grouping ---
    genre_sdrs = {}
    for tr in track_results:
        raw_genre = tr.get("genre", "Unknown") or "Unknown"
        label = GENRE_MAP.get(raw_genre, "Unknown / Other")
        if label not in genre_sdrs:
            genre_sdrs[label] = {s: [] for s in STEMS}
        for stem in STEMS:
            v = tr["sdr"].get(stem)
            if v is not None:
                genre_sdrs[label][stem].append(v)

    genres_out = []
    for label, stem_lists in sorted(genre_sdrs.items()):
        if label == "Unknown / Other":
            continue  # Save for last
        n = len(stem_lists["vocals"]) or len(stem_lists["drums"])
        if n < 2:
            continue  # Skip categories with too few tracks to be meaningful
        stem_meds = {s: median_sdr(stem_lists[s]) for s in STEMS}
        valid = [v for v in stem_meds.values() if v is not None]
        genres_out.append(
            {
                "label": label,
                "n_tracks": n,
                "sdr_vocals": stem_meds["vocals"],
                "sdr_drums": stem_meds["drums"],
                "sdr_bass": stem_meds["bass"],
                "sdr_other": stem_meds["other"],
                "sdr_mean": round(float(np.mean(valid)), 2) if valid else None,
            }
        )

    # Append Unknown at end
    if "Unknown / Other" in genre_sdrs and genre_sdrs["Unknown / Other"]["vocals"]:
        stem_lists = genre_sdrs["Unknown / Other"]
        n = len(stem_lists["vocals"])
        stem_meds = {s: median_sdr(stem_lists[s]) for s in STEMS}
        valid = [v for v in stem_meds.values() if v is not None]
        genres_out.append(
            {
                "label": "Mixed / Unlabelled",
                "n_tracks": n,
                "sdr_vocals": stem_meds["vocals"],
                "sdr_drums": stem_meds["drums"],
                "sdr_bass": stem_meds["bass"],
                "sdr_other": stem_meds["other"],
                "sdr_mean": round(float(np.mean(valid)), 2) if valid else None,
            }
        )

    # --- Energy/complexity grouping (always available, no metadata needed) ---
    # Group tracks by their vocals SDR quartile as a proxy for vocal prominence
    all_vocal_sdrs = [tr["sdr"].get("vocals") for tr in track_results if tr["sdr"].get("vocals") is not None]
    q33 = float(np.percentile(all_vocal_sdrs, 33)) if all_vocal_sdrs else 5.0
    q66 = float(np.percentile(all_vocal_sdrs, 66)) if all_vocal_sdrs else 8.0

    energy_groups = {
        "High separation quality (top third)": {s: [] for s in STEMS},
        "Mid separation quality (middle third)": {s: [] for s in STEMS},
        "Low separation quality (bottom third)": {s: [] for s in STEMS},
    }

    for tr in track_results:
        v_sdr = tr["sdr"].get("vocals")
        if v_sdr is None:
            continue
        if v_sdr >= q66:
            key = "High separation quality (top third)"
        elif v_sdr >= q33:
            key = "Mid separation quality (middle third)"
        else:
            key = "Low separation quality (bottom third)"
        for stem in STEMS:
            val = tr["sdr"].get(stem)
            if val is not None:
                energy_groups[key][stem].append(val)

    quality_tiers = []
    for label, stem_lists in energy_groups.items():
        n = len(stem_lists["vocals"])
        stem_meds = {s: median_sdr(stem_lists[s]) for s in STEMS}
        valid = [v for v in stem_meds.values() if v is not None]
        quality_tiers.append(
            {
                "label": label,
                "n_tracks": n,
                "sdr_vocals": stem_meds["vocals"],
                "sdr_drums": stem_meds["drums"],
                "sdr_bass": stem_meds["bass"],
                "sdr_other": stem_meds["other"],
                "sdr_mean": round(float(np.mean(valid)), 2) if valid else None,
            }
        )

    has_genre_data = any(g["label"] != "Mixed / Unlabelled" for g in genres_out)

    output = {
        "title": "HTDemucs Performance by Track Characteristics",
        "subtitle": (
            f"Genre breakdown and quality tier analysis on {len(track_results)} MUSDB18-7s tracks"
        ),
        "run_date": time.strftime("%B %d, %Y"),
        "run_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "model": model_key,
        "dataset": "MUSDB18-7s",
        "n_tracks": len(track_results),
        "has_genre_data": has_genre_data,
        "key_finding": (
            "Separation quality varies significantly across track types. "
            "Tracks in the top-quality tier average "
            f"{quality_tiers[0]['sdr_mean']} dB mean SDR, "
            f"vs {quality_tiers[-1]['sdr_mean']} dB for the lowest tier."
            if quality_tiers
            else "See results table."
        ),
        "genres": genres_out,
        "quality_tiers": quality_tiers,
    }

    save_yaml(output, output_path)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test 3: Genre and characteristic breakdown")
    parser.add_argument("--input", default="results/raw/test2_tracks.json")
    parser.add_argument("--output", default="results/genre_performance.yml")
    args = parser.parse_args()

    run(args.input, args.output)
