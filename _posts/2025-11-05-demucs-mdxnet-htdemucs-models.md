---
layout: post
title: "Demucs, MDX-Net, and HTDemucs: The AI Models That Power Stem Splitters"
date: 2025-11-05
description: "Most stem splitters use the same handful of AI models. Here's what Demucs, MDX-Net, and HTDemucs actually are and how they differ."
---

There are dozens of stem splitter apps, websites, and plugins out there. Most of them are running the same handful of AI models underneath. The app name on the label matters a lot less than which model is actually doing the work.

Understanding the models helps you make better choices about which tools to trust, what quality to expect, and why different tools sometimes produce very different results on the same track.

## Why the model matters more than the app name

[Music source separation](https://en.wikipedia.org/wiki/Music_source_separation) as a field is largely built on open-source research. The major models, Demucs, MDX-Net, HTDemucs, and the VR Architecture variants, are all publicly available. Any developer can build an application on top of them, and many do.

This means two apps that look totally different on the surface might be producing identical outputs. Conversely, two apps that look similar might be using different model versions or fine-tunes that produce noticeably different quality.

When you're comparing stem splitters, ask which model they're using. If they don't tell you, that's worth knowing too.

The [complete guide to stem splitting]({{ "/complete-guide-stem-splitting/" | relative_url }}) covers how these tools fit into broader workflows. But if you want to understand what's actually happening under the hood, the models are where to start. The [how AI stem separation works]({{ "/how-ai-stem-separation-works/" | relative_url }}) post goes into the underlying mechanics in more detail.

## Where Demucs came from

Demucs was published by [Meta AI (Facebook Research) in 2019](https://github.com/facebookresearch/demucs). It was one of the first deep learning models specifically designed for music source separation to achieve competitive results against older signal-processing approaches.

The original Demucs architecture is a U-Net-based model that works directly in the waveform domain. It takes raw audio as input and outputs raw audio for each stem, no intermediate frequency conversion. That time-domain approach was somewhat novel at the time and gave Demucs a particular character: generally good transient handling, which matters a lot for drums and percussion.

The benchmark dataset for this field is MUSDB18, a collection of 150 multi-track songs with ground-truth stems. SDR (Signal-to-Distortion Ratio) is the standard metric, measuring in decibels how well an estimated stem matches the original isolated source. Higher SDR means cleaner separation. Original Demucs scored competitively on MUSDB18 when it launched, and it established Meta AI as a serious player in the separation space.

## What MDX-Net was built to solve

MDX-Net came out of the [2021 Sony Music Demixing Challenge](https://arxiv.org/abs/2111.03600), a competition specifically designed to push the state of music source separation forward. The challenge produced several architectures, and MDX-Net was among the strongest performers.

Where Demucs worked in the time domain, MDX-Net takes a different approach: it operates on spectrograms. A spectrogram is a visual representation of audio frequency content over time, and it turns out that modeling frequency patterns can be very effective for separating instruments that occupy distinct spectral regions.

MDX-Net's architecture processes the complex spectrogram of a mixed signal and estimates masks for each source. The masks are then applied to recover the individual stems. This spectral approach gives MDX-Net some particular strengths: it tends to handle cases where instruments are spectrally separated fairly cleanly, and it often performs well on instrumental stems where the frequency structure is more predictable.

One limitation: purely spectrogram-based models can sometimes produce metallic or "phasey" artifacts, especially on transients. This is a known trade-off of the spectral approach and part of why hybrid models became the next step.

## HTDemucs: the current standard

HTDemucs, published in 2022 and detailed in the [accompanying academic paper](https://arxiv.org/abs/2111.03600), is the model that most serious tools use today. It's a hybrid domain model, meaning it processes audio in both the time domain (like original Demucs) and the frequency domain (like MDX-Net) simultaneously, then combines those estimates.

The architecture splits processing into two parallel streams. A waveform encoder handles the time-domain pass, capturing transients and temporal structure. A spectrogram encoder handles the frequency-domain pass, capturing spectral patterns. A cross-domain transformer then allows these two streams to exchange information, so the model can use time-domain context to inform spectral decisions and vice versa.

The result is a meaningful improvement in SDR scores over the original Demucs across all four stems on MUSDB18. The gains are particularly notable on bass and "other" (non-rhythmic instruments), which benefited from the combined time and frequency perspective.

HTDemucs is open source and available via the [Demucs GitHub repository](https://github.com/facebookresearch/demucs) alongside the original models.

## Which model handles what best

This is where it gets practical. Not every model is equally good at every stem.

**HTDemucs** is the best general-purpose choice. If you're doing a 4-stem separation and you want the best overall quality across vocals, drums, bass, and other, HTDemucs is typically the right model. It's not always the top performer on every individual stem in isolation, but it's consistently strong.

**MDX-Net** has a reputation for doing well on instrumental separation specifically, and some practitioners prefer it for producing the cleanest accompaniment track (everything minus vocals). For karaoke production or acapella extraction, it's worth testing against HTDemucs to see which sounds cleaner on your specific material.

**VR Architecture models** (popularized through [UVR5](https://github.com/Anjok07/ultimatevocalremovergui)) are a separate family worth knowing about. These are often used for vocal isolation specifically, and fine-tuned versions of VR Architecture models perform very well on clean, mastered pop material. If your primary goal is getting the cleanest possible vocal stem from a commercially released track, a VR Architecture model might outperform HTDemucs on that specific task.

The [artifacts and bleed post]({{ "/stem-splitter-artifacts-bleed/" | relative_url }}) covers why no model produces perfect results, regardless of architecture.

## Why most web tools don't let you choose

If you're using a typical web-based stem splitter, you're probably not choosing your model. The app picks one for you, often a fine-tuned version they've optimized internally or simply the best-available open-source checkpoint at the time they built the product.

Fine-tuned models are trained variants that start from a base architecture (like HTDemucs) and then get additional training on curated data to improve performance on specific use cases. A tool might use "HTDemucs fine-tuned for vocals" or a proprietary model trained on their own dataset, and they may not disclose which.

That opacity is frustrating if you're trying to understand what you're actually running. Tools that do expose model selection, like the desktop application UVR5, give you the most control. For most users, the practical answer is to test a few tools on a track you know well and listen for which produces the fewest artifacts on the stems you care about.

The [FAQ]({{ "/faq/" | relative_url }}) covers common questions about model selection and which tools give you the most control.

## What this means for your workflow

If you're using a web tool and it works well for your material, don't overthink the model question. The output quality matters more than the architecture label.

If you're getting artifacts or bleed that bothers you, and especially if you're doing critical work like audio restoration or sample-accurate editing, it's worth experimenting with different models. UVR5 on desktop gives you access to the full range of architectures and checkpoints. For quick online separation on most material, tools running HTDemucs are the reliable default.

The field is still moving fast. HTDemucs represents the current consensus best practice, but new models and fine-tunes are published regularly, and the gap between what's possible and what most web tools offer is usually a few months behind the research frontier.
