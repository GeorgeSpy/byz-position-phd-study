# Melodic Segmentation and Formula Family Recognition

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/README.md) · **English (summary)**
<!-- language-switch:end -->

[Home](../../../../README.md) · [Core research summary](../../../start/research-summary.md) · [M1 and rule J](../../m1-selection-decision.md) · [M1-X](../../m1-x-design.md) · [M2/EISE](../../m2-eise-research-design.md) · [ByzCorpus](../README.md)

> **Status (13 November 2026).** A research section in development: synthetic trainings, exploratory runs on Gregorian responsories and numerical checks. The initial training and evaluation on annotated Byzantine works is the next planned phase alongside the development of ByzCorpus. This page summarises the Greek record, which contains the full tables.

## Questions

The section studies architectures that detect melodic formulae (*theseis*) of variable length in continuous symbolic chant and recognise their analytical family. Three questions organise the experiments:

1. Does the complete formula carry family information better than a composition of internal sub-segments that keeps the same family?
2. Does an independent, unsupervised model of smaller segments add boundary information once length and context are controlled?
3. Can internal composition help to recognise a family across different realisations?

The primary application is the papadic Cheroubika and Koinonika in New Method notation. Helsen's Gregorian responsory elements serve as a comparative testbed with their own, independent family ontology.

## Models

F and the locally factorised compositional models use zero-order semi-Markov CRFs with exact dynamic programming for their local scores. LASM adds a global boundary-event term: with a zero-order base this factorises by span, whereas a context-dependent NHPYLM base requires history-aware inference or certified search. DBC is currently a mathematical specification.

- **F** scores the whole span together with its family. It shares the broad semi-Markov probabilistic class of M1 architecture A, while A retains its specified family-compatibility structure and the representation-selection rule J.
- **C_comp** builds each formula from latent typed sub-segments drawn from a shared inventory and keeps the parent family throughout. It is distinct from **C_fac** in M1-X, a factorised boundary-and-family model without latent sub-segments.
- **LASM** adds $`\lambda_b\log Q_0(B(y)\mid X)`$ with $`\lambda_b\ge0`$: the log-probability, under a frozen unsupervised segmentation model, that all boundaries of the analysis are also boundaries of the finer segmentation.
- **RM** adds a family tilt of the frozen base (trained in a synthetic prototype). **DBC**, a duration-weighted family term, is specified but not trained.

## Findings

| Question | Result | Evidence class |
|---|---|---|
| F versus C_comp | F ahead in every synthetic cell, e.g. joint F1 0.894 vs 0.749 (G0) and 0.644 vs 0.319 in the cell designed to favour composition; C_comp unstable across seeds. Applies to composition learned from formula-level labels only. | Synthetic |
| Boundary term, with text | No detectable gain in the synthetic comparisons; Gregorian −0.021 [−0.040, −0.001] exact-unit F1 | Synthetic; Gregorian exploratory |
| Boundary term, melody only | Synthetic +0.036 [+0.022, +0.050] joint F1, but not distinguishable from a capacity-matched F; Gregorian +0.044 [+0.025, +0.063], not reproduced by a base trained on shuffled melodies | Synthetic; Gregorian exploratory |
| Family term RM | Not distinguishable from F or from capacity-matched F | Synthetic |
| Gregorian feasibility | With about 60 training responsories per fold, F with text reaches exact-unit F1 0.684 against 0.173 for a cadence rule; family accuracy on reference units only 0.448 | Gregorian exploratory |

The Gregorian runs are exploratory: the fixed-length training protocol was adopted after a first batch had been inspected, and that batch, which showed an artefactual gain, is withdrawn but kept for transparency. Linear duration centring leaves the probability distribution over complete segmentations unchanged; the paired runs confirm this invariance.

## Relation to the core programme

M1 (the $`U\times\Phi`$ grid, rule J, $`R_A^\star`$), M1-X (A versus C_fac), A2, M2a/M2b/EISE and ByzCorpus keep their roles and protocols. The [comparative NHPYLM–Helsen pilot](../gregorian-nhpylm-helsen-pilot.md) is earlier and self-contained; the supervised experiments here use 123 of its 148 mode-1 responsories.

**Detailed record (Greek):** [models](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/01-research-questions-and-models.md) · [complete formula vs composition](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/02-full-position-vs-composition.md) · [boundary information](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/03-multiscale-boundary-information.md) · [family composition](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/04-family-compositional-learning.md) · [Gregorian benchmark](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/05-gregorian-benchmark.md) · [numerical checks](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/06-mathematical-verification.md) · [Byzantine protocol](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/07-byzantine-protocol.md) · [references](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/REFERENCES.md) · [experiment register](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/support/manifests/experiments.csv)

**English:** [decisions and evidence](08-decisions-and-evidence.md)

The experimental record identifies completed runs, numerical checks, withdrawn results and planned work. Reported statistics are reconstructed from stored outputs, with explicit source and reproducibility information.
