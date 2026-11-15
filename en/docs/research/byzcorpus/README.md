# ByzCorpus — Symbolic Corpus of Byzantine Chant and Research Toolkit

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../docs/research/byzcorpus/README.md) · **English**
<!-- language-switch:end -->

[Home](../../../README.md) · [Core research summary](../../start/research-summary.md) · [Preliminary inventory](../corpus/README.md) · [Data model (Greek)](../../../../docs/research/byzcorpus/data-model.md) · **[Expert-boundary pilot (English)](expert-boundary-pilot.md)** · [NHPYLM follow-up (Greek)](../../../../docs/research/byzcorpus/segmentation-pilot.md) · [Comparative pilot study](gregorian-nhpylm-helsen-pilot.md) · [Roadmap (Greek)](../../../../docs/research/byzcorpus/roadmap.md) · [Melodic segmentation and formula-family recognition](segmentation-and-family-recognition/README.md)

> **Status: Research direction under development and feasibility assessment · 7 November 2026.** **ByzCorpus** organises the design of symbolic data, Python research tooling and melodic segmentation experiments. The current release comprises specifications, protocols and a roadmap. Datasets and software will be released incrementally following quality and rights reviews.

## 1. Purpose

**ByzCorpus** is designed as a controlled, reproducible infrastructure for symbolic Byzantine chant data. It links complete works, specific musical witnesses, neumatic notation, elementary melodic events, text, melodic-segment annotations and historically documented relationships. Access to and publication of each layer are governed by the rights of the respective sources.

The work is organised into two connected directions:

1. **Symbolic corpus and Python toolkit.** Import of works (prioritising *Neanes* files where available), conversion and provenance verification, searchable metadata and standardised exports for Symbolic Music Information Retrieval (Symbolic MIR).
2. **Pilot study on melodic segmentation.** Application and evaluation of unsupervised segmentation methods—including the Nested Hierarchical Pitman–Yor Language Model (NHPYLM) as applied by Lanz and Hajič (2025)—on symbolic Byzantine melodies.

**ByzCorpus** constitutes a self-contained research direction for data infrastructure and Symbolic MIR. The infrastructure may support work packages **PE0/PE1 and study M1** of the research proposal, while the comparative study of segmentation across chant traditions maintains independent research questions and metrics. Study M1, the representation selection rule (J), study A2 and M2/EISE retain their established protocols.

## 2. Current state and remaining work

**Available documentation:** the [preliminary inventory](../corpus/README.md) based on Gheorghiță (2009) records metadata for 42 Sunday Koinonika, 11 formations and 338 inventory entries across 68 tables. Of these entries, 35 have been visually verified while 303 carry the `OCR_DRAFT` flag. The inventory locates candidate passages and sources; it does not constitute a corpus of continuous symbolic melodies.

The [Karagkounis (2003, 2005) inventory](../corpus/karagkounis-2003-2005.md) adds 933 Cherubic hymn catalogue entries, including 243 in the new-composition period from 1814 to the late nineteenth century, and 206 named-position catalogue references. The two historical strata and the pending work-level matching with St. Anthony's Monastery *Papadic Formulae* are documented separately. These are source-selection and musicological metadata; continuous symbolic encoding is a subsequent phase.

The *Papadic Formulae* catalogue of St Anthony's Monastery serves as a source for locating candidate occurrences and formula families drawn from 758 compositions, as described in the [active research summary](../../start/research-summary.md). The catalogued types require cross-checking against complete works and independent musicological annotation.

**Required tasks:** rights clearance, selection of initial complete works, digital encoding, certification of symbolic conversion, documentation of source relationships, independent annotation and a reproducible experimental pipeline. No specific count of completed Byzantine symbolic encodings or executed NHPYLM training runs on Byzantine material is claimed at present. The [comparative pilot study](gregorian-nhpylm-helsen-pilot.md) reports a completed Gregorian experiment alongside the design of the Byzantine application.

## 3. Ontology and scope of use

The infrastructure mandatorily distinguishes **work**, **witness/source**, **digital transcription (score)**, **written symbol**, **elementary melodic event**, **segment occurrence**, **formula family (*thesis* family)**, **musicological specification** and **historical relationship**. Relationship types carry distinct source documentation and verification status.

A *thesis* as a musicologically recognisable unit is distinguished from a model's statistical segment; their relationship is **the object of empirical testing**. See [Position and family (Greek)](../../../../docs/current/position-and-family.md) and the [data model (Greek)](../../../../docs/research/byzcorpus/data-model.md).

## 4. Structure of the research infrastructure

- **ByzCorpus:** versioned releases of eligible symbolic data, persistent identifiers, metadata and documented annotations.
- **Python toolkit (name to be finalised):** *Neanes* validator/converter, import/export routines, search functionality and quality-control utilities.
- **Byzantine melodic segmentation pilot:** reproducible baseline methods (n-grams, syllabic boundaries) and NHPYLM models, evaluated against musicological criteria adapted to the Byzantine tradition.
- **Potential interoperability:** evaluation of relevant principles from CantusCorpus/PyCantus and symbolic processing workflows, while fully preserving the distinctive characteristics of Byzantine notation.

ByzCorpus is initially developed **within the proposal repository as documentation**. A standalone code or data repository will be considered once executable, validated material and an agreed publication policy are in place.

## 5. Research questions

**RQ-C1 — Representation:** What minimal data schema permits bidirectional linking between melodic events, written symbols, text and source witness without losing critical information of Byzantine notation?

**RQ-C2 — Segmentability:** What segments do statistical models induce on complete Byzantine melodies, and how do these relate to musicologically accepted *thesis* boundaries?

**RQ-C3 — Unit scale:** Do induced short subsequences form structural constituents of larger *theseis*, particularly in extensive melismatic works?

**RQ-C4 — Contextual information:** How does segmentation change when textual, modal (*echos*) and graphic-grouping cues are present versus absent, under appropriate controls for information leakage?

Answering these questions requires sufficient symbolic data and independent musicological evaluation. These modules are not presented as newly approved branches of the dissertation.

## 6. Scientific precedents and exploratory scope

The dissertation of Mavromatis (2005), the published studies of Lanz and Hajič on Gregorian segmentation (DLfM 2023; ISMIR 2025), and the CantusCorpus/PyCantus infrastructure (2026) provide bibliographic and technical precedents. In Mavromatis (2005), *chunks* are analytically identified within alternative melodic realisations generated by an HMM for a fixed textual phrase, and their organisation is described in terms of decision points; musical examples are presented in staff transcription (§2.1, n. 5, printed p. 19 / PDF p. 30), while the HMM input is a sequence of note events carrying syllable stress, duration, diatonic interval, diatonic degree and a chromatic number in sixths of a whole tone (Appendix A, pp. 101–102 / PDF pp. 112–113; Table C.1, p. 161 / PDF p. 172). Neume identity, qualitative signs, *martyriai*, *phthorai* and neume groupings are not fields of the computational symbol. The proposed ByzCorpus schema preserves these layers linked to the source and accompanied by verified neume-to-event alignment, allowing their effect to be tested empirically via controlled projections onto the same event axis. ByzCorpus independently investigates how statistically induced segments relate to musicologically recognisable units in Byzantine chant.

Two central open questions are: (a) *how statistically induced melodic segments relate to the structural units of each chant tradition*, and (b) *which elements of a Byzantine symbolic schema can interoperate with established digital-musicology tools*. Source selection, schema finalisation and independent evaluation constitute the next stages.

## 7. Navigation and next steps

**Recent design decision (6 November 2026).** Following an independent technical review, the first comparative study is organised as a [feasibility pilot of independent expert boundary annotation](expert-boundary-pilot.md), incorporating explicit per-specialist coverage masks, recorded abstentions, agreement measured within jointly examined regions and textual controls. **Revision of 7 November 2026:** the Byzantine Phase B is self-contained, while the Gregorian Phase G is designed separately. Mandatory selective-abstention diagnostics and a separate textual field `E′` are added. The exploratory [NHPYLM pilot study (Greek)](../../../../docs/research/byzcorpus/segmentation-pilot.md) remains the next computational stage.

- [Data model, provenance and rights (Greek)](../../../../docs/research/byzcorpus/data-model.md)
- [First exploratory study of expert agreement](expert-boundary-pilot.md)
- [Segmentation research plan and NHPYLM (Greek)](../../../../docs/research/byzcorpus/segmentation-pilot.md)
- [Comparative pilot study: Gregorian and Byzantine chant](gregorian-nhpylm-helsen-pilot.md)
- [Roadmap, readiness criteria and open decisions (Greek)](../../../../docs/research/byzcorpus/roadmap.md)
- [Inventory of available historical metadata](../corpus/README.md)
- [M1 — rule J and evaluation](../m1-selection-decision.md)
- [A2 — musicological knowledge](../a2-knowledge-design.md)
- [M2/EISE — historical supervision](../m2-eise-research-design.md)

**Maintenance principle:** every new data entry is accompanied by a verification status, source identifier, usage licence and conversion version. Every new design decision is logged in the [roadmap (Greek)](../../../../docs/research/byzcorpus/roadmap.md), distinctly from the core research proposal. Any remaining Greek-only technical documents will be translated incrementally as their content stabilises.

## Melodic segmentation and formula-family recognition

The [research section](segmentation-and-family-recognition/README.md) documents comparisons between complete-*thesis* and subsegment-composition models, the use of multiscale boundary information, family-specific terms and the experimental protocol for Byzantine works. Synthetic and comparative Gregorian results are reported with explicit indication of their evidential status.
