# 3. Boundary information at two segmentation scales

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/03-multiscale-boundary-information.md) · **English**
<!-- language-switch:end -->

[Overview](README.md) · [Models](01-research-questions-and-models.md) · [Gregorian benchmark](05-gregorian-benchmark.md) · [Numerical verification](06-mathematical-verification.md)

## Research question

An unsupervised model trained on unannotated chant proposes finer segmentations. This architecture estimates the probability that boundaries of complete formulae coincide with boundaries in the finer segmentation. The experiments test whether this relation adds information to F after controlling for span length, number of formulae and text features.

## Joint boundary-event probability

For a frozen model $`q_0`$ with segmentation weights $`W(z;X)`$ and a required boundary set $`B`$:

```math
Q_0(B\mid X)=\frac{\sum_{z:\,B\subseteq B(z)}W(z;X)}{\sum_{z}W(z;X)}.
```

$`Q_0`$ is the **joint probability** that all boundaries in $`B`$ occur, rather than a product of boundary marginals. It satisfies $`0\le Q_0\le1`$, $`Q_0(\varnothing\mid X)=1`$, and $`\log Q_0=-\infty`$ for an impossible event. LASM adds $`\lambda_b\log Q_0(B(y)\mid X)`$, with $`\lambda_b\ge0`$; $`\lambda_b=0`$ gives F.

### Zero-order segmentation base

When segmentation weights factorise by sub-segment and the complete analysis covers the work:

```math
\log Q_0\big(B(y)\mid X\big)=\sum_{s\in y}\log Z_0(s)-\log Z_0(X),
```

where $`Z_0(s)`$ is the sum of weights over all segmentations of span $`s`$. The contribution factorises by complete unit, so exact training and decoding retain the original computational complexity. With uncovered events in the Byzantine setting, each **maximal uncovered run** also contributes its $`\log Z_0`$ term to the numerator.

### Context-dependent base: NHPYLM

In the Nested Hierarchical Pitman–Yor Language Model (NHPYLM), the probability of a sub-segment depends on preceding context. Exact $`Q_0`$ carries history across the required boundaries and counts the beginning and end of a work only once. Resetting the history at each formula defines a different model. The local approximation A1 agrees with the exact result for zero or one internal boundary, but can deviate in either direction for multiple boundaries ([Section 6](06-mathematical-verification.md)). With a contextual base, the score couples neighbouring complete-formula spans. Exact decoding can use augmented-state dynamic programming or candidate re-ranking with certified upper bounds; certification must explicitly account for unexamined analyses.

## Executed experiments

All training experiments used a **zero-order multigram** base. Incorporating exact global NHPYLM $`Q_0`$ into training is a planned experiment. The present NHPYLM evaluation is numerical verification of boundary probabilities on constructed sequences.

### Synthetic series S1: text features included

The base was trained on 300 separate, unlabelled G0 works; three random initialisations.

| Training groups | J(F) | J(F+LASM) | J with shuffled-sequence base | F+LASM − F [95%] |
|---:|---:|---:|---:|---:|
| 4 | 0.679 | 0.678 | 0.677 | −0.001 [−0.010, +0.009] |
| 8 | 0.764 | 0.763 | — | −0.001 [−0.009, +0.008] |
| 48 | 0.894 | 0.900 | — | +0.006 [−0.002, +0.014] |

The confidence intervals contain zero in every S1 condition.

### Synthetic series S2: melody only

F+LASM − F = +0.036 [+0.022, +0.050]; when initialisations are also resampled, [+0.018, +0.055]. The learned weights were 0.167 / 0.187 / 0.180 in the three initialisations. Against F-wide, the difference is +0.010 [−0.007, +0.027]; the comparison with a capacity-matched scorer does not yield a statistically distinguishable gain for LASM.

### Gregorian evidence ([Section 5](05-gregorian-benchmark.md))

| Condition | LASM − F, exact-unit F1 [95%] | Real − shuffled base |
|---|---:|---:|
| Melody and text | −0.021 [−0.040, −0.001] | +0.003 [−0.028, +0.035] (initialisation 0) |
| Melody only | +0.044 [+0.025, +0.063] | +0.046 [+0.026, +0.065] |

### Interpretation

The boundary term improved performance in the **melody-only** conditions in both synthetic and Gregorian experiments. With text features, differences were neutral or slightly negative. A possible explanation is overlapping information between text alignment and the finer segmentation. A subsequent controlled comparison will evaluate that hypothesis using the same encoder, data and computational budget. S1 and S2 differ in encoder, budget and label count; the F-wide contrast assesses LASM relative to added model capacity.

## Invariance to linear duration offsets

For complete coverage of an event sequence of length $`T`$, the transformation $`\log Z_0(s)\mapsto\log Z_0(s)-\mu|s|`$ changes every legal complete-analysis score by the same constant $`-\lambda_b\mu T`$. Consequently, the normalised distribution over analyses, MAP decoding and joint F1 remain unchanged. Paired initialisations 0 and 1 gave identical J values for both versions (0.729308 and 0.682572).

## Next experiment

Six scoring configurations of the same trained F, separately with and without text: (1) F; (2) F plus length/count; (3) plus multigram; (4) plus NHPYLM with exact joint $`Q_0`$; (5) plus NHPYLM trained on shuffled sequences; and (6) plus the sum of individual boundary marginals. The unsupervised base is trained on data outside all held-out work groups. At least six paired random initialisations and a capacity-matched F comparator are planned.
