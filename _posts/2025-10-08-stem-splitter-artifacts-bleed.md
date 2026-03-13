---
layout: post
title: "Why Stem Splitters Aren't Perfect: Bleed, Artifacts, and What Causes Them"
date: 2025-10-08
description: "Stem splitters produce bleed and artifacts because of frequency overlap. Here's what causes these problems and when they matter most."
---

If you've run a track through a stem splitter and noticed that the vocal stem has a faint hi-hat in it, or the drum stem has a ghost of the bass guitar, you've encountered bleed. It's not a glitch, it's not a sign of a broken tool, and it doesn't mean the technology doesn't work. It's an inherent byproduct of what the AI is actually doing.

Understanding why bleed happens changes how you work with stems. You stop expecting perfection and start knowing exactly what to expect from different types of material.

## What bleed actually is

Bleed is when audio from one stem shows up faintly in another.

The most common example: you isolate the vocals from a track, and underneath the singing you can hear a faint shimmer of hi-hats. Or you pull out the drums, and there's a low-frequency murmur of bass guitar running through the kick hits. Or the "other" stem (guitars and synths) has a shadow of the lead vocal ghosting through it.

It's rarely loud enough to be obtrusive. Usually it's quiet, like listening through a wall, but it's there, and depending on what you're trying to do with the stems it can range from completely irrelevant to genuinely frustrating.

The other category of problem is artifacts: digital glitches, warbling or "phasing" sounds, metallic smearing in the frequency content, or a quality that sounds processed rather than natural. Artifacts happen when the model's reconstruction of a stem diverges from what the original source actually sounded like.

Both problems come from the same root cause.

## Why frequency overlap is the root cause

When a kick drum hits, most of its energy is in the low frequencies, say 60-150Hz for the body of the hit, with some click up around 3-4kHz for the attack. A bass guitar note sits in roughly 80-250Hz. These ranges overlap.

In the spectrogram that the AI analyzes, the kick and the bass guitar are fighting over the same frequency territory at the same moments in time. The model has to make a decision: does this particular block of low-frequency energy belong to the kick stem or the bass stem? In a well-produced electronic track where the kick and bass are sidechain-compressed to duck against each other, that decision is easier. In a live jazz recording where the upright bass and kick drum ring out together, it's much harder.

Vocals live mostly in the 300Hz-3kHz range. So do acoustic guitars, piano, snare drums, horns, and dozens of other instruments. Reverb tails from the snare spread across the whole frequency spectrum including the vocal range. Any instrument that shares frequency space with another creates the potential for bleed in both directions.

The AI can't separate what physics mixed together. It can only make its best statistical guess about which frequencies belonged to which source, and those guesses are imperfect.

## When you'll notice it most

Dense arrangements are the worst case. A full band recording with drums, bass, 2 guitars, keyboards and vocals, all playing simultaneously, means every stem has more potential bleed sources competing for the same frequency space.

Live recordings compound the problem because microphone bleed was already baked in before mixing. The vocal mic captured drum room sound. The guitar amp was in the same room as the drums. That physical bleed got mixed into the final track, and the AI can't retroactively un-mix what was never separated to begin with.

Acoustic music, folk, classical, singer-songwriter, tends to be harder than produced music for exactly this reason. There's no multiband compression squashing each element into a defined zone. Everything rings naturally and bleeds into the natural reverb of the recording space.

Electronic music and well-produced modern pop are the easiest cases. Producers of that music often make deliberate spectral arrangement choices (high-pass the bass here, low-cut the synth pad there) that create cleaner separation between instruments in frequency space. Those decisions help the AI enormously.

Heavily distorted guitars are a specific nightmare, distortion spreads harmonic content across enormous frequency ranges and makes guitar almost impossible to cleanly isolate.

## What the AI gets wrong and why

The model was trained on MUSDB18, a dataset of 150 songs with ground-truth stems, mostly contemporary pop and indie music. That training distribution shapes what the model is good at and what it isn't.

If a recording sounds like the typical studio pop or rock it trained on, the model's priors are well-calibrated. It knows roughly what a rock vocal sounds like, what a recorded drum kit sounds like, what a DI bass sounds like.

When you throw at it something far outside that distribution, a 1960s soul recording with a different mixing aesthetic, a death metal track with extreme saturation, an orchestral film score, the model's learned expectations don't match reality as well. The guesses get worse.

This is why model choice matters. Different models (Demucs, MDX-Net, and their variants) have different training histories and different strengths on different material. Using the wrong model for your genre isn't just suboptimal, it can produce noticeably worse output, and the model selection post goes into this in detail.

There's also an irreducible limitation: the problem is mathematically underdetermined. Given just the stereo mix, multiple valid reconstructions of the underlying sources could have produced it. The AI picks the most statistically likely one. On unusual material, "most statistically likely" might still be wrong.

## How to work around the worst of it

You're not going to eliminate bleed entirely. But you can minimize it and work with it rather than against it.

**Choose the right model.** HTDemucs is the current best general-purpose option for most material. But for certain use cases, fine-tuned variants of MDX-Net outperform it on vocals specifically. Running the same track through 2 different models and comparing is a legitimate strategy, it doesn't take long and the difference is sometimes significant. Tools like [UVR5 (Ultimate Vocal Remover)](https://github.com/Anjok07/ultimatevocalremovergui) let you do exactly this with fine-grained model control.

**Use higher stem counts when isolation matters.** Going from 4 stems to 6 stems forces the model to separate guitar and piano from the "other" bucket, which can reduce bleed in all the stems because the model is working with more specific targets. See [4-stem vs 6-stem separation]({{ '/4-stem-vs-6-stem-separation/' | relative_url }}) for when this is actually worth doing.

**Work with the bleed rather than against it.** For karaoke and practice purposes, a faint hi-hat in the vocal stem doesn't matter. For sampling a bassline, trace amounts of kick bleed into the bass stem might actually help the groove feel right. Bleed only becomes a real problem when you need pristine isolation, which is a narrower set of use cases than it might initially seem.

**Use EQ to manage what remains.** If the drum stem has low-frequency bass bleed, a high-pass filter at 200Hz will clean it up without hurting the kick much. If the vocal stem has high-frequency cymbal shimmer, careful EQ in the 6-12kHz range can reduce it. This takes time, but it's a faster path to clean stems than running the separation repeatedly hoping for a better result.

**Accept that some material just doesn't separate well.** Live recordings of acoustic instruments through a single microphone, music with extreme reverb as a production aesthetic, heavily layered choral arrangements: these are genuinely hard cases where no current tool will give you clean stems. That's not a failure of the technology, it's the current state of what's physically possible.

The [complete guide to stem splitting]({{ '/complete-guide-stem-splitting/' | relative_url }}) covers what to expect from different genres more broadly, and [how AI stem separation works]({{ '/how-ai-stem-separation-works/' | relative_url }}) explains the frequency overlap problem in more technical detail if you want the full picture.

For specific questions about stem separation quality and use cases, the [FAQ]({{ '/faq/' | relative_url }}) covers the most common ones directly.

This stuff has real limits. Knowing them upfront means you use it effectively rather than getting frustrated, and the quality on material it handles well is genuinely good enough for most production purposes.
