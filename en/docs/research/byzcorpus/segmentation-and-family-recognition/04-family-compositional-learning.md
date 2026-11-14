# 4. Family composition across different melodic realisations

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/04-family-compositional-learning.md) · **English**
<!-- language-switch:end -->

[Overview](README.md) · [Models](01-research-questions-and-models.md) · [M2/EISE](../../m2-eise-research-design.md) · [Musicological background (Greek)](../../../../../docs/musicology/index.md)

## Research question

The same formula family is realised through internal patterns that vary in length and elaboration. This study asks whether family recognition benefits from evaluating a formula's internal segments. In contrast to C_comp ([Section 2](02-full-position-vs-composition.md)), the internal segments are **supplied** by a frozen unsupervised model; their discovery does not depend on labels for complete formulae. Family identity remains attached to the parent formula.

## RM — experimental family-composition model

```math
\phi_{RM}(s,f;X)=\phi_F(s,f;X)+\eta\,\big[\log Z_f(s;X)-\log Z_0(s;X)\big],
```

where $`Z_0(s)`$ sums the internal segmentation weights of span $`s`$ from the frozen base and $`Z_f(s)`$ sums the corresponding weights after a family-specific *tilt*. The family tilt is initialised at zero, at which point the additional term vanishes and the score equals F.

**Result (S2, melody only, three initialisations).** F+RM achieved mean joint F1 J of 0.642, compared with 0.627 for F and 0.653 for F-wide, which has a matched parameter count (12,037 versus 11,988).

| Contrast | Difference | 95% work groups | 95% work groups and initialisations |
|---|---:|---:|---:|
| F+RM − F | +0.015 | [−0.003, +0.033] | [−0.009, +0.041] |
| F+RM − F-wide | −0.011 | [−0.031, +0.008] | [−0.052, +0.028] |
| F+RM − F+LASM | −0.021 | [−0.037, −0.005] | [−0.042, −0.001] |

RM performed at a level statistically comparable to F and the capacity-matched full-span scorer. In this generator, F already achieves family accuracy of 0.89–0.95 on reference spans, leaving limited scope for improvement from the family term. The next evaluation will use conditions with more challenging family recognition.

## DBC — specified architecture

Let $`q_s`$ be a fixed, normalised distribution over internal segmentations $`z`$ of formula $`s`$, and let $`\widetilde V_f(u)`$ be a centred family-specific score for sub-segment $`u`$. Define

```math
A_f(z,s)=\sum_{u\in z}\frac{|u|}{|s|}\,\widetilde V_f(u),\qquad
R_f^{\mathrm{lin}}(s)=\mathbb E_{q_s}\big[A_f\big],\qquad
R_f^{\mathrm{dur}}(s)=\log\mathbb E_{q_s}\big[\exp A_f\big].
```

Duration weighting makes the contribution independent of the number of sub-segments when the family score is constant over the formula. The family contribution is decomposed into a discriminative identity component and a common component:

```math
\bar R(s)=\frac{1}{|\mathcal F|}\sum_{f}R_f(s),\qquad R_f^{\mathrm{id}}(s)=R_f(s)-\bar R(s).
```

$`R^{\mathrm{id}}`$ changes family selection only. $`\bar R`$ changes the common span score across all families and can therefore shift boundaries. Both components are estimated and reported separately.

**Numerically verified properties** ([Section 6](06-mathematical-verification.md)):

- With a constant family score, the duration-weighted $`R^{\mathrm{dur}}`$ has the same value for every segmentation; variable scores break this property.
- Jensen's inequality gives $`R^{\mathrm{lin}}\le R^{\mathrm{dur}}`$; dynamic programming agrees with enumeration.
- Family-wise centring leaves a common nonlinear contribution, which motivates the explicit $`R^{\mathrm{id}}`$ / $`\bar R`$ decomposition.
- A constant family offset can change the predicted number of complete formulae; there is no general monotonicity with span length.

DBC is currently a **mathematical architecture specification**, with the numerical properties of its kernels verified in [Section 6](06-mathematical-verification.md), in preparation for training and evaluation on real data.

## Next experiment

A factorial design on real data will compare: LASM boundary term present/absent × family term present/absent; $`R^{\mathrm{lin}}`$ versus $`R^{\mathrm{dur}}`$; $`R^{\mathrm{id}}`$ versus $`R^{\mathrm{id}}+\bar R`$; a simple per-event mean, a direct family-classification head and a capacity-matched F; and unknown family classes. The evaluation requires data on which F has not already nearly saturated family recognition.

## Relation to M2/EISE

M2a learns from occurrences of the same analytical family; M2b/EISE uses historically documented pairs of exegetic versions of the same passage, with its own evidence-adequacy criteria. The family term here can use a suitable supervision source while leaving the M2 experimental protocols intact. Analytical family identity and historical identity remain separate relations.
