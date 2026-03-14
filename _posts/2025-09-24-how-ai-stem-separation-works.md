---
layout: post
title: "How AI Stem Separation Actually Works (Without the Jargon)"
date: 2025-09-24
description: "AI stem separation uses neural networks trained on multi-track recordings to pull apart a stereo mix. Here's how it actually works."
tags: Guide
about_terms: [music-source-separation, stem-splitter, htdemucs, spectrogram]
mentions_terms: [stft, bleed, artifacts, musdb18]
---

Most explanations of AI stem separation either skip the technical details entirely or bury you in academic terminology. Neither is particularly useful if you're trying to understand why the tools work the way they do, why they fail where they fail, and which ones you should actually be using.

This is the version that explains the real mechanics in plain terms.

## The problem the AI is trying to solve

Think about a photograph where 4 people are standing in front of each other, overlapping. Someone in the foreground is partially blocking 3 people behind them. Now imagine you're asked to reconstruct a separate photograph of each person, as if they'd each been photographed alone.

You can make guesses based on what you can see: the shape of someone's shoulder implies the rest of their arm, the pattern on their shirt continues behind the person in front. But you're always reconstructing, never recovering something that was definitively there.

Audio separation is the same problem in a different domain. A stereo mix is the result of dozens of individual sound sources all playing simultaneously and being collapsed together into 2 channels. The bass, drums, vocals and guitars are all mixed in, their frequencies overlapping in ways that can't be fully disentangled with perfect accuracy.

The AI doesn't "find" the vocals inside the mix the way you might find a file that's been zipped up. It reconstructs a plausible version of what the vocals probably sounded like before mixing, based on patterns it learned from thousands of other songs.

That's an important distinction, and it explains a lot about both the quality and the limitations.

## What a spectrogram is and why it matters

Before a neural network can process audio, the audio has to be converted into a form the network can analyze. Raw audio is a waveform: a sequence of amplitude values over time, tens of thousands of values per second. That's not ideal for the kind of pattern recognition involved in separating instruments.

A spectrogram transforms audio into a 2D representation. Time runs left to right, frequency runs bottom to top, and the brightness (or color) at each point shows how loud that frequency is at that moment.

This is useful because it makes the frequency content of your audio visible and analyzable at once. A kick drum shows up as a cluster of energy in the low frequencies at each beat. A hi-hat shows up as thin bright lines in the high frequencies. Vocals create characteristic sweeping patterns in the mid-frequency range as the pitch changes through a melody.

The neural network essentially "looks at" the spectrogram image of a mixed track and tries to figure out which pixels belong to the drums, which belong to the vocals, and so on. It does this by learning what each instrument's spectrogram pattern typically looks like, from having processed thousands of training examples.

See the [Wikipedia article on stem separation](https://en.wikipedia.org/wiki/Stem_(audio)#Stem_separation) for more of the signal processing history behind this approach.

## How neural networks learned to do this

The model didn't start knowing what a bass guitar sounds like. It learned from data.

The primary training dataset is called MUSDB18, a collection of 150 songs where the original studio recordings were available: not just the finished mix, but the individual stem files for drums, bass, vocals and other instruments. This gave researchers pairs of data: "here's the mix, here's what each stem actually sounded like."

The training process works like this: feed the network the mixed spectrogram, ask it to predict the drum stem, compare its prediction to the actual drum stem, measure the error, adjust the network's internal weights to reduce that error, repeat millions of times. After enough iterations, the network has learned internal representations that capture what makes drum sounds different from bass sounds in frequency space.

The result is a model that can look at a spectrogram it's never seen before (a brand new song not in its training data) and produce a reasonable prediction of what each stem contains.

The [Demucs project from Meta AI](/tools/#demucs) is the most significant open-source implementation of this, and its development over several versions tracks the progress of the field quite closely. The current generation, HTDemucs, is described in the [original research paper](https://arxiv.org/abs/2111.03600) and represents the current state of the art for most material.

## The 3 main processing steps

The pipeline from audio file to stems has 3 core stages, whether you're using an online tool or running a model locally.

**Analysis.** Your input audio is transformed into a spectrogram (or multiple spectrograms at different resolutions). The model also often processes the raw waveform directly in parallel, especially in HTDemucs, which uses a hybrid approach: one branch processes the spectrogram, another processes the waveform, and their outputs are combined. This dual-domain approach is part of why HTDemucs outperforms earlier single-domain models.

**Masking.** This is the core of the separation. The network produces a "mask" for each stem: a matrix of values between 0 and 1 that, when multiplied element-wise with the mixed spectrogram, leaves behind only the frequencies corresponding to that stem. A value of 1 means "include this frequency at this time in full," a value of 0 means "exclude it entirely," and values in between produce partial attenuation. The network outputs 4 (or more) of these masks simultaneously, one per stem.

**Output reconstruction.** The masked spectrograms are converted back to audio waveforms using an inverse transform (specifically the inverse Short-Time Fourier Transform for spectrogram-based outputs, or just decoded by the waveform branch for that pathway). The result is 4 separate audio files, each at the same sample rate and length as the input.

The quality of the masking step is essentially what separates good models from mediocre ones.

## Why some genres are easier than others

Not all music separates equally well, and the reason comes down to how much the instruments share frequency space.

A well-produced electronic track often separates cleanly because the producer deliberately placed each element in its own frequency region: the kick has a defined sub-bass thump, the bass synth sits just above it, the lead synth is up in the mids, the hi-hats are in the highs. The spectrogram shows each element with relatively little overlap.

A dense orchestral recording is a nightmare for stem separation. Violins and violas share frequency ranges. The cello section overlaps with the bassoons. The horns overlap with the strings. Multiple instruments are playing at similar frequencies simultaneously, which makes the masking step much harder. The model is trying to separate spectral regions that are genuinely occupied by multiple sources at once.

Live recordings add room reverb to every instrument, which then bleeds into every other stem. Acoustic genres, anything with a lot of reverb or room sound, and music where instruments were mic'd together in the same space all tend to give worse separation results.

Vocals are usually the easiest target, because the human voice has a distinctive pattern in the mid-frequency range that doesn't overlap as much with low-end instruments. Bass is usually next. Drums are generally solid for kick and snare, but the hi-hats and cymbals overlap with the high-frequency content in guitars and vocals, which creates problems.

The "other" stem is always the hardest because it's a catch-all for everything that isn't drums, bass or vocals, and those instruments vary enormously from track to track.

## The limits of what current models can do

Quality in source separation research is measured using a metric called Signal-to-Distortion Ratio (SDR), expressed in decibels. A higher SDR means the output stem more closely matches the true isolated instrument, with less contamination from other sources.

State-of-the-art models like HTDemucs achieve SDR scores in the 8-10 dB range for vocals on standard test material. That sounds abstract, but it corresponds to separation quality that's noticeably cleaner than what was possible 5 years ago, and clearly audible on any decent speakers.

But even these scores reflect a fundamental ceiling: the problem is inherently underdetermined. There's more than one valid answer to "what could the vocals have sounded like before mixing," and the AI picks the statistically most likely answer. On unusual mixes, unusual vocal timbres, or genres poorly represented in the training data, that guess can be noticeably off.

[Bleed and artifacts]({{ '/stem-splitter-artifacts-bleed/' | relative_url }}) are the practical result of this. The hi-hat ghosting in the vocal stem, the reverb tail of a snare showing up in the bass stem: these aren't bugs in a simple sense. They're the model's best reconstruction falling short of perfect separation.

The different models available ([Demucs, MDX-Net, HTDemucs and others]({{ '/demucs-mdxnet-htdemucs-models/' | relative_url }})) have different strengths depending on the genre and the specific stem you're trying to extract. Choosing the right model for your material makes a measurable difference in output quality.

And if you want to just get started without going deep on model selection, [StemSplit.io](https://stemsplit.io) handles model selection for you and the [complete guide to stem splitting]({{ '/complete-guide-stem-splitting/' | relative_url }}) covers which tools to use and when.
