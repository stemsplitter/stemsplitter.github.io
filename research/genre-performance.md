---
layout: research-post
title: "HTDemucs Performance by Track Characteristics"
description: "How HTDemucs separation quality varies across genre and track type using MUSDB18-7s data."
data_key: genre_performance
permalink: /research/genre-performance/
---

## Methodology

This analysis uses per-track SDR results from the model comparison test (Test 2), grouped two ways.

**Quality tiers** group tracks by their vocals SDR tertile. The top third of tracks by vocal SDR is labelled "High separation quality," the middle third "Mid," and the bottom third "Low." This quantifies how much variance exists across the test set and which stem types benefit most from easier separation conditions.

**Genre grouping** uses genre metadata from the MUSDB18-7s track files where available. If the dataset sample used does not include genre tags (which varies by download), the genre table will not render and only quality-tier grouping is shown.

**Model:** htdemucs\_ft. **Dataset:** MUSDB18-7s (50 test tracks).

## Interpretation notes

Large differences between quality tiers indicate that HTDemucs performance is highly track-dependent. A low mean SDR on a specific genre or tier does not necessarily mean that genre is "hard" in absolute terms -- 7-second clips can include difficult sections (dense choruses, sustained instruments) that bias the sample.
