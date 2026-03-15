---
layout: research-post
title: "Spleeter vs HTDemucs: Quality and Speed on Apple M4"
description: "Head-to-head SDR quality and processing time comparison between Spleeter 4-stem (TensorFlow CPU) and HTDemucs base (PyTorch MPS) on 50 MUSDB18-7s test tracks."
data_key: spleeter_comparison
yaml_file: spleeter_comparison.yml
cite_key: michaels2026spleeter
measurement_technique: "BSSEval v4 SDR via mir_eval; wall-clock processing time on Apple M4. Spleeter 2.1.0 on TensorFlow 2.16.2 (CPU only, no MPS support). HTDemucs 4.0.1 base model on PyTorch 2.10.0 with MPS acceleration."
variable_measured: "Signal-to-Distortion Ratio (SDR) in dB per stem; processing time in seconds per 7-second clip"
permalink: /research/spleeter-vs-htdemucs/
---

## Background

[Spleeter](https://github.com/deezer/spleeter) was released by Deezer Research in 2019 and became one of the most widely used open source stem splitters. It uses a U-Net convolutional architecture trained on TensorFlow. [HTDemucs](https://github.com/facebookresearch/demucs) arrived later, in 2022, combining a hybrid transformer-convolutional architecture that significantly raised the state of the art on MUSDB18 benchmarks.

Both the [2022 HTDemucs paper](https://arxiv.org/abs/2211.02302) (Defossez) and subsequent comparisons report HTDemucs outperforming Spleeter in mean SDR on full-length MUSDB18 tracks. What has not been benchmarked is their relative performance on Apple Silicon in 2026, where the hardware gap between the two matters: Spleeter runs TensorFlow, which has no MPS backend, so it runs CPU-only on M-series chips. HTDemucs uses PyTorch which fully supports Apple's MPS GPU acceleration.

This test runs both models on the same 50 MUSDB18-7s clips under identical conditions, measuring both separation quality and real-world processing speed.

## Methodology

**Models tested:**
- `Spleeter 2.1.0` with `spleeter:4stems` pretrained weights -- TensorFlow 2.16.2, CPU only on Apple M4
- `htdemucs` base model (demucs 4.0.1) -- PyTorch 2.10.0 with MPS acceleration on Apple M4

**Dataset:** [MUSDB18-7s](https://zenodo.org/record/1117372) -- the 50 test split tracks (7-second clips from the standard 150-track benchmark). Same tracks used across all 5 prior benchmark tests on this site.

**Metric:** BSSEval v4 SDR via [mir\_eval](https://github.com/craffel/mir_eval). Median across tracks per stem. Standard 4-stem targets: vocals, drums, bass, other.

**Device:** Apple M4 MacBook Pro. Spleeter is TensorFlow-based and does not support MPS; it runs all computation on CPU. HTDemucs is PyTorch-based and runs on MPS. Processing time is wall-clock seconds per 7-second clip, measured with `time.time()` around the separation call only.

## Notes on interpreting speed numbers

Times are per 7-second clip. A real 4-minute song contains roughly 34 such clips. The speed difference shown here compounds directly into real-world processing time. Spleeter's CPU limitation on Apple Silicon is a structural constraint; it cannot be resolved by updating Spleeter alone, since TensorFlow currently has no MPS support for the operations Spleeter uses.
