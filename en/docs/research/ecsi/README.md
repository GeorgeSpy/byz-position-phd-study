# ECSI — Musicologically Grounded Signatures for Melodic Formula Families

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../docs/research/ecsi/README.md) · **English**
<!-- language-switch:end -->

**Independent research direction · Status: research design and exploratory phases P0′–P2′**

[English research proposal homepage](../../../README.md) · [Musicological foundations (Greek)](../../../../docs/musicology/index.md) · [Mthesis](../../current/m-thesis.md) · [EISE (Greek)](../../../../docs/full/06-eise.md) · [ATL](../../current/atl.md)

## Research programme and methodological contribution

How does a Byzantine melodic formula (*thesis*) retain its identity across distinct historical and modal realisations? How can a model use **the structure of musicological knowledge itself**—rather than only labels or isolated features—to recognise this identity while preserving information about its particular melodic realisation?

**ECSI** (*Evidence-Conditioned Selective Invariance*) develops a testable framework of **Musicology-Informed Machine Learning (MIML)** for symbolic **Music Information Retrieval (MIR)**. Its central methodological step is to move beyond supervising individual musical concepts towards **compiling explicitly documented family signatures into probabilistic events for formula recognition**.

The proposed contribution has three connected components:

1. **A musicologically grounded family signature** (`σ_F`). Numbered source-based claims are connected to required and supporting diagnostic relationships, rules for the active modal context, alternative sufficient branches, and explicit exclusion criteria. Family identity is distinguished from historical correspondence of a local passage, co-exegesis, and copying dependencies between sources. Chrysanthos's *parakalesma* (`408) is a **candidate for direct examination of the primary source**, not an already validated signature.
2. **The probabilistic ECSI-D architecture.** A shared learning backbone estimates a dependent distribution of diagnostic variables, `q_θ(z|x,c)`. The family signature is compiled into an admissible set `S_F(c)`, and its probability `m_F(x,c)` is computed as the exact union of sufficient branches, counting overlaps only once. A distinct observation model represents expert judgements, while a separate `v` branch retains information about variability among realisations. Scores across candidate families use an explicit reference distribution and **calibration to be tested empirically**, rather than an assumed Bayesian interpretation.
3. **A controlled knowledge–learning experiment.** The sequence `P0′ → P1′ → P2′` begins with seven inventory measures (`μ1–μ7`), continues with source-backed compiler dossiers, and culminates in a 2×2 design (valid versus perturbed knowledge × structured versus flat use). ECSI-D is compared with the factored **ECSI-F** variant and a strong **B★** baseline (SupCon + family prototypes + matched concept supervision + the same `v` branch). Evaluation targets difficult recognition cases and preservation of realisation information under predeclared decision gates.

## Relationship to the research proposal

ECSI is an **independent extension** of the melodic-formula research programme, with its own hypotheses, estimands, and protected evaluation sets. It shares representation and source-provenance infrastructure but leaves unchanged **Studies M1–M5**, the **B2–EISE** comparison and `Δ_hist`, **analysis A2 of M2**, the performance-related `Γ_F`, and the separate **Mthesis**, **ATL**, and **ATL-INV** research tracks.

## Evidence and current status

The completed checks concern **synthetic examples and algorithmic correctness**: 63 legacy checks (62 passing, one known expected N5 scale-related failure) and 22 newer checks (22 passing). No fully validated musicological family-signature cards or confirmatory ECSI-D training on an independent Byzantine music corpus have yet been reported. A general machine-learning theorem on concept identifiability remains an **open research objective**.

## Documentation

- [01 — Research question, ontology, and relationship to M1–M5](01-research-question.md)
- [02 — ECSI-D architecture and probabilistic formulation](02-architecture.md)
- [03 — Protocol P0′–P2′, gates, and comparators](03-methods-and-gates.md)
- [04 — Design decisions, assumptions, and revision criteria](04-decisions.md)
- [05 — Evidence, reproducibility, and outstanding work](05-evidence-and-limitations.md)
- [06 — Relevant scientific literature](06-bibliography.md)
- [07 — Research roadmap and prospective publications](07-publication-roadmap.md)
- [Family-signature card template (JSON)](signature-card-template.json)
