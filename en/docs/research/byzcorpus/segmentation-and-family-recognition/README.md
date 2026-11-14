# Melodic Segmentation and Formula Family Recognition

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/README.md) · **English**
<!-- language-switch:end -->

[Home](../../../../README.md) · [Research summary](../../../start/research-summary.md) · [M1 and selection rule J](../../m1-selection-decision.md) · [M1-X](../../m1-x-design.md) · [M2/EISE](../../m2-eise-research-design.md) · [ByzCorpus](../README.md)

> **Status (13 November 2026).** Research section in development. It brings together synthetic training experiments, exploratory Gregorian responsory experiments and numerical verification. Initial training on annotated Byzantine chant is the next phase, coordinated with ByzCorpus development.

## Architectures and experimental evaluation

This ByzCorpus research section examines melodic segmentation and the joint recognition of complete formulae and analytical families. The studies below assemble current synthetic and comparative results and specify the planned evaluation on Byzantine chant.

## Scope

The section evaluates architectures that detect melodic **formulae** (*theseis*) of variable duration and recognise their **analytical families** within continuous symbolic chant. Three questions organise the experiments:

1. Does the complete formula carry family information more effectively than a composition of internal sub-segments that preserve the same parent-family identity?
2. Does an independent unsupervised model of shorter segments provide additional boundary information once length and text context are controlled?
3. How can internal composition improve family recognition across different formula realisations?

The primary application is papadic Cheroubika and Koinonika in New Method notation. Helsen's Gregorian responsory material provides a comparative real-world monophonic testbed with its own analytical ontology.

## Section contents

| Section | Content | Study type |
|---|---|---|
| [1. Questions and models](01-research-questions-and-models.md) | Definitions of F, C_comp, C_fac, LASM, RM, DBC; common scoring; metrics | Specification |
| [2. Complete formula versus composition](02-full-position-vs-composition.md) | F–C_comp comparisons across two synthetic series | Synthetic training |
| [3. Boundary information at two scales](03-multiscale-boundary-information.md) | Joint $`Q_0(B\mid X)`$, LASM, null controls and duration-offset invariance | Synthetic experiments; numerical verification |
| [4. Family composition](04-family-compositional-learning.md) | RM, a trained synthetic prototype; DBC, a specified architecture | Synthetic training; specification |
| [5. Exploratory Gregorian benchmark](05-gregorian-benchmark.md) | Helsen mode 1: 123 responsories, 121 melodic groups | Exploratory real-data evaluation |
| [6. Mathematical and computational checks](06-mathematical-verification.md) | Dynamic programming versus enumeration, NHPYLM and certified search | Numerical verification |
| [7. Byzantine experimental protocol](07-byzantine-protocol.md) | Data, architectural comparisons and validity controls | Study design |
| [8. Decisions and evidence](08-decisions-and-evidence.md) | Architectural choices, evidence and pending evaluations | Research register |
| [References](REFERENCES.md) | Primary literature and software | Bibliography |
| [Experiment register](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/support/manifests/experiments.csv) | IDs, measures, provenance and rights; code release planned separately | Research records |

## Experiments and metrics

The [experiment register](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/support/manifests/experiments.csv) records synthetic training, exploratory real-data evaluations, numerical checks and planned comparisons. The [metrics register](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/support/manifests/metrics.json) gives computational conventions and definitions.

## Summary of findings

- **Complete formula versus composition.** F scores above C_comp in all executed synthetic conditions. The 95% intervals exclude zero in the assessed comparisons, while C_comp varies substantially across random initialisations. This result concerns composition trained using **complete-formula labels only** ([Section 2](02-full-position-vs-composition.md)).
- **Boundary information.** With text, LASM provides no detectable gain in the synthetic experiments and a small negative difference on the Gregorian material (−0.021). In melody-only experiments it shows positive differences in synthetic data (+0.036 joint F1) and Gregorian responsories (+0.044 exact-element F1). The latter is not replicated by a base trained on shuffled melodies ([Section 3](03-multiscale-boundary-information.md); [Section 5](05-gregorian-benchmark.md)).
- **Family term RM.** In S2, RM shows no statistically distinguishable improvement over the capacity-matched complete-formula model ([Section 4](04-family-compositional-learning.md)).
- **Gregorian benchmark.** With about 60 responsories for training per fold, F with text reaches exact-element F1 0.684 versus 0.173 for a cadence-based rule. Family accuracy remains limited at 0.448 on reference spans.

## Relation to the principal research programme

The present architecture comparisons form a complementary research workstream. **M1** retains its 12-condition $`U\times\Phi`$ grid, representation-selection rule J and selection of $`R_A^\star`$. **M1-X** retains the A–C_fac comparison. The present F–C_comp comparison examines internal composition: C_fac factorises boundaries and families with no latent internal sub-segments, while C_comp generates a formula's score from a latent composition ([Section 1](01-research-questions-and-models.md#c_fac-and-c_comp)). **A2** and **M2a/M2b/EISE** retain their respective protocols. **ByzCorpus** supplies the infrastructure for the Byzantine corpus.

The earlier [comparative NHPYLM–Helsen pilot](../gregorian-nhpylm-helsen-pilot.md) is a separate study. Its main analysis examines unsupervised segmentation of 148 mode-1 responsories; an exploratory extension covers 626 responsories across modes. The supervised study reported in [Section 5](05-gregorian-benchmark.md) uses a **subset** of 123 of those 148 mode-1 responsories.

## Reproducibility and rights

Aggregate results are linked to the [experiment register](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/support/manifests/experiments.csv), the [metrics register](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/support/manifests/metrics.json) and [source and rights documentation](support/manifests/sources-and-rights.md). Primary result files and execution scripts are planned for a subsequent reproducibility release, following validation of their dependencies and distribution rights.
