---
layout: research-post
title: "What Makes a Track Hard to Separate?"
description: "Audio feature correlation analysis showing which track properties predict higher or lower HTDemucs SDR on MUSDB18-7s."
data_key: complexity
permalink: /research/complexity-prediction/
---

## Methodology

Audio features were extracted from each MUSDB18-7s mixture using [librosa](https://librosa.org). These features were then correlated with the per-track SDR values from the htdemucs\_ft model comparison run (Test 2) using Pearson r.

**Features computed:**
- RMS energy (overall loudness)
- Spectral centroid (brightness)
- Spectral flatness (how tonal vs noisy the signal is)
- Zero crossing rate (noisiness proxy)
- Harmonic and percussive energy (via HPSS decomposition)
- Harmonic-to-percussive ratio
- Onset density (rhythmic activity)
- Chroma variance (harmonic complexity)
- Vocal band energy (200Hz-3kHz)

Each feature was correlated separately with vocal, drums, bass, and other SDR. The table shows the top predictors for vocal SDR specifically.

## Interpretation

A positive correlation means tracks with a higher feature value tend to produce higher SDR. A negative correlation means the feature is associated with worse separation. Values close to 0 indicate no reliable relationship in this dataset.

Pearson r magnitudes above 0.3 are considered moderate; above 0.5 are substantial. With 50 tracks, even moderate correlations should be interpreted carefully.
