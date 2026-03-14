---
layout: research-post
title: "HTDemucs Model Variant Comparison: Quality vs Speed"
description: "SDR and processing time comparison across htdemucs, htdemucs_ft, htdemucs_6s, and hdemucs_mmi on MUSDB18-7s."
data_key: model_comparison
yaml_file: model_comparison.yml
cite_key: michaels2026models
measurement_technique: "BSSEval v4 SDR via mir_eval Python package; wall-clock processing time on Apple M4 MPS. All four HTDemucs variants evaluated on 50 MUSDB18-7s test tracks."
variable_measured: "Signal-to-Distortion Ratio (SDR) in dB per stem; processing time in seconds per 7-second clip"
permalink: /research/model-comparison/
---

## Methodology

All four publicly available HTDemucs variants were evaluated on the full 50-track MUSDB18-7s test set. Each track was processed independently per model and the wall-clock time recorded. SDR was computed against ground truth stems using BSSEval v4 via [mir\_eval](https://github.com/craffel/mir_eval).

**Models evaluated:**
- `htdemucs` -- base hybrid transformer-convolutional model
- `htdemucs_ft` -- fine-tuned on additional data, generally higher SDR on standard benchmarks
- `htdemucs_6s` -- 6-stem variant (adds guitar and piano stems); only standard 4-stem SDR reported for comparability
- `hdemucs_mmi` -- the older Hybrid Demucs (non-transformer) variant trained with [multi-mirror input](https://github.com/facebookresearch/demucs) on extra data

**Device:** Apple M4 MPS. Models run at default segment size.

## Notes on speed numbers

Times are per 7-second clip, not per minute of audio. To extrapolate to real-world usage: a 4-minute track at 44100Hz would take roughly 34x as long as the per-clip time shown. These are single-run numbers; actual throughput varies with background system load.
