# 2. Complete-formula scoring versus sub-segment composition

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/02-full-position-vs-composition.md) · **English**
<!-- language-switch:end -->

[Overview](README.md) · [Models](01-research-questions-and-models.md) · [Evidence register](08-decisions-and-evidence.md)

This section uses controlled synthetic data to compare architectures and assess family-recognition performance across training conditions.

## Research question

F scores the complete formula. C_comp constructs the formula from latent internal sub-segments while preserving the same family across the entire internal analysis. The two models share the encoder, supervision (family labels only at complete-formula level), decoder and approximately the same number of parameters. The comparison tests whether compositional inductive bias improves learning.

## Generators

- **G0:** six families; each formula is assembled from fixed motifs with variations. Two text–melody configurations are generated: syllabically aligned and melismatic.
- **G1 (shared inventory):** eight families constructed from eight shared motifs, with two rare families. It is designed to favour composition in low-label settings.
- **G2 (endpoint agreement):** family identity depends on the relationship between the first and last motif; designed to favour complete-formula scoring.

## Series S1

An encoder with $`H=48`$ and textual features; $`K=8`$ internal types; early stopping selected by development-set joint F1 $`J`$. Five random initialisations are used for F and C_comp on G0 and three for the other conditions. Parameter counts on G0: F 35,763; C_comp 35,750.

| Condition | J(F) | J(C_comp) | C_comp − F [95%] |
|---|---:|---:|---:|
| G0, 48 training groups, extended test set (288 works / 96 groups) | 0.894 | 0.749 | −0.146 [−0.161, −0.131] |
| G0, 48 groups, small test set (36 / 12) | 0.835 | 0.707 | −0.127 [−0.185, −0.070] |
| G1, 8 training groups (test 216 / 72) | 0.644 | 0.319 | −0.327 [−0.359, −0.293] |
| G1, 48 groups | 0.821 | 0.540 | −0.281 [−0.312, −0.250] |
| G2, 48 groups | 0.284 | 0.152 | −0.133 [−0.159, −0.108] |

C_comp performs below F in every executed condition, including G1 with eight training groups, which was designed to demonstrate the strengths of composition.

**Control conditions**

| Comparison | Result |
|---|---|
| Hybrid FC − F | G0: −0.006 [−0.019, +0.005]; G1/8: −0.061 [−0.083, −0.040]; G1/48: −0.005 [−0.020, +0.010]; G2: −0.015 [−0.033, +0.004] |
| FC − F-wide (matched parameters, G0) | −0.002 [−0.013, +0.009] |
| C_comp − C-untied (shared vs separate inventory per family) | G1/8: −0.107 [−0.136, −0.078]; G1/48: −0.175 [−0.205, −0.147] |
| C_comp − C-bag (with vs without type order, G1/48, two C-bag initialisations) | −0.072 [−0.097, −0.048] |
| C-agn (family-independent composition plus full-span family head, G0, one initialisation) | J = 0.891 versus F 0.894 |
| Rare / frequent family recall, G1/48 | F 0.674 / 0.882; C_comp 0.169 / 0.686; C-untied 0.577 / 0.775 |
| Internal-cut F1 of C_comp against generator motifs | G0: 0.315; G1/48: 0.239 |
| Family accuracy on reference spans, G2 (chance 0.25) | F 0.377; C_comp 0.243 |

Sharing the type inventory did not improve performance: C-untied outperformed C_comp. The hybrid did not exceed F. C-agn, which predicts the family through a complete-span head, reached a similar value to F in one initialisation. C_comp's performance gap is associated with routing family information exclusively through latent internal types. A single C-agn result is insufficient to establish equivalence.

## Series S2 — matched melody-only comparison

Melody-only input; encoder $`H=24`$; 24 works / 8 training groups, 36 / 12 development and 288 / 96 test; 30 epochs × 8 updates; initialisations 0, 1, 2. S2 uses G0 with a different architecture and training budget from S1; numerical results should be compared **within** each series.

| System | Parameters | Init. 0 | Init. 1 | Init. 2 | Mean J |
|---|---:|---:|---:|---:|---:|
| F | 10,150 | 0.638 | 0.630 | 0.612 | 0.627 |
| F + LASM | 10,151 | 0.663 | 0.677 | 0.648 | 0.663 |
| F + RM | 11,988 | 0.643 | 0.662 | 0.620 | 0.642 |
| F-wide | 12,037 | 0.622 | 0.671 | 0.666 | 0.653 |
| C_comp (K=8) | 10,129 | 0.260 | 0.018 | 0.434 | 0.237 |
| COMP (composition only on the frozen base) | 8,286 | 0.354 | 0.337 | 0.301 | 0.331 |

| Contrast | Mean difference per initialisation | 95% work groups | 95% work groups and initialisations |
|---|---:|---:|---:|
| F − C_comp | +0.389 | [+0.358, +0.420] | [+0.185, +0.603] |
| COMP − F | −0.296 | [−0.325, −0.265] | [−0.330, −0.259] |
| F+LASM − F | +0.036 | [+0.022, +0.050] | [+0.018, +0.055] |
| F+RM − F | +0.015 | [−0.003, +0.033] | [−0.009, +0.041] |
| F+RM − F-wide | −0.011 | [−0.031, +0.008] | [−0.052, +0.028] |

C_comp exhibits substantial variation across initialisations: one of the three runs barely trained (J = 0.018). LASM and RM are analysed further in [Section 3](03-multiscale-boundary-information.md) and [Section 4](04-family-compositional-learning.md), respectively.

## Interpretation and next steps

- Across the evaluated generators, latent composition trained with supervision **only at complete-formula level** scores below F. Pretraining the internal layer, limited internal annotations and $`\max_z`$ decoding are candidates for further experiments. One exploratory run with $`K=16`$ also scored below F.
- The initial hypothesis that composition would outperform F with few labels (G1) or for rare families was not supported by the corresponding synthetic runs. **G0 with eight training groups remains untested.**
- A promising direction for Byzantine formulae is internal composition using sub-segments supplied by an independent segmentation model or musicological annotation, as developed in [Section 4](04-family-compositional-learning.md).

**Next comparison:** F versus C_comp on real data, including a label-learning curve, alternative initialisations, a small amount of internal supervision and a separate M1-X C_fac baseline.
