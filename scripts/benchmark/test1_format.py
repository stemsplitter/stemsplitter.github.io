#!/usr/bin/env python3
"""
Test 1: Input Format Quality Impact
------------------------------------
Measures how audio format and bitrate affect HTDemucs separation quality.
Re-encodes the same mixture to 6 formats via ffmpeg, separates each,
then computes SDR vs ground truth stems.

Unique contribution: no one has published systematic SDR numbers
for format degradation on a standard benchmark dataset.
"""

import argparse
import os
import subprocess
import tempfile
import time
from pathlib import Path

import numpy as np
import soundfile as sf
from tqdm import tqdm

from utils import compute_sdr, get_device, load_model, load_musdb, median_sdr, save_yaml, separate_track

N_TRACKS = 20  # Use first 20 of 50 test tracks

FORMATS = [
    {
        "id": "wav_24",
        "label": "WAV 24-bit",
        "category": "lossless",
        "ffmpeg_args": ["-acodec", "pcm_s24le"],
        "ext": "wav",
    },
    {
        "id": "wav_16",
        "label": "WAV 16-bit",
        "category": "lossless",
        "ffmpeg_args": ["-acodec", "pcm_s16le"],
        "ext": "wav",
    },
    {
        "id": "mp3_320",
        "label": "MP3 320kbps",
        "category": "lossy",
        "ffmpeg_args": ["-acodec", "libmp3lame", "-b:a", "320k"],
        "ext": "mp3",
    },
    {
        "id": "mp3_192",
        "label": "MP3 192kbps",
        "category": "lossy",
        "ffmpeg_args": ["-acodec", "libmp3lame", "-b:a", "192k"],
        "ext": "mp3",
    },
    {
        "id": "mp3_128",
        "label": "MP3 128kbps",
        "category": "lossy",
        "ffmpeg_args": ["-acodec", "libmp3lame", "-b:a", "128k"],
        "ext": "mp3",
    },
    {
        "id": "aac_256",
        "label": "AAC 256kbps",
        "category": "lossy",
        "ffmpeg_args": ["-acodec", "aac", "-b:a", "256k"],
        "ext": "m4a",
    },
]

STEMS = ["vocals", "drums", "bass", "other"]


def reencode_audio(audio, rate, fmt):
    """
    Write audio to disk, encode to target format, decode back to numpy.
    Uses a temp directory so nothing persists on disk.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "src.wav")
        encoded = os.path.join(tmpdir, f"encoded.{fmt['ext']}")
        decoded = os.path.join(tmpdir, "decoded.wav")

        sf.write(src, audio, rate, subtype="PCM_24")

        # Encode to target format
        subprocess.run(
            ["ffmpeg", "-i", src] + fmt["ffmpeg_args"] + [encoded, "-y", "-loglevel", "quiet"],
            check=True,
        )

        # Decode back to float WAV so HTDemucs can read it
        subprocess.run(
            ["ffmpeg", "-i", encoded, "-acodec", "pcm_f32le", decoded, "-y", "-loglevel", "quiet"],
            check=True,
        )

        result, _ = sf.read(decoded, always_2d=True)
        return result


def run(output_path, n_tracks=N_TRACKS, data_root=None):
    device = get_device()
    print(f"Device: {device}")

    print("Loading MUSDB18-7s test tracks...")
    tracks = load_musdb(data_root=data_root, subset="test")
    tracks = tracks[:n_tracks]

    model = load_model("htdemucs_ft", device)

    # sdrs[format_id][stem] = list of SDR values
    sdrs = {fmt["id"]: {s: [] for s in STEMS} for fmt in FORMATS}

    for track in tqdm(tracks, desc="Tracks"):
        mixture = track.audio  # (samples, 2)
        rate = track.rate
        refs = {s: track.targets[s].audio for s in STEMS if s in track.targets}

        for fmt in FORMATS:
            try:
                reencoded = reencode_audio(mixture, rate, fmt)
                min_len = min(len(mixture), len(reencoded))
                estimates = separate_track(reencoded[:min_len], rate, model, device)

                for stem in STEMS:
                    if stem not in refs or stem not in estimates:
                        continue
                    sdr = compute_sdr(refs[stem][:min_len], estimates[stem][:min_len])
                    if sdr is not None:
                        sdrs[fmt["id"]][stem].append(sdr)

            except Exception as e:
                tqdm.write(f"  Skipped {track.name} / {fmt['label']}: {e}")
                continue

    # Build output structure for Jekyll
    formats_out = []
    baseline_mean = None

    for i, fmt in enumerate(FORMATS):
        stem_medians = {s: median_sdr(sdrs[fmt["id"]][s]) for s in STEMS}
        valid = [v for v in stem_medians.values() if v is not None]
        fmt_mean = round(float(np.mean(valid)), 2) if valid else None

        if i == 0:
            baseline_mean = fmt_mean

        delta = (
            round(fmt_mean - baseline_mean, 2)
            if fmt_mean is not None and baseline_mean is not None
            else None
        )

        formats_out.append(
            {
                "id": fmt["id"],
                "label": fmt["label"],
                "category": fmt["category"],
                "sdr_vocals": stem_medians["vocals"],
                "sdr_drums": stem_medians["drums"],
                "sdr_bass": stem_medians["bass"],
                "sdr_other": stem_medians["other"],
                "sdr_mean": fmt_mean,
                "delta_from_wav24": delta,
            }
        )

    # Find worst format for the key finding
    valid_fmts = [f for f in formats_out if f["sdr_mean"] is not None]
    worst = min(valid_fmts, key=lambda x: x["sdr_mean"]) if valid_fmts else None
    best = formats_out[0]

    key_finding = (
        f"{worst['label']} input reduces mean SDR by "
        f"{abs(worst['delta_from_wav24'])} dB compared to {best['label']} "
        f"({worst['sdr_mean']} dB vs {best['sdr_mean']} dB)"
        if worst and worst.get("delta_from_wav24")
        else "See results table for format quality comparison."
    )

    output = {
        "title": "Does Audio Format Affect Stem Separation Quality?",
        "subtitle": f"SDR benchmark across 6 audio formats on {n_tracks} MUSDB18-7s test tracks using htdemucs_ft",
        "run_date": time.strftime("%B %d, %Y"),
        "run_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "model": "htdemucs_ft",
        "dataset": "MUSDB18-7s",
        "dataset_url": "https://zenodo.org/record/1117372",
        "n_tracks": n_tracks,
        "stems": STEMS,
        "key_finding": key_finding,
        "formats": formats_out,
    }

    save_yaml(output, output_path)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test 1: Format degradation benchmark")
    parser.add_argument("--output", default="results/format_quality.yml")
    parser.add_argument("--n-tracks", type=int, default=N_TRACKS)
    parser.add_argument("--data-root", default=None, help="Path to MUSDB18 data directory")
    args = parser.parse_args()

    run(args.output, n_tracks=args.n_tracks, data_root=args.data_root)
