---
layout: glossary
title: "Stem Splitter Glossary: Audio and AI Terms Explained"
description: "A reference glossary of terms used in stem splitting, music source separation, and AI audio tools. From stems and spectrograms to HTDemucs and STFT."
permalink: /glossary/
---

This glossary covers the key terms you'll encounter when working with stem splitters, reading about music source separation research, or evaluating AI audio tools. Definitions are written for working producers and audio engineers, not computer scientists, though technical context is included where it matters.

<nav class="glossary-alpha-nav" aria-label="Jump to letter">
<a href="#a-cappella">A</a> · <a href="#bass-stem">B</a> · <a href="#daw">D</a> · <a href="#flac">F</a> · <a href="#htdemucs">H</a> · <a href="#instrumental">I</a> · <a href="#karaoke-track">K</a> · <a href="#mashup">M</a> · <a href="#online-stem-splitter">O</a> · <a href="#remix">R</a> · <a href="#sampling">S</a> · <a href="#vr-architecture">V</a> · <a href="#wav">W</a>
</nav>

---

### A cappella {#a-cappella}

An a cappella recording consists of vocals only, with no instrumental accompaniment. In the context of stem splitting, an a cappella is what you get when you extract just the vocal stem from a mixed track. Tools like [StemSplit.io](https://stemsplit.io) can produce a clean a cappella from most commercial recordings in under a minute. See [how to isolate vocals from a song]({{ "/how-to-isolate-vocals-from-a-song/" | relative_url }}).

### AI music splitter {#ai-music-splitter}

An AI music splitter is another term for a stem splitter: software that uses artificial intelligence to separate a mixed audio recording into its individual component parts. The "AI" in the name refers to the deep learning models (such as HTDemucs and MDX-Net) that power modern separation tools. AI music splitters have largely replaced older phase-cancellation vocal removal methods, which produced noticeably lower quality results.

### Artifacts {#artifacts}

Unwanted sounds introduced by the separation process. These can include metallic or "watery" distortion on vocals, clicks, faint ghost notes from other instruments, or reverb tails that get clipped unexpectedly. Artifacts are one of the main quality differentiators between older and newer separation models. See [stem splitter artifacts and bleed]({{ "/stem-splitter-artifacts-bleed/" | relative_url }}) for a deeper look at how they occur and how to minimize them.

### Bass stem {#bass-stem}

The isolated low-frequency bass content extracted from a mix, typically targeting bass guitar or synthesizer bass. Bass stems are notoriously difficult to separate cleanly because bass frequencies overlap significantly with kick drum content. A high-quality bass stem should contain the fundamental note content of the bass instrument without significant kick bleed.

### Bit depth {#bit-depth}

The number of bits used to represent each audio sample. 16-bit is CD standard; 24-bit is the working standard in professional audio. Higher bit depth provides more dynamic range and less quantization noise. When exporting stems, working in 24-bit preserves more headroom for downstream processing.

### Bleed {#bleed}

Bleed (also called leakage) refers to parts of one instrument appearing in a stem intended for a different instrument. Vocal bleed in the instrumental stem, or kick drum bleed in the bass stem, are common examples. Reducing bleed is one of the central engineering challenges in source separation. See [stem splitter artifacts and bleed]({{ "/stem-splitter-artifacts-bleed/" | relative_url }}) for more detail.

### BPM {#bpm}

Beats Per Minute. A measure of tempo. Stem splitters don't require BPM information to operate, but downstream tools like DAWs and sample libraries use BPM metadata for tempo-syncing stems. Some online tools auto-detect BPM and include it in the output file metadata.

### DAW {#daw}

Digital Audio Workstation. The software environment where most audio production work happens, including importing and working with stems. Common DAWs include Ableton Live, Logic Pro, Pro Tools, FL Studio, and Reaper. Stems produced by a stem splitter are typically dragged directly into a DAW session for further use. See [bringing stems into your DAW]({{ "/using-stems-in-your-daw/" | relative_url }}) for the practical workflow.

### Demucs {#demucs}

An open-source music source separation model developed by Meta AI Research. Demucs has gone through multiple major versions since its initial release in 2019, with HTDemucs being the current state of the art. It supports 4-stem and 6-stem separation and benchmarks near the top of the field on standard evaluations. See the [Demucs GitHub repository](https://github.com/facebookresearch/demucs) for documentation and model weights, and the [HTDemucs paper on arXiv](https://arxiv.org/abs/2111.03600) for the research behind the current architecture.

### Drum stem {#drum-stem}

The isolated drum and percussion content extracted from a mix. A well-separated drum stem should contain kick, snare, hi-hats, cymbals, and auxiliary percussion without significant bleed from bass, synths, or vocals. Drum stems are widely used in remixing, practice tracks, and rhythmic analysis. See [how to extract drum stems]({{ "/how-to-extract-drum-stems/" | relative_url }}).

### FLAC {#flac}

Free Lossless Audio Codec. An audio format that compresses files without discarding any audio data, unlike MP3. FLAC files are significantly larger than MP3s but contain all of the original audio information. Stem splitters generally produce better results from high-quality source files, and FLAC is preferred over compressed formats when available.

### Frequency {#frequency}

The rate of oscillation of a sound wave, measured in Hertz (Hz). Musical pitch corresponds to frequency: lower frequencies are lower pitches, higher are higher. Most audible audio sits between roughly 20 Hz and 20,000 Hz. Stem separation works in part by identifying the characteristic frequency patterns associated with different instruments.

### HTDemucs {#htdemucs}

The current primary model in the Demucs family, released by Meta AI Research. HTDemucs uses a hybrid architecture that combines convolutional layers and transformers to model both the waveform and spectrogram representation of audio simultaneously. This dual-domain approach improves separation quality, particularly on complex and densely arranged material. See the [model comparison post]({{ "/demucs-mdxnet-htdemucs-models/" | relative_url }}) for a fuller discussion of how it compares to earlier versions and other architectures.

### Instrumental {#instrumental}

An instrumental track is a version of a song with the lead vocals removed, leaving only the musical arrangement. Creating an instrumental is one of the most common reasons people use stem splitters, and the output is functionally the same as a karaoke backing track. For most well-produced pop and hip-hop, a good stem splitter will produce a clean instrumental with minimal vocal bleed. See [how to make a karaoke track]({{ "/how-to-make-karaoke-track/" | relative_url }}).

### Karaoke track {#karaoke-track}

An instrumental version of a song with the lead vocals removed, used for singing along. Karaoke tracks are one of the most common consumer applications of stem splitting. The quality depends primarily on how cleanly the AI can identify and isolate the vocal, which varies by genre and production style. See [how to make a karaoke track]({{ "/how-to-make-karaoke-track/" | relative_url }}).

### Mashup {#mashup}

A music production technique where elements from two or more different songs are combined into a new recording. Stem splitters enable mashups by making it possible to extract the vocal from one song and place it over the instrumental of another. The main technical challenges are matching key and tempo between the two tracks. See [stem splitting for sampling and beatmaking]({{ "/stem-splitting-for-sampling-beatmaking/" | relative_url }}).

### MDX-Net {#mdx-net}

A neural network architecture developed for music demixing competitions, associated with the MDX (Music Demixing) challenge. MDX-Net models are known for strong performance on vocal and instrument separation and form the basis for several commercial and open-source tools. Many online stem splitters use MDX-Net or hybrid approaches combining it with Demucs-style processing.

### Model ensemble {#model-ensemble}

The technique of running two or more separate AI models on the same audio input and combining their outputs. Ensemble approaches can produce cleaner stems than any single model alone because different models tend to have different failure modes: one might handle vocals better, another might produce a cleaner bass. Tools like [UVR5](https://github.com/Anjok07/ultimatevocalremovergui) support ensemble separation, and some professional online tools use ensemble methods internally.

### MUSDB18 {#musdb18}

A standardized dataset used for benchmarking music source separation systems. MUSDB18 contains 150 tracks with professionally recorded stems, allowing researchers to evaluate model performance consistently across the same material. Results on MUSDB18 are the standard way of comparing model quality in academic and research contexts. See the [MUSDB18 dataset page](https://sigsep.github.io/datasets/musdb.html) for more information.

### Multitrack recording {#multitrack-recording}

An audio recording where each instrument or sound source is captured on its own separate track, rather than being mixed together into a stereo file. Professional recordings are made this way, with individual tracks for vocals, drums, bass, guitars, and so on. When a finished mix is released without the original multitracks, stem splitters can produce approximate reconstructions of what those individual tracks contained. The gap between a real multitrack and an AI-separated stem is where bleed and artifacts come from.

### Music source separation {#music-source-separation}

The technical field focused on isolating individual audio sources from a mixed recording. Stem splitting is a practical application of music source separation research. The field draws on signal processing, machine learning, and psychoacoustics, and has advanced significantly since the introduction of deep learning approaches. [Wikipedia's article on music source separation](https://en.wikipedia.org/wiki/Music_source_separation) provides a useful overview of the history and methodology.

### Online stem splitter {#online-stem-splitter}

A browser-based tool that performs AI source separation without requiring any software installation. You upload a file, the processing runs on remote servers, and you download the resulting stems. [StemSplit.io](https://stemsplit.io) is a well-regarded example that handles common formats and produces consistent results on standard commercial material. Online tools are the most accessible option for most users; see [online vs desktop stem splitters]({{ "/online-vs-desktop-stem-splitters/" | relative_url }}) for a comparison with local tools.

### Other stem {#other-stem}

In a 4-stem separation model, the "other" stem captures everything that isn't vocals, drums, or bass. This typically includes guitars, keyboards, synths, strings, and any additional melodic or harmonic content. The catch-all nature of this stem makes it one of the harder ones to separate cleanly, since it encompasses a broad range of frequency content. See [4-stem vs 6-stem separation]({{ "/4-stem-vs-6-stem-separation/" | relative_url }}) for when it makes sense to break this stem down further.

### Remix {#remix}

A new version of a song, typically created by altering the arrangement, tempo, key, or instrumentation of the original. Stem splitters make unofficial remixing accessible by providing isolated components of a track that were never separately released. Common workflows include extracting a vocal stem and placing it over new production, or using drum and bass stems as the rhythmic foundation for a new arrangement. See [stem splitting for sampling and beatmaking]({{ "/stem-splitting-for-sampling-beatmaking/" | relative_url }}).

### Sample rate {#sample-rate}

The number of audio samples captured per second, measured in Hz or kHz. 44.1 kHz is CD standard; 48 kHz is common in video production; 96 kHz is used in high-resolution audio contexts. Higher sample rates capture more high-frequency detail but produce larger files. Stem splitters typically work at or convert to 44.1 kHz internally.

### Sampling {#sampling}

The practice of using a portion of one recording as an element in a new composition. Producers use stem splitters to isolate the specific part of a track they want to sample, such as a drum break, a bass riff, or a vocal hook, without other instruments bleeding into the sample. This produces a cleaner, more usable sample than cutting directly from the full mix. See [stem splitting for sampling and beatmaking]({{ "/stem-splitting-for-sampling-beatmaking/" | relative_url }}).

### Spectrogram {#spectrogram}

A visual representation of audio frequency content over time. The horizontal axis is time, the vertical axis is frequency, and brightness or color indicates amplitude at each point. Many source separation models operate on spectrograms rather than raw waveforms, treating the separation problem as an image masking task. HTDemucs operates in both the waveform and spectrogram domains simultaneously, which contributes to its quality advantage on complex material.

### Spleeter {#spleeter}

An open-source source separation library released by Deezer Research in 2019. Spleeter was one of the first widely accessible neural stem splitters, offering 2-stem, 4-stem, and 5-stem separation with a straightforward command-line interface. It remains useful for batch processing workflows and as a historical baseline, though it has been surpassed in output quality by newer models. See the [Spleeter GitHub repository](https://github.com/deezer/spleeter) for source and documentation, or the [Spleeter review]({{ "/spleeter-review/" | relative_url }}) for a current assessment.

### Stem {#stem}

A single isolated audio component extracted from a mixed recording. Common stems include vocals, drums, bass, and other instruments. The term comes from music production, where projects are often delivered as discrete elements for mixing or further processing. A "stem file" is the individual audio file containing that isolated component. See [what are audio stems]({{ "/what-are-audio-stems/" | relative_url }}).

### Stem splitter {#stem-splitter}

A tool that takes a mixed audio recording and separates it into individual component stems using AI-based source separation. Modern stem splitters are built on deep learning models like HTDemucs and MDX-Net. The [complete guide to stem splitting]({{ "/complete-guide-stem-splitting/" | relative_url }}) covers the full picture for anyone newer to the concept. See also: [how AI stem separation works]({{ "/how-ai-stem-separation-works/" | relative_url }}).

### STFT (Short-Time Fourier Transform) {#stft}

A mathematical technique that converts an audio signal into its frequency components across a series of short, overlapping time windows. The STFT is foundational to spectrogram-based audio processing and is used in many source separation pipelines as a way of representing audio in a form more amenable to neural network processing. The inverse STFT converts the processed frequency representation back into audio.

### VR Architecture {#vr-architecture}

Vocal Remover Architecture. A class of neural network designs optimized for separating vocal content from instrumentals. VR Architecture models are the basis for several tools within the Ultimate Vocal Remover application and are known for particularly clean vocal isolation on appropriate material. See the [UVR5 GitHub repository](https://github.com/Anjok07/ultimatevocalremovergui) for more information.

### Vocal isolation {#vocal-isolation}

The process of extracting the vocal stem from a mixed recording, leaving behind a clean instrumental version. Vocal isolation quality is one of the most frequently evaluated metrics for stem splitters because the results are audibly obvious. A clean vocal isolation has minimal instrument bleed and no audible processing artifacts on the voice. See [how to isolate vocals from a song]({{ "/how-to-isolate-vocals-from-a-song/" | relative_url }}).

### Vocal remover {#vocal-remover}

Often used interchangeably with "stem splitter" or "vocal isolator," though in practice it usually refers to tools focused specifically on the vocal/instrumental split rather than full multi-stem separation. Most vocal removers produce two outputs: a vocals stem and an accompaniment stem. See also: vocal isolation, karaoke track.

### Vocal stem {#vocal-stem}

The isolated audio file containing only the lead vocal from a mixed recording. It is one of the four standard outputs of a 4-stem separation, alongside drums, bass, and other. Vocal stems are used for remixing, karaoke creation, vocal analysis, pitch correction, and practice. The quality of the vocal stem depends heavily on the source material and the AI model used. See [how to isolate vocals from a song]({{ "/how-to-isolate-vocals-from-a-song/" | relative_url }}).

### WAV {#wav}

Waveform Audio File Format. An uncompressed audio format that stores raw audio data without any quality loss. WAV files are the standard format for professional audio work and for stem exports. Saving stems in WAV preserves the full quality of the separation output and avoids introducing compression artifacts into the downstream workflow.

---

For answers to common questions about stem splitting, see the [FAQ]({{ "/faq/" | relative_url }}). For a broader introduction to how all of this works, the [complete guide to stem splitting]({{ "/complete-guide-stem-splitting/" | relative_url }}) is the place to start.
