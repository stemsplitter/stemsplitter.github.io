---
layout: page
title: "Stem Splitter Glossary: Audio and AI Terms Explained"
description: "A reference glossary of terms used in stem splitting, music source separation, and AI audio tools. From stems and spectrograms to HTDemucs and STFT."
permalink: /glossary/
---

This glossary covers the key terms you'll encounter when working with stem splitters, reading about music source separation research, or evaluating AI audio tools. Definitions are written for working producers and audio engineers, not computer scientists, though technical context is included where it matters.

---

**Artifacts**
Unwanted sounds introduced by the separation process. These can include metallic or "watery" distortion on vocals, clicks, faint ghost notes from other instruments, or reverb tails that get clipped unexpectedly. Artifacts are one of the main quality differentiators between older and newer separation models. See [stem splitter artifacts and bleed]({{ "/stem-splitter-artifacts-bleed/" | relative_url }}) for a deeper look at how they occur and how to minimize them.

**Bass stem**
The isolated low-frequency bass content extracted from a mix, typically targeting bass guitar or synthesizer bass. Bass stems are notoriously difficult to separate cleanly because bass frequencies overlap significantly with kick drum content. A high-quality bass stem should contain the fundamental note content of the bass instrument without significant kick bleed.

**Bit depth**
The number of bits used to represent each audio sample. 16-bit is CD standard; 24-bit is the working standard in professional audio. Higher bit depth provides more dynamic range and less quantization noise. When exporting stems, working in 24-bit preserves more headroom for downstream processing.

**Bleed**
Bleed (also called leakage) refers to parts of one instrument appearing in a stem intended for a different instrument. Vocal bleed in the instrumental stem, or kick drum bleed in the bass stem, are common examples. Reducing bleed is one of the central engineering challenges in source separation. See [stem splitter artifacts and bleed]({{ "/stem-splitter-artifacts-bleed/" | relative_url }}) for more detail.

**BPM**
Beats Per Minute. A measure of tempo. Stem splitters don't require BPM information to operate, but downstream tools like DAWs and sample libraries use BPM metadata for tempo-syncing stems. Some online tools auto-detect BPM and include it in the output file metadata.

**DAW**
Digital Audio Workstation. The software environment where most audio production work happens, including importing and working with stems. Common DAWs include Ableton Live, Logic Pro, Pro Tools, FL Studio, and Reaper. Stems produced by a stem splitter are typically dragged directly into a DAW session for further use.

**Demucs**
An open-source music source separation model developed by Meta AI Research. Demucs has gone through multiple major versions since its initial release in 2019, with HTDemucs being the current state of the art. It supports 4-stem and 6-stem separation and benchmarks near the top of the field on standard evaluations. See the [Demucs GitHub repository](https://github.com/facebookresearch/demucs) for documentation and model weights, and the [HTDemucs paper on arXiv](https://arxiv.org/abs/2111.03600) for the research behind the current architecture.

**Drum stem**
The isolated drum and percussion content extracted from a mix. A well-separated drum stem should contain kick, snare, hi-hats, cymbals, and auxiliary percussion without significant bleed from bass, synths, or vocals. Drum stems are widely used in remixing, practice tracks, and rhythmic analysis.

**FLAC**
Free Lossless Audio Codec. An audio format that compresses files without discarding any audio data, unlike MP3. FLAC files are significantly larger than MP3s but contain all of the original audio information. Stem splitters generally produce better results from high-quality source files, and FLAC is preferred over compressed formats when available.

**Frequency**
The rate of oscillation of a sound wave, measured in Hertz (Hz). Musical pitch corresponds to frequency: lower frequencies are lower pitches, higher are higher. Most audible audio sits between roughly 20 Hz and 20,000 Hz. Stem separation works in part by identifying the characteristic frequency patterns associated with different instruments.

**HTDemucs**
The current primary model in the Demucs family, released by Meta AI Research. HTDemucs uses a hybrid architecture that combines convolutional layers and transformers to model both the waveform and spectrogram representation of audio simultaneously. This dual-domain approach improves separation quality, particularly on complex and densely arranged material. See the [related model comparison post]({{ "/demucs-mdxnet-htdemucs-models/" | relative_url }}) for a fuller discussion of how it compares to earlier versions and other architectures.

**Karaoke track**
An instrumental version of a song with the lead vocals removed. Karaoke tracks are one of the most common consumer applications of stem splitting. The quality of a karaoke track depends primarily on how cleanly the vocal stem is separated, particularly on sections where the arrangement is dense.

**MDX-Net**
A neural network architecture developed for music demixing competitions, associated with the MDX (Music Demixing) challenge. MDX-Net models are known for strong performance on vocal and instrument separation and form the basis for several commercial and open-source tools. Many online stem splitters use MDX-Net or hybrid approaches that combine it with Demucs-style processing.

**MUSDB18**
A standardized dataset used for benchmarking music source separation systems. MUSDB18 contains 150 tracks with professionally recorded stems, allowing researchers to evaluate model performance consistently across the same material. Results on MUSDB18 are the standard way of comparing model quality in academic and research contexts. See the [MUSDB18 dataset page](https://sigsep.github.io/datasets/musdb.html) for more information.

**Music source separation**
The technical field focused on isolating individual audio sources from a mixed recording. Stem splitting is a practical application of music source separation research. The field draws on signal processing, machine learning, and psychoacoustics, and has advanced significantly since the introduction of deep learning-based approaches. [Wikipedia's article on music source separation](https://en.wikipedia.org/wiki/Music_source_separation) provides a useful overview of the history and methodology.

**Other stem**
In a 4-stem separation model, the "other" stem captures everything that isn't vocals, drums, or bass. This typically includes guitars, keyboards, synths, strings, and any additional melodic or harmonic content. The catch-all nature of this stem makes it one of the harder ones to separate cleanly, since it encompasses a broad range of frequency content.

**Sample rate**
The number of audio samples captured per second, measured in Hz or kHz. 44.1 kHz is CD standard; 48 kHz is common in video production; 96 kHz is used in high-resolution audio contexts. Higher sample rates capture more high-frequency detail but produce larger files. Stem splitters typically work at or convert to 44.1 kHz internally.

**Spectrogram**
A visual representation of audio frequency content over time. The horizontal axis is time, the vertical axis is frequency, and brightness or color indicates amplitude at each point. Many source separation models operate on spectrograms rather than raw waveforms, treating the separation problem as an image masking task. HTDemucs operates in both the waveform and spectrogram domains simultaneously, which is part of what gives it an edge on complex material.

**Spleeter**
An open-source source separation library released by Deezer Research in 2019. Spleeter was one of the first widely accessible neural stem splitters, offering 2-stem, 4-stem, and 5-stem separation with a straightforward command-line interface. It remains useful for batch processing workflows and as a historical baseline for comparisons, though it has been surpassed in output quality by newer models. See the [Spleeter GitHub repository](https://github.com/deezer/spleeter) for source and documentation.

**Stem**
A single isolated audio component extracted from a mixed recording. Common stems include vocals, drums, bass, and other instruments. The term comes from music production, where projects are often delivered as discrete elements for mixing or further processing. A "stem file" is the individual audio file containing that isolated component.

**Stem splitter**
A tool that takes a mixed audio recording and separates it into individual component stems using AI-based source separation. The [complete guide to stem splitting]({{ "/complete-guide-stem-splitting/" | relative_url }}) covers the full picture for anyone newer to the concept. See also: [how AI stem separation works]({{ "/how-ai-stem-separation-works/" | relative_url }}).

**STFT (Short-Time Fourier Transform)**
A mathematical technique that converts an audio signal into its frequency components across a series of short, overlapping time windows. The STFT is foundational to spectrogram-based audio processing and is used in many source separation pipelines as a way of representing audio in a form more amenable to neural network processing. The inverse STFT converts the processed frequency representation back into audio.

**VR Architecture**
Vocal Remover Architecture. A class of neural network designs optimized for separating vocal content from instrumentals. VR Architecture models are the basis for several tools within the Ultimate Vocal Remover (UVR) application and are known for particularly clean vocal isolation on appropriate material. See the [UVR5 GitHub repository](https://github.com/Anjok07/ultimatevocalremovergui) for more information.

**Vocal isolation**
The process of extracting the vocal stem from a mixed recording, leaving behind a clean instrumental version. Vocal isolation quality is one of the most frequently evaluated metrics for stem splitters because the results are audibly obvious. A clean vocal isolation has minimal instrument bleed and no audible processing artifacts on the voice.

**Vocal remover**
Often used interchangeably with "stem splitter" or "vocal isolator," though in practice it usually refers to tools focused specifically on the vocal/instrumental split rather than full multi-stem separation. Most vocal removers produce two outputs: a vocals stem and an accompaniment stem. See also: vocal isolation, karaoke track.

**WAV**
Waveform Audio File Format. An uncompressed audio format that stores raw audio data without any quality loss. WAV files are the standard format for professional audio work and for stem exports. Saving stems in WAV preserves the full quality of the separation output and avoids introducing compression artifacts into the downstream workflow.

---

For answers to common questions about stem splitting, see the [FAQ]({{ "/faq/" | relative_url }}). For a broader introduction to how all of this works, the [complete guide to stem splitting]({{ "/complete-guide-stem-splitting/" | relative_url }}) is the place to start.
