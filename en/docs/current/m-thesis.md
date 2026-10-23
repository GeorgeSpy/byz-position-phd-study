# The probabilistic operator Mθέσις

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/current/m-thesis.md) · **English** · [Translation progress](../translation-status.md)
<!-- language-switch:end -->

[Methodological map](index.md) · [Formula and family](position-and-family.md) · [ATL](atl.md) · [Inverse problem](inverse-problem.md)

$`M_{\mathrm{θέσις}}`$ asks whether knowing a melodic formula's family improves prediction of its written realisations once modal, prosodic and local context has been taken into account. It measures the predictive benefit of family information, assessing specification selectivity and the empirical distribution of forms separately.

## What is new in Mθέσις

The operator investigates **which realisations characterise a family and how they change with musical context**. The musicological specification identifies compatible forms; the study of practice identifies preferred forms and their frequencies.

The new knowledge concerns three questions:

- **Which internal changes are organised by the family?** The model tests whether family identity improves prediction of extent, density, temporal organisation and syllabic application.
- **Which forms are preferred within the admissible space?** The comparison distinguishes how selective the specification is from which compatible forms characterise the corpus.
- **How does typicality relate to musical interpretation?** Common and rare realisations are returned to their passages and considered alongside independent judgements of acceptability.

The contribution is a predictive account of **how a melodic formula is realised**. Musicologists gain a way to investigate how modal and textual context relates to its characteristic forms, and where a composer's distinctive realisation lies. [Contribution to the research as a whole](../review/knowledge-contributions.md#specification-selectivity-and-preference-in-practice).

## Context and family

Context describes the modal, prosodic and local conditions of a passage. The family adds the information that the passage belongs to a specific analytical category, with its own diagnostic relations and admissible alternatives. Comparing predictions with and without this information measures what family identity contributes to the prediction of form.

## Definition and variables

Let $`F`$ be the family, $`C`$ the admissible modal, prosodic and local context, and $`X`$ the particular symbolic realisation at a declared level of analysis. The operator is defined as a stochastic kernel:

```math
M_{\mathrm{θέσις}}:(F,C)\longmapsto
\mathcal P(\mathcal X),\qquad
M_{\mathrm{θέσις}}(F,C)[X=x]=p_\theta(x\mid F,C).
```

Here $`\mathcal X`$ is the space of eligible sequences and $`\mathcal P(\mathcal X)`$ the space of distributions over them. For a discrete space, $`\sum_{x\in\mathcal X}p_\theta(x\mid F,C)=1`$. The set $`\mathcal X(\sigma_F,C)\subseteq\mathcal X`$ of realisations permitted by the specification is defined separately. $`F`$ comes from a finalised family specification and $`C`$ from context recorded before prediction. Ambiguous but admissible readings retain their alternatives rather than being forced into an arbitrary single label.

A distribution has musical significance. A formula can retain its family organisation while the extent of its development, internal density, syllabic application and cadence vary. Estimating $`p_\theta`$ retains this multiplicity and allows a particular form to be characterised as common or rare relative to a declared reference corpus. The quantity $`-\log_2 p_\theta(x\mid F,C)`$ describes **predictive typicality**, while musicological acceptability is assessed through independent expert judgements.

## The first testable quantity

The first generative evaluation compares two models: $`q_0(x\mid C)`$, which knows the context, and $`q_F(x\mid F,C)`$, which also knows the family. It measures the additional predictive benefit of family information under shared available conditions. Label provenance determines whether the use is descriptive or prospective.

For the same set of held-out works $`D_{\mathrm{test}}`$, define empirical cross-entropy:

```math
\widehat{\mathrm{CE}}_{D}(X\mid V;q)
=-\frac{1}{|D|}\sum_{i\in D}\log_2 q(x_i\mid v_i),
\qquad
\Delta_{\mathrm{family}}
=\widehat{\mathrm{CE}}_{D}(X\mid C;q_0)
-\widehat{\mathrm{CE}}_{D}(X\mid F,C;q_F).
```

Cross-entropy and $`\Delta_{\mathrm{family}}`$ are measured in bits per realisation, using base-2 logarithms. Predictive typicality above uses the same unit.

## What the evaluation distinguishes

Family benefit is examined at two levels: how much the specification restricts possible forms, and how well the model predicts relative frequencies within the admissible set. A comparison of preferences requires the same admissible set for both models. When the label was assigned by applying the specification to the same realisation, the benefit of excluding incompatible forms follows by construction. Empirical preferences are tested on independent compatible realisations; prospective prediction requires family information available outside the target.

The [technical note](m-thesis-technical.md) gives the full decomposition, normalisation and coverage conditions, the three uses of the label, and conversion to bits per atomic event.

## From family specification to prediction

| Stage | Content | Output |
|---|---|---|
| P0 | Register of diagnostic relations, scope and admissible alternatives. | Defined $`F,C,\mathcal X`$ and evidence roles. |
| P1 | Assessment of family identifiability and reading ambiguity. | The population in which the predictive contrast can be estimated. |
| P2 | Simple probabilistic models with and without $`F`$. | $`\Delta_{\mathrm{family}}`$, calibration and error analysis by family. |
| Extension | Neural decoder and tests of synthetic realisations. | A richer distribution assessed independently for musical acceptability. |

[Sources and mathematical development of the pilot pathway](m-thesis-technical.md#sources-of-the-development).

## Relation to historical recovery

Predicting realisations describes the possible written forms of a family. [Historical recovery](inverse-problem.md) additionally requires a channel connecting an exegesis to an independently read old label. The mathematical bridge is Bayesian inversion of this historical channel, with declared inputs and its own test set. [Full formulation](m-thesis-technical.md#relation-to-historical-recovery).
