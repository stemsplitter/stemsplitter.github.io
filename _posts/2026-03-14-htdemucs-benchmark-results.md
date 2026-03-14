---
layout: post
title: "We Ran 5 HTDemucs Benchmarks So You Don't Have To: Results and Data"
date: 2026-03-14
description: "Original benchmark data from 5 HTDemucs tests run locally on Apple M4. Covers input format quality, model comparison, track characteristics, reconstruction fidelity, and what predicts separation quality."
tags: Research
about_terms: [htdemucs, music-source-separation, stem-splitter]
mentions_terms: [musdb18, spectrogram, bleed, artifacts, model-ensemble]
---

There are a lot of questions about HTDemucs that come up regularly: which model variant is actually best, does the bitrate of your source file matter, how clean is the reconstruction when you sum the stems back. I ran a set of five structured tests on the MUSDB18-7s benchmark dataset to get actual numbers rather than subjective impressions. All tests ran locally on Apple M4.

The full data tables are on the [research hub](/research/). This post summarises the key findings.

---

## Which HTDemucs model is best

Short answer: **HTDemucs (base)** achieved the highest mean SDR at **8.38 dB** across all four stems on the test set. It averaged 1.8 seconds per 7-second track on M4.

The speed range across models was notable: HTDemucs 6S (6-stem) processed tracks in 1.6s on average, while HTDemucs FT (fine-tuned) took 6.4s. For most producers the quality difference justifies the time cost, but batch processing scenarios change that calculation.

Full model comparison: [/research/model-comparison/](/research/model-comparison/)

---

## Does input format actually matter

Yes, measurably. MP3 128kbps input produces stems with a mean SDR of **7.8 dB**, compared to **8.04 dB** for 24-bit WAV. That's a 0.24 dB difference. The vocal stem shows the most degradation, which makes sense given how MP3 compression handles mid-frequency content.

For most production use, MP3 320kbps is close enough to lossless that the quality difference is small. Below 192kbps the degradation becomes more consistent.

Full format comparison: [/research/format-quality/](/research/format-quality/)

---

## How much information does separation actually lose

In 4-stem mode, summing the separated stems back produces a reconstruction that correlates with the original at **r = 0.996**. The difference signal sits at -21.6 dB below the original, meaning there's real but limited information loss in the separation process.

6-stem separation shows higher reconstruction error, which is expected: dividing the signal into more components means more rounding and leakage at each split.

Full reconstruction data: [/research/reconstruction-fidelity/](/research/reconstruction-fidelity/)

---

## What predicts separation quality

The strongest correlate of vocal SDR across the test tracks was **Chroma variance (harmonic complexity)** (Pearson r = 0.522). In plain terms: tracks where the harmonic content is clearly separated from percussive content in the frequency domain tend to separate more cleanly. Dense arrangements with a lot of frequency overlap between instruments are harder for the model to disentangle.

Full analysis: [/research/complexity-prediction/](/research/complexity-prediction/)

---

## All results

All five tests, methodology notes, and full data tables are on the [research hub](/research/). Tests ran on March 14, 2026 using MUSDB18-7s (the 7-second sample of the standard MUSDB18 benchmark dataset) on Apple M4 with MPS acceleration. I'll re-run and update these when HTDemucs releases a major model update.
