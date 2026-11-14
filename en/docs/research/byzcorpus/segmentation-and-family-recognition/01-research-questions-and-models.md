# 1. Research questions and models

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/01-research-questions-and-models.md) · **English**
<!-- language-switch:end -->

[Overview](README.md) · [M1-X](../../m1-x-design.md) · [Appendix G (Greek)](../../../../../docs/appendices/g.md) · [M2/EISE](../../m2-eise-research-design.md)

## Research problem

Recognising a melodic formula (*thesis*, plural *theseis*) within a continuous symbolic representation requires joint estimation of its onset, offset and family. Formulae vary in length, a family may have multiple realisations, and some passages may lie outside any recognised formula. This is a structured-prediction problem over non-overlapping melodic spans labelled with analytical families.

1. **RQ1 — Complete formula and internal composition.** To what extent does a complete formula preserve family information more effectively than a composition of smaller segments that share the same family?
2. **RQ2 — Boundary information.** What additional boundary information can an independent, unsupervised finer-segmentation model provide after controlling for duration, number of formulae and context?
3. **RQ3 — Family recognition.** How does family-dependent internal composition contribute to distinguishing different realisations of a formula family?
4. **RQ4 — Musicologically informed features.** How do neumatic signs, *echos* (mode), text and historical relationships contribute to formula boundary detection and family recognition in matched experimental conditions?

## Common output space

A work is represented by a sequence of atomic melodic events $`X=(e_1,\ldots,e_T)`$. An analysis $`y`$ consists of non-overlapping pairs $`(s,f)`$, where $`s=[a,b]`$ is a contiguous **event-index span** and $`f`$ is the analytical family of the corresponding melodic formula. A span is an interval of event indices, distinct from a musical interval between pitches. The maximum complete-formula length is $`L_{\mathrm{outer}}=L_2`$ events; the exploratory Helsen experiments used $`L_2=36`$. The Byzantine application permits uncovered events and an empty analysis. In the executed comparisons of Sections 2–5, all events are covered by the analytical units.

The full-span scorer F and the locally compositional models use a zero-order semi-Markov conditional random field (CRF), with score

```math
S_{\mathrm{local}}(y;X)=\sum_{(s,f)\in y}\phi(s,f;X)+S_{\mathrm{gap}}(y;X),\qquad
p_{\mathrm{local}}(y\mid X)=\frac{\exp S_{\mathrm{local}}(y;X)}{\sum_{y'\in\mathcal Y(X)}\exp S_{\mathrm{local}}(y';X)}.
```

The term $`S_{\mathrm{gap}}`$ scores uncovered events and vanishes for the executed full-coverage conditions. With locally computable span potentials $`\phi`$, dynamic programming gives exact partition functions, log-likelihood gradients and maximum-a-posteriori (MAP) decoding.

LASM adds the joint boundary-event probability $`Q_0(B(y)\mid X)`$. For a zero-order base this term factorises by span. A context-sensitive base such as the Nested Hierarchical Pitman–Yor Language Model (**NHPYLM**) couples formulae through segmentation history; exact inference requires augmented-state dynamic programming or candidate search with certified upper bounds. DBC is an architecture specified for subsequent empirical evaluation.

## Models

### F — complete-formula scorer

```math
\phi_F(s,f;X)=\mathrm{MLP}_\theta\big(h(s;X)\big)_f,
```

where $`h(s;X)`$ summarises bidirectional recurrent-encoder states at the endpoints and within $`s`$, including a length representation. F has no latent segmentation variable.

F belongs to the same broad zero-order semi-Markov scoring class as M1 architecture A ([Appendix G (Greek)](../../../../../docs/appendices/g.md)). A retains its own family-compatibility specification and implements the M1 representation-selection procedure. F serves as an independent reference architecture for the experiments reported here.

### C_comp — latent composition with a shared parent family

A complete formula $`s`$ has an internal segmentation $`z_s=(u_1,\ldots,u_m)`$, with $`u_r`$ a contiguous sub-segment and $`m=m(z_s)`$ the number of sub-segments. The set $`\mathcal Z(s)`$ contains all permitted internal segmentations with maximum sub-segment length $`L_{\mathrm{inner}}`$. Each sub-segment is assigned a latent type $`k_r\in\{1,\ldots,K\}`$ drawn from a shared inventory of $`K`$ types. The family $`f`$ remains identical throughout the parent formula:

```math
\phi_{C_{\mathrm{comp}}}(s,f;X)=\beta_f+\log\sum_{z_s\in\mathcal Z(s)}\sum_{\mathbf k\in\{1,\ldots,K\}^{m(z_s)}}\exp\!\left(
\pi_f[k_1]+\sum_{r=1}^{m}e(u_r,k_r;X)+\sum_{r=2}^{m}A_f[k_{r-1},k_r]+\omega_f[k_m]\right).
```

Here $`\beta_f`$ is a family-specific score bias, $`e(u,k;X)`$ scores a sub-segment and its latent type, $`\pi_f`$ gives the initial type potential, $`A_f`$ the transition potential and $`\omega_f`$ the terminal potential. The last three comprise shared parameters and family-specific shifts: $`\pi_f=\pi_0+\Delta\pi_f`$, $`A_f=A_0+\Delta A_f`$, and $`\omega_f=\omega_0+\Delta\omega_f`$. The emission score $`e`$ is shared across families. Dynamic programming marginalises the internal segmentations and types exactly. Training uses labels of complete formulae while internal structure remains latent.

A sufficiently expressive complete-formula scorer can approximate $`\phi_{C_{\mathrm{comp}}}`$. C_comp imposes a specific **inductive bias** through its finite type inventory and transitions. [Section 2](02-full-position-vs-composition.md) tests the consequences with identical family supervision and matched model capacity.

**Control variants.** *C-untied* uses a separate type inventory for each family; *C-bag* omits type transitions to test ordering information; *C-agn* uses family-agnostic internal types and a full-span family head. *FC* is the recorded experimental hybrid $`F+C_{\mathrm{comp}}`$, obtained by summing $`\phi_F`$ and $`\phi_{C_{\mathrm{comp}}}`$. *F-wide* is a capacity-matched F. The explicit subscripts distinguish the C_comp architecture here from C_fac in M1-X; FC is retained as the registered experimental label.

### C_fac and C_comp

**C_fac** in [M1-X](../../m1-x-design.md) factorises boundary and family decisions as $`p_B(B\mid X)\prod_s p_F(f_s\mid s,X)`$, with a free boundary head and a normalised family head. Its model does not introduce latent internal sub-segments. **C_comp** constructs each complete formula from latent sub-segments. Thus the A–C_fac and F–C_comp contrasts address distinct architectural questions.

### LASM — multiscale boundary compatibility

**LASM** transfers boundary information from a finer unsupervised segmentation to complete-formula recognition. A frozen model $`q_0`$ is trained on unannotated chant; $`B(y)`$ is the set of internal boundaries of the complete-formula analysis. Let $`z_0`$ denote a finer segmentation of the **entire** event sequence $`X`$ generated by $`q_0`$, as distinct from C_comp's within-formula segmentation $`z_s`$. LASM adds

```math
\lambda_b\log Q_0\big(B(y)\mid X\big),\qquad Q_0(B\mid X)=q_0\big(B\subseteq B(z_0)\mid X\big),\qquad \lambda_b\ge0,
```

namely the log-probability that **all** boundaries of the complete-formula analysis are also boundaries of the finer segmentation. Setting $`\lambda_b=0`$ recovers F. Zero-order and context-dependent computation are discussed in [Section 3](03-multiscale-boundary-information.md).

### RM and DBC — family composition over a finer segmentation

- **RM — family-conditioned marginalisation of internal analyses.** The trained experimental model uses $`\phi_{RM}(s,f;X)=\phi_F(s,f;X)+\eta\,[\log Z_f(s;X)-\log Z_0(s;X)]`$. $`Z_0`$ sums the weights of permitted internal segmentations from the frozen base; $`Z_f`$ sums the corresponding family-tilted weights. The additional score vanishes at zero family tilt. The coefficient $`\eta`$ belongs to the trained RM experiment.
- **DBC — duration-weighted family composition.** The proposed extension combines boundary-event probability with family-specific sub-segment scores. It separates family identity information from the common component that affects boundary selection. Mathematical definitions and the evaluation status are given in [Section 4](04-family-compositional-learning.md).

## Combined scoring architecture for future evaluation

The proposed architecture integrates full-span scoring, optional duration effects, family information and boundary compatibility:

```math
S_{\mathrm{combined}}(y;X)=\sum_{(s,f)\in y}\!\left[\phi_F(s,f;X)+\ell(|s|)+\lambda_c R_f(s;X)\right]
+S_{\mathrm{gap}}(y;X)+\lambda_b\log Q_0\big(B(y)\mid X\big),
\qquad \lambda_b\ge0,\quad \lambda_c\ge0.
```

The optional $`\ell(|s|)`$ scores span length or formula count and is assessed separately because the encoder representation $`h(s;X)`$ already contains length information. $`R_f(s;X)`$ is a family-specific contribution derived from RM or DBC. The coefficient $`\lambda_c`$ pertains to this future combined architecture and is distinct from $`\eta`$ in the trained RM prototype. $`S_{\mathrm{gap}}`$ accommodates uncovered connective passages. Both coefficients are selected using development data.

For a zero-order base, $`Q_0`$ factorises locally. With history-dependent NHPYLM, complete-formula scores are coupled across spans, requiring exact history-state propagation or certified re-ranking. **The combined architecture is a training specification**; currently available experiments evaluate its components separately.

## Metrics

Metric conventions are defined here and recorded in the [machine-readable metrics register](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/support/manifests/metrics.json).

- **Joint formula-and-family F1 ($`J`$ in the experimental tables):** one-to-one matching of onset, offset and family label, aggregated over TP/FP/FN. The distinct **M1 selection rule J** selects a symbolic representation $`R^\star`$ by maximising the estimated joint score $`\widehat J_A(R)`$ of prespecified architecture A among representations satisfying $`\widehat G_A(R)\ge g_{\min}`$. $`\widehat G_A`$ is macro-average family recall with reference boundaries; the $`U\times\Phi`$ grid combines three input units $`U`$ and four feature sets $`\Phi`$ (12 conditions). The full selection procedure and associated uncertainty set are specified in [M1](../../m1-selection-decision.md).
- **Exact-formula F1:** exact onset–offset matching irrespective of family.
- **Boundary F1:** micro-averaged F1 over internal cut positions.
- **Family accuracy at reference boundaries:** family classification on given spans; distinct from joint F1.
- **Bits per candidate boundary position:** cross-entropy in bits per possible boundary between successive melodic events, with the eligible coverage reported.

The 95% intervals use paired work-group bootstrap resampling (10,000 replicates). Where stated, bootstrap sampling also includes random initialisations. Work-group-only intervals do **not** include training variability.
