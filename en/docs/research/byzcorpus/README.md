# ByzCorpus — Byzantine chant symbolic corpus and research toolkit

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../docs/research/byzcorpus/README.md) · **English**
<!-- language-switch:end -->

[Home](../../../README.md) · [Core research summary](../../start/research-summary.md) · [Preliminary inventory](../corpus/README.md) · [Data model (Greek)](../../../../docs/research/byzcorpus/data-model.md) · [Segmentation pilot (Greek)](../../../../docs/research/byzcorpus/segmentation-pilot.md) · [Roadmap (Greek)](../../../../docs/research/byzcorpus/roadmap.md)

> **Status: research planning, 6 November 2026.** “ByzCorpus” is a provisional project name. This page documents a work in progress: no corpus release, validated model performance, public toolkit or external research partnership is claimed.

## Purpose

**ByzCorpus** is a proposed reproducible infrastructure for symbolic Byzantine chant data. It aims to link complete compositions and source witnesses with New Method notation, atomic melodic events, text and prosody, position annotations and explicitly documented historical relations. Data distribution will be determined by source-specific rights and permissions.

Two connected workstreams are being designed:

1. **A versioned symbolic corpus and Python toolkit:** import (including Neanes where available), validation, provenance, notation–event correspondence, searchable metadata and MIR exports.
2. **A Byzantine segmentability pilot:** application of unsupervised statistical segmentation, including the Nested Hierarchical Pitman–Yor Language Model (NHPYLM) studied by Lanz and Hajič (2025), to continuous Byzantine melodies. The key comparison is with independently justified musicological position boundaries and, where available, position-family identities.

The project can support the **PE0/PE1 data infrastructure** and M1 of the PhD proposal. The segmentation pilot is a separately scoped exploratory study. The approved M1 rule J, its fixed architecture A for representation selection, A2, and M2/EISE remain unchanged.

## Current evidence and dependencies

The [preliminary inventory](../corpus/README.md) based on Gheorghiță (2009) contains metadata on 42 Sunday Koinonika, 11 melodic formations and 338 rows from 68 tables. Of these rows, 35 have undergone visual verification while 303 retain an `OCR_DRAFT` flag. They locate candidate passages, rather than providing continuous symbolic scores.

The St Anthony's *Papadic Formulae* catalogue, drawing on 758 compositions in the current proposal, supports the discovery of candidate occurrences and families. Full works and validated musicological annotations still need to be acquired, encoded and independently reviewed.

## Proposed data structure

The model distinguishes **work, source witness, transcription, written symbol, atomic melodic event, text alignment, segment occurrence, family specification and historical relation**. Each element requires stable IDs, verification status and provenance. Data licences, executable code licences and permissions for transcriptions are assessed separately.

The main initial tasks are: a source-and-rights inventory; a small set of complete, legally usable scores; validation of symbol-to-event mapping; a first data schema; and reproducible segmentation baselines with independent musical review.

## Research relevance

The project connects the generative melodic-chunk account of **Mavromatis (2005)**, text and modal leakage controls from **Lanz & Hajič (2023)**, and memory-efficient NHPYLM segmentation from **Lanz & Hajič (2025)**. An open question is whether statistically efficient chunks align with complete Byzantine positions or with smaller internal components, especially in melismatic chant.

An exploratory discussion with Dr Jan Hajič Jr is scheduled for **23 November 2026**. Potential collaboration is a topic for discussion and has not been agreed.

## Working documents

- [Proposed data model and provenance rules (Greek)](../../../../docs/research/byzcorpus/data-model.md)
- [Proposed Byzantine NHPYLM / segmentability pilot (Greek)](../../../../docs/research/byzcorpus/segmentation-pilot.md)
- [Roadmap, gates and decision log (Greek)](../../../../docs/research/byzcorpus/roadmap.md)
- [Current M1 representation decision](../m1-selection-decision.md)
- [A2 knowledge design](../a2-knowledge-design.md)
- [M2/EISE research design](../m2-eise-research-design.md)

Technical documents will be translated incrementally as their content stabilises.
