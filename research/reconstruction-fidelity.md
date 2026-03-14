---
layout: research-post
title: "How Much Information Does Stem Separation Actually Lose?"
description: "Measuring reconstruction fidelity when stems separated by HTDemucs are summed back to a mix. Tests 2-stem, 4-stem, and 6-stem modes."
data_key: reconstruction
yaml_file: reconstruction.yml
cite_key: michaels2026reconstruction
measurement_technique: "Mean squared error, Pearson correlation, and dB difference between original MUSDB18-7s mixture and the sum of all separated stems."
variable_measured: "Reconstruction fidelity: mean squared error (MSE), Pearson r, and dB difference signal level relative to original"
permalink: /research/reconstruction-fidelity/
---

## Methodology

Each mixture in the MUSDB18-7s test set was separated into stems, which were then summed back together. The sum was compared to the original mixture using three metrics:

- **Mean squared error (MSE):** direct amplitude difference between original and reconstruction
- **Pearson correlation:** captures temporal synchrony and shape fidelity between original and reconstruction
- **dB difference:** the reconstruction error expressed as a level relative to the original signal, in dB

Separation modes tested:
- **2-stem:** vocals and accompaniment (accompaniment = drums + bass + other summed from a 4-stem run)
- **4-stem:** vocals, drums, bass, other using htdemucs\_ft
- **6-stem:** vocals, drums, bass, guitar, piano, other using htdemucs\_6s

**Device:** Apple M4 MPS. **Dataset:** MUSDB18-7s (50 test tracks).

## What these numbers tell you

A perfect reconstruction would have MSE = 0, correlation = 1.0, and dB difference of -infinity (no difference signal at all). Real-world reconstruction is imperfect because the separation model introduces filter ringing, bleed, and frequency masking artefacts that don't cancel when stems are summed.

The practical implication: if you separate a track and then re-mix the stems at equal volume, the result will not be bit-identical to the original mix. The dB difference number shows how audible that difference is in principle.
