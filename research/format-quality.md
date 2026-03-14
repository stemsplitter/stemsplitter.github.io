---
layout: research-post
title: "Does Audio Format Affect Stem Separation Quality?"
description: "Benchmark measuring how WAV, MP3, and AAC input quality affects HTDemucs SDR scores on the MUSDB18-7s dataset."
data_key: format_quality
permalink: /research/format-quality/
---

## Methodology

Twenty test tracks from MUSDB18-7s were taken as WAV 24-bit reference audio. Each mixture was re-encoded to a target format via ffmpeg and decoded back to WAV before being processed by HTDemucs. This isolates the effect of format-induced audio degradation on separation quality.

All six formats were applied to the same 20 tracks so comparisons are apples-to-apples. SDR was computed against the ground truth stems using [mir\_eval](https://github.com/craffel/mir_eval) BSSEval v4.

**Formats tested:** WAV 24-bit, WAV 16-bit, MP3 320kbps, MP3 192kbps, MP3 128kbps, AAC 256kbps.

**Model:** htdemucs\_ft (fine-tuned, 4-stem). **Device:** Apple M4 MPS.

## Notes on the data

7-second clips introduce more per-track variance than full tracks would. The SDR numbers here should be read as indicative rather than as definitive absolute benchmarks. The relative differences between formats are reliable because each format is compared on the same set of clips.
