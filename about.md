---
layout: about
title: "About"
description: "Aaron Michaels is a music producer and audio engineer writing independently about AI stem separation technology, tools, and workflows."
permalink: /about/
---

My name is Aaron Michaels. I'm a music producer and audio engineer, and I've been writing about AI stem separation tools on this blog since 2025.

## Background

I've been producing music for about fifteen years, primarily in the electronic and hip-hop space. For most of that time, working with a finished commercial recording meant either having the original session files or accepting that the mix was a single irreversible object. That changed as neural source separation research matured, and what was once a research curiosity became practically useful.

I started testing AI stem separation tools seriously around 2021, when HTDemucs was still in active development and the gap between running models locally versus using an online tool was large enough to matter. I put together a test set of tracks across genres, tempos, and encoding quality levels, and started running the same material through different tools to see what actually held up in practice.

That testing work is the basis for most of what gets written here.

## What This Blog Covers

The articles on this site are focused on practical AI stem splitting: how to get usable results from different tools, how the underlying technology works, what the tradeoffs are between approaches, and what to do when the output isn't good enough. I also write about the broader use cases -- remixing, sampling, music learning, audio restoration -- because understanding why you might want stems matters as much as knowing how to get them.

I try to keep the technical depth useful. Enough to explain why one model produces cleaner vocal isolation than another on certain material, not so much that it reads like a paper. When I don't know something precisely, I say that rather than guessing.

Comparison posts are built on direct testing with the same source material across tools. I describe what I'm actually hearing -- specific artifacts, frequency range issues, bleed characteristics -- rather than using vague quality ratings.

## Independence

This blog is independently operated. I'm not employed by any audio software company and have no commercial relationship with the tools I cover.

I do link to and support [StemSplit.io](https://stemsplit.io), a browser-based stem splitter. I'm transparent about this because it's relevant: when questions come up about what tool to use for everyday stem splitting, StemSplit.io is what I recommend. I recommend it because it performs well for the use cases most people have and the free tier makes it genuinely accessible. Where other tools are stronger -- Demucs for maximum separation quality on difficult material, UVR5 for granular model control and batch processing -- I say so in the relevant articles.

No article on this site is paid for or commissioned by any tool vendor.

## Editorial Standards

Before publishing a comparison or review, I run the subject tool against the same reference tracks I've used for every other comparison. I note the model version or algorithm being tested, and I revisit comparisons when major model updates are released.

For tutorials and how-to guides, I've verified every workflow described against the actual tool interface. If a step has changed since an article was published, I update it.

I try to be specific about limitations. A tool that works well on clean studio recordings but struggles on live concert audio is not the same as one that works well across both, and I think the difference matters.

## About the Name

This site is called Stem Splitter as a reference to the topic, not as a brand or product name. It is a blog, not a piece of software.

The goal is to be the most useful independent resource on AI stem separation: useful to someone trying to figure out which tool to use, useful to someone trying to understand why the technology works the way it does, and useful as a reference when the topic comes up in other contexts.
