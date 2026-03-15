---
layout: research-hub
title: "HTDemucs Benchmark Research"
description: "Original benchmark data from HTDemucs tests run locally on Apple M4. Covers input format quality, model comparison, track characteristics, reconstruction fidelity, complexity prediction, and a head-to-head comparison with Spleeter."
permalink: /research/
---

Six structured tests on the [MUSDB18-7s](https://zenodo.org/record/1117372) benchmark dataset, run locally on Apple M4 using MPS acceleration. Tests 1-5 focus on HTDemucs performance across different conditions. Test 6 runs a head-to-head comparison between [Spleeter](https://github.com/deezer/spleeter) (TensorFlow, CPU) and HTDemucs (PyTorch, MPS) to quantify the quality and speed gap on Apple Silicon.

All raw data is available in the [site repository](https://github.com/stemsplitter/stemsplitter.github.io/tree/main/_data/research). The benchmark scripts are published at [github.com/attackseo/htdemucs-benchmark](https://github.com/attackseo/htdemucs-benchmark) so results can be independently reproduced. Methodology details are on each individual test page.
