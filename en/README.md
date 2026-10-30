# The Byzantine Melodic Formula (*thesis*) as a Computational Unit

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../README.md) · **English** · [Translation progress](docs/translation-status.md)
<!-- language-switch:end -->

**PhD research proposal — Georgios Spyridakis**

[Research biography](docs/author/index.md) · [Prior work and public code (Greek)](../docs/author/prior-work.md) · [Unpublished manuscripts](../documents/prior-work/README.md)

> **Status (October 2026).** Proposal in preparation for the Department of Music Technology and Acoustics, Hellenic Mediterranean University; not yet submitted.

## The core research programme

**Central question:** how can a melodic formula and its family be recognised in continuous notation when the realisation varies, and what does the musicological knowledge that defines the family contribute to that recognition? The core is limited to three studies on a shared symbolic infrastructure:

- **M1 — Joint segmentation and recognition.** Boundaries and family are estimated together; input units of the notation and feature layers are compared.
- **A2 — The value of musicological knowledge.** Valid versus deliberately perturbed family specifications, used either additively or as structured logical constraints.
- **M2 — Identity and realisation.** Learning from occurrences of the same family without losing their variation; a historical strand using exegeses of the same passage, only where the sources allow it.

Evaluation rests on blind judgements by independent specialists (M3a). M5-min applies the final model to complete works held out from training. The core is deliberately limited so that it is feasible. The probabilistic operator Mθέσις, listening studies, performance timing, the full M5 and the comparison with Znamenny chant are designed as [conditional extensions](#conditional-extensions) that would broaden the core as far as data and sources allow.

**[Core research plan (Greek PDF)](../documents/core-research-plan.pdf)** — the current version; an English translation is in preparation. · [Earlier English short proposal (PDF)](../documents/short-proposal-en.pdf) · **Quick route:** [What is new](#what-is-new) → [Formula and family](docs/current/position-and-family.md#a-schematic-example) → [The inverse problem](docs/current/inverse-problem.md)

A **melodic formula** (*thesis*) is the historically grounded musical formation studied here. Its **family**, **occurrence** and **realisation** have distinct analytical roles. [Definitions](docs/current/position-and-family.md).

## What is new

The proposed research project examines **how a melodic formula retains its identity through variation and what exegeses transmit from older notation**. It connects these musicological questions with formula recognition in complete works and learning from documented historical relationships.

**For Byzantine musicology**

- **Which occurrences are “the same formula”?** It determines the scope of each family and the distinctions needed across mode, genre and form.
- **What remains stable, and what changes?** It locates written variation and examines its relationship with timing differences among contemporary chanters.
- **What do exegeses retain from older notation?** It measures which older notational distinctions can be recovered from analytical renderings and what exegetical practice adds beyond known rules.
- **How does Nikolaos of Smyrna differ?** It separates family selection from the particular ways families are realised, identifying the dimensions of his compositional individuality.

**For music information retrieval**

The new task combines formula localisation and recognition in continuous chant, with multiple acceptable boundary analyses and unknown families. Historically documented hard examples show when learned relatedness follows family identity beyond the metrophonic surface. Comparing input units and learning transformations determines which representation retains this musical knowledge.

**For machine learning**

The provenance of positive pairs becomes an experimental variable: common family labels are compared with verified exegeses of the same passage, using an independent performance criterion. Correct and perturbed knowledge are compared to examine what musicological content contributes and how it is used. Probabilistic models characterise a family's preferred realisations and the additional information provided by each historical source.

[What each study will teach us](docs/review/knowledge-contributions.md) · [Contributions, previous research and evaluation](docs/review/contribution-matrix.md).

## The two questions at a glance

| Question | What is compared | What the research seeks to establish |
|---|---|---|
| **How does identity persist through variation?** | Realisations across works, sources and performances, with documented family judgements. | Where each family occurs and which changes are organised by its identity. |
| **What does exegesis retain from older notation?** | A specific older passage and one or two confirmed analytical exegeses of it. | Which older notational distinctions can be recovered beyond metrophonia and known rules. |

[Musical evidence and schematic examples](docs/examples/index.md).

## Conditional extensions

The following designs are developed to broaden the core as far as possible. Each is activated by pre-specified criteria: sufficient data and sources, independent documentation and, where needed, collaboration with specialists.

- **The probabilistic operator Mθέσις.** A musicologically constrained model of realisations: the family specification defines the space of admissible realisations, and the contribution of the empirically learned distribution within that space is measured separately. [Overview](docs/current/m-thesis.md) · [Technical note](docs/current/m-thesis-technical.md).
- **Listening and performance validation.** Auditory family recognition (M3b), musical expectation (M3c) and recorded performance variation (full M4), developed in [Appendix A (Greek)](../docs/full/07-validation.md). M4-min is required only if the confirmatory historical strand of M2 is activated.
- **Musicologically grounded family signatures.** A pilot direction in musicology-informed machine learning that encodes independently validated criteria for formula families. [Overview (ECSI)](docs/research/ecsi/README.md).
- **Full M5.** Family sequences and functional roles in complete works, with a possible focus on Nikolaos Protopsaltis of Smyrna, given sufficient documentation and independence of sources.
- **Comparison with Znamenny chant.** Asks whether a method for recognising melodic identity amid variation can be evaluated when Byzantine *theseis* and Znamenny *popevki* are defined independently by each tradition. Conditional on sources and specialist annotation. [English research appendix](../docs/research/znamenny-transfer/research-appendix-en.md) · [Greek edition](../docs/research/znamenny-transfer/research-appendix.md).

**All documents:** [Greek short proposal](../documents/short-proposal.pdf) · [Detailed proposal (Greek)](../documents/analytical-proposal.pdf) · [PDF contents (Greek)](../documents/README.md) · [Documents and protocols](docs/reference.md)

[Comments and scientific discussion (Greek guide)](../docs/review/feedback.md) · [Shared research notebook](https://github.com/GeorgeSpy/byz-position-phd-study/issues/6)

## Start with your question

| I want to… | Reading route |
|---|---|
| understand the proposal in one reading | [Overview](docs/start/overview.md) |
| explore the methodology of the two routes | [Method map](docs/current/index.md) |
| understand the inverse problem and its measurements | [ATL-INV](docs/current/inverse-problem.md) |
| study how historical transformations are learned | [ATL](docs/current/atl.md) |
| examine the operator's definition and contribution | [Mthesis](docs/current/m-thesis.md) |
| explore the new Musicology-Informed Machine Learning research direction | **[ECSI — Musical Formula Family Signatures](docs/research/ecsi/README.md)** |
| explore Byzantine notation and formulae | [Musicological documentation (Greek)](../docs/musicology/index.md) |
| understand the contribution and its relationship to previous research | [Contributions by field](docs/review/contribution-matrix.md) |
| read a full chapter or technical appendix | [Detailed chapters and appendices (Greek)](../docs/full/index.md) |
| find a particular reference | [Methodological bibliography (Greek notes; original-language titles)](../docs/bibliography/methodology.md) · [Bibliographic index (Greek)](../docs/bibliography/index.md) |

The short proposal presents the research problem, methodology and expected contribution. The detailed proposal develops the musicological foundations, mathematical design and evaluation protocols. The thematic pages connect the questions with their evidence and references. [Documents and sources](docs/reference.md).

[All reading routes](NAVIGATION.md) · [Reading paths](docs/start/reading-paths.md) · [Thematic index (Greek)](../docs/topics.md) · [Research roadmap (Greek)](../docs/roadmap.md) · [Questions and evidence (Greek)](../docs/start/review-guide.md)

[Terminology](TERMINOLOGY.md) · [English translation progress](docs/translation-status.md)
