# 7. Experimental protocol for Byzantine chant

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/07-byzantine-protocol.md) · **English**
<!-- language-switch:end -->

[Overview](README.md) · [ByzCorpus](../README.md) · [Data model (Greek)](../../../../../docs/research/byzcorpus/data-model.md) · [Expert boundary agreement pilot](../expert-boundary-pilot.md) · [M1](../../m1-selection-decision.md) · [M2/EISE](../../m2-eise-research-design.md)

This section specifies the experimental protocol for complete Byzantine chant works following the first annotated ByzCorpus release. Synthetic and comparative Gregorian experiments provide the initial computational evidence; the Byzantine evaluation will establish results in the principal target domain.

## Data

Priority is assigned to complete papadic Cheroubika and Koinonika in New Method notation. In accordance with the [ByzCorpus data model (Greek)](../../../../../docs/research/byzcorpus/data-model.md), each work links a composition, an identifiable source, a digital transcription, neumatic notation, atomic melodic events, syllables and words, modal features, and independent annotations of formula boundaries and analytical families.

The St Anthony's Monastery *Papadic Formulae* catalogue and the Gheorghiță (2009) inventory support **retrieval** of candidate formula occurrences and families. They are reference inventories rather than training instances. Supervised training uses complete, verified works with explicit reviewed regions and distinct categories for unknown family, annotator abstention and connective material.

## Comparisons

| Workstream | Comparison | Role |
|---|---|---|
| M1 | Select $`R^\star`$ on $`U\times\Phi`$ by rule J | Independent M1 representation-selection procedure |
| M1-X | A versus C_fac | Retains its established protocol |
| Complete formula versus composition | F versus C_comp with the same family identity and supervision | Label-learning curve and limited internal annotations |
| Boundary information | F, F+length, +multigram, +NHPYLM with global $`Q_0`$, +shuffled base, +marginals | With and without text cues |
| Family composition | RM; DBC with $`R^{\mathrm{id}}`$ / $`\bar R`$ and $`R^{\mathrm{lin}}`$ / $`R^{\mathrm{dur}}`$; direct family head; capacity-matched F | Subsequent stage |
| M2/EISE | Family and historical supervision | Separate protocol |

In the exploratory Gregorian evaluation, boundary information helped only in the melody-only configuration ([Section 5](05-gregorian-benchmark.md)). In melismatic Byzantine genres, a syllable may extend over a long melodic passage and thus yields fewer candidate boundaries. Comparing models with and without text is consequently an important **research hypothesis** for the upcoming Byzantine experiments.

## Validity controls

- Hold out groups of works, sources and related transcriptions; check information leakage in the unsupervised base as well.
- Build family vocabularies from training data only; distinguish rare, unknown and non-standardised labels; calibrate on development sets.
- Report joint formula-and-family F1, exact-formula F1, boundary F1, macro-F1 by family and open-set family recognition.
- Accommodate multiple acceptable annotations per work using one whole-analysis evaluator; apply masks to unreviewed regions and annotator abstentions.
- Set maximum formula length using training data and report coverage.
- Use paired random initialisations and group/initialisation bootstraps; report decoding cost and certification coverage.
- Register hypotheses and decision criteria before training.

## Prerequisites

1. Annotated complete works with verified rights and symbol-to-event alignment ([ByzCorpus](../README.md)).
2. Exact global $`Q_0`$ from a frozen NHPYLM trained on Byzantine chant.
3. The corrected protocol specified in [Section 5](05-gregorian-benchmark.md#technical-findings-and-changes-for-the-next-phase).
