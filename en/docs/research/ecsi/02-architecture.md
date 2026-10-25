# Candidate ECSI-D Architecture

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../docs/research/ecsi/02-architecture.md) · **English**
<!-- language-switch:end -->

[Back to the ECSI overview](README.md)

**ECSI-D** is the proposed **dependent-signature model** (Work A2). The designation is distinct from **analysis A2 in Study M2**, which remains a separate part of the dissertation design.

## Components

1. A musically legitimate input encoded through representation **R★**, together with context `c`.
2. A shared encoder and a **dependent diagnostic distribution** `q_θ(z|x,c)`. The simpler factored distribution is a mandatory comparator rather than an untested default.
3. A documented family signature `σ_F` specifying requirements, supporting relationships, exclusions, contextual rules, and alternative sufficient branches.
4. **Exact membership probability**, with any overlap among sufficient branches counted **once**.
5. Scores that are comparable across candidate families under explicit calibration assumptions.
6. A separate expert-judgement observation model and an independent realisation-information branch `v`.

For a shared finite semantic space `Ω` of diagnostic configurations:

\[
\phi_F(z,c)=\mathbf 1[z\in S_F(c)],\qquad
m_F(x,c)=\sum_{z\in\Omega}q_\theta(z\mid x,c)\phi_F(z,c).
\]

When the admissible set of a broader family contains that of a more specific family, raw membership mass `m_F` favours the broader signature. The proposed correction uses a shared semantic space and requires independent empirical calibration. A candidate score uses a reference probability `r_F>0`:

\[
s_F=\log\pi_F(c)+\beta(\log m_F-\log r_F)+b_\gamma(d_F,c),\quad
p(F\mid x,c)=\operatorname{softmax}_{F}s_F.
\]

This is a **candidate scoring architecture**. Reading its output as an exact **Bayesian posterior** additionally requires a specified generative model and calibration evidence. The probability of a union of sufficient branches, the infimum distance to a union of continuous sets, and an epistemic mixture are mathematically distinct objects.

A family signature may introduce dependencies among anchors. Candidate implementations include exhaustive inference in small state spaces, joint conditional random fields (CRFs)/factor graphs, autoregressive models, or structurally compatible probabilistic circuits. Computational tractability has not yet been established for an entire real collection of formula families. For different candidate families, alignment is **candidate-conditioned**: the true family label is never provided as prediction input. Where candidates have different anchor spaces, score comparison requires an explicit semantic mapping and should be evaluated as calibrated compatibility, not presumed to be a literal Bayesian posterior.

The continuous ECSI-U-refined alternative and the **ECSI-D+R1** hybrid are considered only where a family has musicologically documented continuous **core** diagnostics and an adequate expert-judgement design.
