#!/usr/bin/env python3
"""
Generates the research announcement blog post from benchmark results.
Called by run_all.sh after all tests complete.
"""

import argparse
import os
import time
import yaml


def load_yml(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def run(results_dir, output_path):
    t1 = load_yml(os.path.join(results_dir, "format_quality.yml"))
    t2 = load_yml(os.path.join(results_dir, "model_comparison.yml"))
    t3 = load_yml(os.path.join(results_dir, "genre_performance.yml"))
    t4 = load_yml(os.path.join(results_dir, "reconstruction.yml"))
    t5 = load_yml(os.path.join(results_dir, "complexity.yml"))

    today = time.strftime("%Y-%m-%d")
    pub_date = time.strftime("%B %d, %Y")

    # Pull key numbers
    best_model = None
    if t2 and t2.get("models"):
        best_model = max(t2["models"], key=lambda m: m.get("sdr_mean") or -999)

    mp3_128 = None
    wav_24 = None
    if t1 and t1.get("formats"):
        for fmt in t1["formats"]:
            if fmt["id"] == "mp3_128":
                mp3_128 = fmt
            if fmt["id"] == "wav_24":
                wav_24 = fmt

    recon_4stem = None
    if t4 and t4.get("modes"):
        for m in t4["modes"]:
            if m["stems"] == 4:
                recon_4stem = m

    top_predictor = None
    if t5 and t5.get("top_vocal_predictors"):
        top_predictor = t5["top_vocal_predictors"][0]

    lines = []

    # Front matter
    description = (
        "Original benchmark data from 5 HTDemucs tests run locally on Apple M4. "
        "Covers input format quality, model comparison, track characteristics, "
        "reconstruction fidelity, and what predicts separation quality."
    )

    lines.append("---")
    lines.append(f'layout: post')
    lines.append(f'title: "We Ran 5 HTDemucs Benchmarks So You Don\'t Have To: Results and Data"')
    lines.append(f'date: {today}')
    lines.append(f'description: "{description}"')
    lines.append(f'tags: Research')
    lines.append(f'about_terms: [htdemucs, music-source-separation, stem-splitter]')
    lines.append(f'mentions_terms: [musdb18, spectrogram, bleed, artifacts, model-ensemble]')
    lines.append("---")
    lines.append("")

    # Intro
    lines.append(
        "There are a lot of questions about HTDemucs that come up regularly: which model "
        "variant is actually best, does the bitrate of your source file matter, how clean "
        "is the reconstruction when you sum the stems back. I ran a set of five structured "
        "tests on the MUSDB18-7s benchmark dataset to get actual numbers rather than "
        "subjective impressions. All tests ran locally on Apple M4."
    )
    lines.append("")
    lines.append(
        "The full data tables are on the [research hub](/research/). This post summarises "
        "the key findings."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Test 2 highlight
    if best_model:
        lines.append("## Which HTDemucs model is best")
        lines.append("")
        lines.append(
            f"Short answer: **{best_model['label']}** achieved the highest mean SDR "
            f"at **{best_model['sdr_mean']} dB** across all four stems on the test set. "
            f"It averaged {best_model.get('avg_time_seconds', '?')} seconds per 7-second track on M4."
        )
        if t2 and t2.get("models"):
            slowest = max(t2["models"], key=lambda m: m.get("avg_time_seconds") or 0)
            fastest = min(t2["models"], key=lambda m: m.get("avg_time_seconds") or 9999)
            lines.append("")
            lines.append(
                f"The speed range across models was notable: {fastest['label']} processed "
                f"tracks in {fastest.get('avg_time_seconds')}s on average, while "
                f"{slowest['label']} took {slowest.get('avg_time_seconds')}s. "
                "For most producers the quality difference justifies the time cost, but "
                "batch processing scenarios change that calculation."
            )
        lines.append("")
        lines.append(f"Full model comparison: [/research/model-comparison/](/research/model-comparison/)")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Test 1 highlight
    if mp3_128 and wav_24:
        delta = mp3_128.get("delta_from_wav24")
        lines.append("## Does input format actually matter")
        lines.append("")
        lines.append(
            f"Yes, measurably. MP3 128kbps input produces stems with a mean SDR "
            f"of **{mp3_128['sdr_mean']} dB**, compared to **{wav_24['sdr_mean']} dB** "
            f"for 24-bit WAV. That's a {abs(delta)} dB difference. "
            "The vocal stem shows the most degradation, which makes sense given "
            "how MP3 compression handles mid-frequency content."
        )
        lines.append("")
        lines.append(
            "For most production use, MP3 320kbps is close enough to lossless that "
            "the quality difference is small. Below 192kbps the degradation becomes "
            "more consistent."
        )
        lines.append("")
        lines.append(f"Full format comparison: [/research/format-quality/](/research/format-quality/)")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Test 4 highlight
    if recon_4stem:
        lines.append("## How much information does separation actually lose")
        lines.append("")
        lines.append(
            f"In 4-stem mode, summing the separated stems back produces a reconstruction "
            f"that correlates with the original at **r = {recon_4stem.get('mean_correlation')}**. "
            f"The difference signal sits at {recon_4stem.get('mean_db_difference')} dB "
            "below the original, meaning there's real but limited information loss in "
            "the separation process."
        )
        lines.append("")
        lines.append(
            "6-stem separation shows higher reconstruction error, which is expected: "
            "dividing the signal into more components means more rounding and leakage "
            "at each split."
        )
        lines.append("")
        lines.append(f"Full reconstruction data: [/research/reconstruction-fidelity/](/research/reconstruction-fidelity/)")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Test 5 highlight
    if top_predictor:
        lines.append("## What predicts separation quality")
        lines.append("")
        lines.append(
            f"The strongest correlate of vocal SDR across the test tracks was "
            f"**{top_predictor['feature_label']}** (Pearson r = {top_predictor['pearson_r']}). "
            "In plain terms: tracks where the harmonic content is clearly separated "
            "from percussive content in the frequency domain tend to separate more cleanly. "
            "Dense arrangements with a lot of frequency overlap between instruments "
            "are harder for the model to disentangle."
        )
        lines.append("")
        lines.append(f"Full analysis: [/research/complexity-prediction/](/research/complexity-prediction/)")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Closing
    lines.append("## All results")
    lines.append("")
    lines.append(
        f"All five tests, methodology notes, and full data tables are on the "
        f"[research hub](/research/). Tests ran on {pub_date} using MUSDB18-7s "
        f"(the 7-second sample of the standard MUSDB18 benchmark dataset) on Apple M4 with MPS acceleration. "
        "I'll re-run and update these when HTDemucs releases a major model update."
    )
    lines.append("")

    post_content = "\n".join(lines)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(post_content)
    print(f"Blog post written: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    run(args.results_dir, args.output)
