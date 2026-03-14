---
layout: post
title: "What Are Audio Stems? What Producers Mean When They Say Stems"
date: 2025-09-10
description: "Audio stems are individual instrument tracks separated from a finished mix. Here's what they are, where the term comes from, and why producers care."
tags: Guide
about_terms: [stem, stem-splitter, multitrack-recording]
mentions_terms: [bleed, vocal-stem, drum-stem, bass-stem, other-stem]
---

You've heard producers and engineers throw around the word "stems" but maybe you've never been entirely sure what it means, or whether it means the same thing to everyone using it. It doesn't always. The term gets used loosely, and that causes confusion.

Here's what stems actually are, where the concept comes from, and why the arrival of AI has completely changed who gets to work with them.

## The simple definition

A stem is a bounced audio file that contains a specific group of instruments from a song, mixed down together.

So instead of your full finished mix, you might have 4 stems: one with all the drums, one with the bass, one with the vocals and one with everything else. Each file is stereo (usually), full length, and sits in sync with the others. Stack all 4 back together and you get your original mix back, more or less.

That's it. Stems are not raw session files. They're not individual microphone channels. They're a practical middle layer between "here's the entire session with 200 tracks" and "here's the finished song."

## Where the word "stems" actually comes from

The term comes from mixing and mastering, where engineers have worked with grouped audio exports for decades.

Before AI, stems flowed outward from the studio. A producer finishing a track would bounce stems for the mastering engineer: a drum bus, a bass bus, a vocal bus, an instrumental bus. This gave the mastering engineer more control than a stereo mixdown would allow, without handing over the entire messy session.

Labels used stems for licensing and sync: when a TV show wants to use a song but might need a version without vocals, having the vocal stem separate makes that edit trivial. Film composers have always delivered stems to their music editors.

Broadcast facilities have long required stems from composers so they can remix levels for different formats: stereo TV, Dolby 5.1, streaming.

The word itself doesn't have a clean etymology, it's just become the industry shorthand for these grouped submixes. Some people call them "sub-mixes" or "bus recordings," but stems stuck.

## What stems look like in practice

In practice, getting 4 stems from a song means getting 4 audio files. If the original track is 3 minutes and 42 seconds, each stem is 3 minutes and 42 seconds. They're full stereo WAVs (or FLACs if someone compressed them losslessly).

Open them in any DAW and drop them onto 4 tracks at the zero point, and you've got the song rebuilt. Solo one track and you're listening to just that element.

The standard 4-stem breakdown is:

- Vocals
- Drums
- Bass
- Other (guitars, keys, synths, or whatever isn't covered by the first three)

Some deliverables go further: a film composer might hand over 12 or 15 stems covering every section of the orchestra separately. But for most music production purposes, 4 is the standard, and it maps closely to what AI stem splitters produce.

The "other" bucket is always a bit imprecise, it ends up containing guitars, pianos, synth pads, strings, and anything else that doesn't fit the first three categories. On a song with a complex arrangement, that can mean the "other" stem is still a busy, layered file rather than a clean solo instrument.

## The difference between stems and multitracks

This is where people sometimes get confused, because "stems" and "multitracks" get used interchangeably, but they're not the same thing.

Multitracks are the individual recorded channels: the kick microphone, the snare mic, the overhead mics, the DI bass, the three vocal takes, the reference guitar, all as separate files. A multitrack session might have 80 or 100 or 200 individual tracks.

Stems are a bounced subset of those multitracks. Someone took the 12 drum tracks and mixed them into a single stereo drum stem. The 6 guitar tracks became a single guitar stem. You've lost the ability to remix the individual elements within each group, but you've gained portability and manageability.

For most remix and production purposes, stems are more useful than raw multitracks, because the internal balances within each group are already set. The drum stem sounds like a coherent drum kit, not 12 separate mic channels you'd have to balance yourself.

## Why AI stem splitting changed things

Before AI, you needed the original session to get stems. If you wanted to remix a classic track from the 1970s, you were out of luck unless the record label had the multitracks in a vault somewhere and was willing to let you access them.

AI stem splitting inverts the whole relationship. You start with the finished stereo mix and work backward, extracting approximations of what the original stems sounded like. [How AI stem separation works]({{ '/how-ai-stem-separation-works/' | relative_url }}) gets into the technical detail, but the practical result is that you can now generate working stems from any song you have a recording of.

The quality isn't perfect. There's bleed between stems, meaning trace amounts of the drums might show up in the vocal stem, and some artifacts are unavoidable. But for most use cases, the separation is more than good enough, and the access it provides is genuinely new.

Any producer, for the first time, can extract a vocal from a song they didn't make. Any musician can isolate the bassline from a track they're learning. Any DJ can get a cappella versions of songs that never had official releases. Tools like [StemSplit.io](https://stemsplit.io) make this accessible without any installation or technical setup.

[The complete guide to stem splitting]({{ '/complete-guide-stem-splitting/' | relative_url }}) covers the full landscape of tools and use cases. If you're specifically looking to work with stems in a DAW, [bringing stems into your DAW]({{ '/using-stems-in-your-daw/' | relative_url }}) covers the practical workflow.

The underlying technology draws on decades of academic research in [stem separation](https://en.wikipedia.org/wiki/Stem_(audio)#Stem_separation), but it's the recent deep learning approaches, especially Meta AI's [Demucs project](/tools/#demucs), that pushed quality to the point where these tools became actually useful for everyday music production.
