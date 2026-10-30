# Mθέσις: technical note on decomposition and evaluation

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/current/m-thesis-technical.md) · **English** · [Translation progress](../translation-status.md)
<!-- language-switch:end -->

[The operator: idea and definition](m-thesis.md) · [Formula and family](position-and-family.md) · [Historical recovery](inverse-problem.md)

This note develops family-label provenance, the definition of the intermediate model, common support and reporting units. It uses the definitions of cross-entropy and family benefit on the [main page](m-thesis.md#the-first-testable-quantity).

## Family-label provenance

The family label may describe an already recognised realisation, come from information available before the target, or be the output of a recognition task. The [three uses](position-and-family.md#label-provenance-and-independent-evaluation) are recorded separately, together with the features seen by the annotator.

Descriptive use with a label assigned from $X$ itself evaluates the distribution conditional on a known category. Prospective use requires $F$ to be available from information outside the masked region. Masking is applied before encoding and also covers derived features that could reveal the target. Held-out works and independent sources provide complementary tests of generalisation.

## Decomposing family information

For a common target set $D$ and common normalisation, write $\mathrm{CE}(q)$ for the mean logarithmic loss defined above. Introducing any specified intermediate model gives the algebraic identity:

$$\Delta_{\mathrm{family}} =\underbrace{\mathrm{CE}(q_0)-\mathrm{CE}(q_\sigma)}_{\Delta_\sigma} +\underbrace{\mathrm{CE}(q_\sigma)-\mathrm{CE}(q_F)}_{\Delta_{F\vert\sigma}}.$$

Its interpretation depends on the definition of $q_\sigma$. A model learned freely with $\sigma_F$ as input can also exploit empirical preferences. When $\sigma_F$ uniquely identifies $F$, the two conditions convey equivalent identity information; differences between the learned models assess estimation and parameterisation. Comparisons of finite models retain this scope of interpretation.

### A controlled baseline that restricts support

To measure selectivity separately, a specific additional baseline is defined: restrict the context model to the set $\mathcal X(\sigma_F,C)$ of realisations permitted by the stabilised specification.

$$Z_0(F,C)= \sum_{x\in\mathcal X(\sigma_F,C)}q_0(x\vert C), \qquad q_\sigma(x\vert C,\sigma_F)= \frac{q_0(x\vert C)\,\mathbf 1\lbrace x\in\mathcal X(\sigma_F,C)\rbrace } {Z_0(F,C)}.$$

This requires $Z_0(F,C)\gt 0$ and a normaliser that can be computed or adequately approximated. $q_\sigma$ inherits relative probabilities within the admissible set from $q_0$. Estimation of the normaliser reports the method and numerical uncertainty.

On the common subset $D_\sigma$ where every $x_i$ satisfies the specification and logarithmic scores are finite, the following holds exactly:

$$-\log_2 q_\sigma(x_i\vert C_i,\sigma_{F_i}) =-\log_2 q_0(x_i\vert C_i)+\log_2 Z_0(F_i,C_i),$$

Hence:

$$\Delta_\sigma =\frac{1}{\vert D_\sigma\vert } \sum_{i\in D_\sigma} \left[-\log_2 Z_0(F_i,C_i)\right]\geq0.$$

The quantity expresses the **logarithmic selectivity of the specification** relative to $q_0$, in bits. It is the negative logarithm of the mass that the context model assigns to the admissible set; mass outside that set is $1-Z_0$. When the label has been assigned by applying the same specification to the same realisation, non-negativity follows by construction.

Reporting also includes the number and proportion of independently annotated occurrences outside the specification, ambiguous cases, and coverage of $D_\sigma$. Every term in the decomposition is computed on the same subset. Evaluation on the full $D$ is reported separately.

### Within-family preference on the same admissible set

A comparison of frequencies within the family also evaluates the family model on the same set:

$$Z_F(F,C)= \sum_{x\in\mathcal X(\sigma_F,C)}q_F(x\vert F,C), \qquad r_F(x\vert F,C,\sigma_F)= \frac{q_F(x\vert F,C)\,\mathbf 1\lbrace x\in\mathcal X(\sigma_F,C)\rbrace } {Z_F(F,C)}.$$

For $Z_F\gt 0$, define the separate descriptive quantity:

$$\Delta_{\mathrm{pref}} =\mathrm{CE}(q_\sigma)-\mathrm{CE}(r_F).$$

$\Delta_{\mathrm{pref}}$ measures whether learned relative frequencies predict independent compatible realisations better than the relative frequencies of $q_0$. For the general family model:

$$\Delta_{F\vert\sigma} =\Delta_{\mathrm{pref}} +\frac{1}{\vert D_\sigma\vert } \sum_{i\in D_\sigma}\log_2 Z_F(F_i,C_i).$$

The residual therefore also includes the effect of the mass that $q_F$ places outside the admissible set. When $q_F$ is constructed so that $Z_F=1$, then $\Delta_{F\vert\sigma}=\Delta_{\mathrm{pref}}$. Interpreting preference in compositional terms is further supported by corpus composition, compositional provenance and control of context.

### Full support and reporting unit

Evaluation of occurrences outside the specification can use a predeclared smoothing scheme:

$$q_{\sigma,\epsilon}=(1-\epsilon)q_\sigma+\epsilon q_0, \qquad 0\lt \epsilon\lt 1.$$

$\epsilon$ is selected on development material. Smoothing provides positive probability wherever $q_0$ is positive; the score is calculated from the mixture itself. The simple $-\log_2 Z_0$ identity applies to strict truncation on $D_\sigma$. Cases with $Z_0=0$ or $Z_F=0$ are recorded as coverage failures, with a predefined fallback procedure.

This page uses bits per realisation. Normalisation in the separate technical appendix, in bits per atomic event, uses denominator $\sum_{i\in D_\sigma}L_i$ instead of $\vert D_\sigma\vert$. The identities are preserved when the denominator changes identically in every term; numerical quantities are reported with their units.

Positive $\Delta_{\mathrm{family}}$ establishes lower mean logarithmic loss for the family model on the declared set. Label provenance, specification coverage and the separate comparison of within-family frequencies determine the scientific content of this benefit. The [revision review (Greek)](../../../docs/maintenance/position-family-review-2026-10-23.md) records correspondence with T6.3 of the technical appendix.

## Relation to historical recovery

Realisation prediction and historical recovery are connected through forward probabilistic channels. The operator describes realisation conditional on family and context; the historical channel connects the old label to the exegesis.

Recovery of the old notation requires a dedicated historical channel $p_\phi(X_G\vert H,M,Z)$, where $H$ is the independently read old label and $M$ the metrophonic class. The following Bayesian inversion uses the exegesis, metrophonic class and context to return a distribution over possible historical labels:

$$p_\phi(H\vert X_G,M,Z)= \frac{p_\phi(X_G\vert H,M,Z)\,p(H\vert M,Z)} {\sum_{h\in\mathcal H(M,Z)} p_\phi(X_G\vert h,M,Z)\,p(h\vert M,Z)}.$$

The related forward formulations allow shared design of alignments, boundaries and context encoding. The historical label $H$, estimation of the inverse channel and the test set remain specific to [ATL-INV](inverse-problem.md). The relation between the operator and the inverse problem is thus a concrete mathematical bridge yielding two distinct research results.

## Sources of the development

The initial pilot pathway and neural extension correspond to the [probabilistic realisation source (Greek)](../../../sources/proposal-v878-candidate.tex#L793). Additional definitions of truncation, preference and smoothing are recorded in the [review of mathematical assumptions (Greek)](../../../docs/maintenance/position-family-review-2026-10-23.md). The [document and protocol correspondence](../reference.md) brings together their editorial provenance.
