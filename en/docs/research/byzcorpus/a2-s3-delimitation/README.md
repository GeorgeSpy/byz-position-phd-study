# A2–S3 · Musicological knowledge and complete-formula delimitation

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../docs/research/byzcorpus/a2-s3-delimitation/README.md) · **English**
<!-- language-switch:end -->

[ByzCorpus](../README.md) · [S3 protocol](protocol.md) · [Evidence and next steps](evidence-and-next-steps.md) · [Core A2](../../a2-knowledge-design.md) · [Segmentation and families](../segmentation-and-family-recognition/README.md)

> **Status · 16 November 2026:** a separate ByzCorpus research extension. Its mathematical implementation and decision rules have been tested on synthetic data. Musicological screening and evaluation on actual Byzantine chant are subsequent stages. [Executable checks](../../../../../docs/research/byzcorpus/a2-s3-delimitation/support/README.en.md), [B_L training](../../../../../docs/research/byzcorpus/a2-s3-delimitation/support/bl-training.en.md), and the [A2 score ingestion interface](../../../../../docs/research/byzcorpus/a2-s3-delimitation/support/integration.en.md) are available in separate technical PRs. Empirical evaluation requires reviewed primary-source annotations and actual trained model scores.

## Research question

How do **valid, logically structured musicological family specifications** help distinguish a complete melodic formula from plausible truncations and extensions?

A2–S3 studies the **extent** of a formula with its family identity and preferred start held fixed. For a documented occurrence, it contrasts the accepted complete extent with two alternative right endpoints: a plausible premature ending and an extension into documented connective material.

The paired comparison reuses scores from the established FV, FP, DV and DP conditions of [core A2](../../a2-knowledge-design.md). The **B_L delimitation reference** accounts for exact length per candidate family, articulation and text boundaries, with L2 regularisation. Internal melodic development is examined through musicological specifications and diagnostic interpretation.

## Place in the research programme

| Study | Question | Connection to A2–S3 |
|---|---|---|
| [M1](../../m1-selection-decision.md) | Representation selection and joint boundary–family recognition | Shared event axis and R★ representation |
| [Core A2](../../a2-knowledge-design.md) | Knowledge validity × logical use: family AP at accepted fixed boundaries | Existing conditions and model scores |
| **A2–S3** | Knowledge contribution to preference for complete extent | Separate diagnostic estimand and protocol |
| [ByzCorpus segmentation](../segmentation-and-family-recognition/README.md) | Statistical subsegments, complete formulas and family recognition | Independent comparison against NHPYLM cuts |
| [M3a](../../../../../docs/full/07-validation.md#r052) | Independent musicological validation | Evaluation of finalised specifications on separate material |

Core A2 retains its V/P × F/D design, family AP, two primary estimands, five replications and [Appendix K](../../../appendices/k.md). S3 has its own question, candidate-variant rules, eligibility conditions and descriptive statistics. The [S3 protocol](protocol.md) is the **single authoritative location** for its technical definition.

## Relation to segmentability

NHPYLM supplies independent statistical evidence about smaller melodic units. The main S3 variants are chosen **from musicological judgements and prespecified articulation**, without using NHPYLM cuts to construct them. A **separate analysis** compares eligible points with and without such cuts, controlling for articulation, textual boundaries, distance from the accepted endpoint and length.

This approach connects to comparative *segmentability* in Gregorian and Byzantine chant while retaining tradition-specific musicological reference units.

## Evaluation pathway

**WP0 screening** develops and checks family cards, accepted extents, connective regions and eligible variants. **M3a** independently evaluates the finalised guidelines on separate material. Subsequent computational S3 assessment uses a common occurrence sample, a fixed family catalogue and the scores from core A2.

See the [full protocol](protocol.md), [evidence and research plan](evidence-and-next-steps.md), [executable reference checks](../../../../../docs/research/byzcorpus/a2-s3-delimitation/support/README.en.md), [trained B_L comparator](../../../../../docs/research/byzcorpus/a2-s3-delimitation/support/bl-training.en.md), and [source-to-score integration guide](../../../../../docs/research/byzcorpus/a2-s3-delimitation/support/integration.en.md).
