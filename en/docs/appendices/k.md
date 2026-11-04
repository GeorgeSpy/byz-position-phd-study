# K · A2 — Technical protocol

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/appendices/k.md) · **English**
<!-- language-switch:end -->

[A2 research design](../research/a2-knowledge-design.md) · [Synthetic checks](../../../docs/research/a2/support/README.en.md) · [Revised M1](../research/m1-selection-decision.md) · [Revised M2](../research/m2-eise-research-design.md)

**Date:** 3 November 2026. **Status:** preregistrable technical protocol. The mathematical checks and the synthetic design checks have been run; no model has been trained on the real corpus. This revision replaces the previous one, of 27 October 2026. Acceptance of the real perturbation set, calibration of the statistical procedure and confirmatory status are decided in WP0, before the independent test set H is opened. The Greek text is the reference version.

This appendix is the companion A2 technical protocol cited by the [core research plan](../../../documents/core-research-plan.tex): §§3–10 there correspond to §§K.3–K.10. The [design page](../research/a2-knowledge-design.md) explains the question and the rationale. This appendix defines the scores, the generator, the estimands, the splits, the statistical procedure and the records. The synthetic checks behind the decisions of this revision are in [`docs/research/a2/support/`](../../../docs/research/a2/support/README.en.md).

**In this appendix**

- [K.0 · Changes from the previous revision](#k0--changes-from-the-previous-revision)
- [K.1 · Question, population and units](#k1--question-population-and-units)
- [K.2 · Data and independent judgement](#k2--data-and-independent-judgement)
- [K.3 · Shared input, bases and model family](#k3--shared-input-bases-and-model-family)
- [K.4 · Probabilistic model and training](#k4--probabilistic-model-and-training)
- [K.5 · Perturbations and the non-equivalence certificate](#k5--perturbations-and-the-non-equivalence-certificate)
- [K.6 · Estimands and metrics](#k6--estimands-and-metrics)
- [K.7 · Splits, selection and computational budget](#k7--splits-selection-and-computational-budget)
- [K.8 · Statistical procedure and multiplicity](#k8--statistical-procedure-and-multiplicity)
- [K.9 · Link to M1 and M2](#k9--link-to-m1-and-m2)
- [K.10 · Criteria, fallbacks and timeline](#k10--criteria-fallbacks-and-timeline)
- [K.11 · Reproducibility and sources](#k11--reproducibility-and-sources)

## K.0 · Changes from the previous revision

1. **Five bases.** Each replicate $r=1,\dots,5$ has its own base $b_r$ and temperature $T_r$, shared by the conditions and by $B_K$ within the replicate (§K.3).
2. **Heads on the internal development set.** $(w,\lambda)$ and the head of $B_K$ are fitted on the internal development groups $\mathcal{D} _ {\mathrm{int}}$, where the temperature is also fitted. The base is trained on the separate groups $\mathcal{D} _ {\mathrm{base}}$ (§K.3, §K.7).
3. **$\lambda$.** It remains $\lambda\in[0,2]$, with $\lambda=0$ feasible. The distribution of $\hat{\lambda}$ and the frequencies at both ends are reported. The certificate $d_D$ covers exactly this interval (§K.5).
4. **Generator.** A constrained sampler of bijective mappings. The canonical card of every family must change. Uniqueness is checked on the canonical form of the bank and on the function $(Q,v)$. Satisfiability requires a witness with $\phi=1$. LP certificates are accepted only with checked residuals and a conservative dual lower bound. The termination reason is recorded (§K.5).
5. **Statistical procedure.** The primary candidate procedure is the jackknife standard error with a Student $t(G-1)$ reference distribution. The bootstrap-t becomes a sensitivity analysis. Confirmatory use requires successful calibration in WP0 before H (§K.8).
6. **Composition of H.** H is designed for family coverage. Presence of every family in at least two groups is necessary, not sufficient (§K.7).
7. **Operating-characteristics study.** Null hypotheses are constructed exactly. Reference values and Monte Carlo datasets use independent random streams. Denominators are reported separately. The study also runs the algorithm that allocates groups to H. The warp-speed method is used only for exploration, and critical calibrations run the full procedure (§K.8).
8. **Supportive relations.** They stay outside $Q$ and $\phi$ until the WP0 decision. An example is the neumatic patterns of the kylisma (§K.3).
9. **Link to M1.** $R^\star$ is selected with rule J in architecture A. The encoder is preselected between TCN-S and BiGRU. The names of the M2 reference models ($\mathrm{B0_{sym}}$, $\mathrm{B0_{profile}}$, B1, $\mathrm{B2_{fam}}$, $\mathrm{B2_{main}}$) are kept distinct from the A2 comparators $B_K$ and $B^\star$ (§K.9). The timeline includes M5-min (§K.10).
10. **Metric names.** $F1_{\mathrm{seg+fam}}$ denotes exact joint recognition of boundaries and family and $F1_{\mathrm{bnd}}$ boundaries only, as in M1 (§K.6).

## K.1 · Question, population and units

A2 measures (a) the mean effect of valid family relations against a specific, controlled set of perturbed assignments and (b) the added benefit of an explicit logical composition when the relations are valid. The domain is the occurrences of melodic formulae (theseis) in complete papadic Cherubic hymns and Koinonika of the New Method. A family is a documented analytical category, and membership of an occurrence is judged independently of the mechanical application of the rule.

The unit of independence is the component of the work–source kinship graph. Edges come from every shared historical passage, co-exegesis, copy, near-identical edition or other dependence that can carry the same musical evidence. All connected records belong to the same group. Occurrences, training replicates and cross-validation folds are not independent replications. The group catalogue is finalised before any split, and large components are not cut to inflate $G$ artificially.

The primary AP refers to the population of occurrences produced by this sampling of works: equal weight per occurrence and a mean over the prespecified families. Large works therefore contribute more occurrences. The sensitivity analysis with weight $1/n_g$ per occurrence, giving every group equal weight, estimates a different quantity and is reported separately.

## K.2 · Data and independent judgement

The tables `works(group_id, work_id, source, mode, licence)`, `events(work_id, t, N, T, M, L)`, `occurrences(id, work_id, family, status, accepted_bounds)`, `concepts(segment_id, concept_id, value, observed, reason)` and `specifications(family, role, group_id, concept_id, version)` are required, together with separate split files. Identifiers are not used as features. Every change is recorded with a hash and a reason.

M3a has two distinct phases. In the first, experts judge boundaries and family without access to the specifications $\sigma$ or to predictions; these judgements provide the evaluation labels. In the second, they check the applicability of the $\sigma$. The initial judgements and disagreements are kept. "Unresolved" is excluded from the primary family AP, recorded separately and never turned into a negative example. The unknown family $\varnothing$ is a distinct, positively documented category. The experts' school and experience and agreement per kind of decision are recorded, not just one overall $\kappa$.

Every candidate segment $s=[a,b]$ is mapped to the shared scale of atomic events. All conditions see exactly the same candidate set, the same maximum length and the same admissible endpoints. The maximum length comes from development data and is finalised before H. Candidate recall with respect to the accepted boundaries (oracle recall) is reported overall and per family.

Concepts are extracted from the admissible symbolic input for **every** $s$ and every candidate family $f$. Deterministic extractors are error-checked in the pilot. Learned extractors are trained only on the groups $\mathcal{D} _ {\mathrm{base}}$ and give out-of-sample predictions on $\mathcal{D} _ {\mathrm{int}}$ and on H. Manual concept marking on H is used only to evaluate the extractors. No extractor receives the label, the work name or the confirmed family.

## K.3 · Shared input, bases and model family

### Concept table

For each $s$ the shared bank has values $c_j\in\lbrace 0,1,?\rbrace$ and observability masks $m_j$. For each specification $\sigma_f^K$, $K\in\lbrace V,P\rbrace$, the full table

$$
T_f^K(s)=\lbrace (j,c_j,m_j,r_j,g_j):j\text{ appears in }\sigma_f^K\rbrace
$$

is built, with concept identity, value, observability, role $r_j\in\lbrace R,A,E\rbrace$ and alternative-group identity $g_j$. $F$ and $D$ receive the same table in the same order. $F$ does not receive a ready-made final logical decision. The difference is the admissible composition function: $F$ is constrained additive, while $D$ adds a specific interaction. The same input does not mean that the two internal functions retain the same information.

**Supportive relations.** The specification cards also record relations that strengthen a membership without imposing it. An example is the neumatic patterns of the kylisma. These relations do not enter $Q$ and $\phi$ in the main analysis. Their status is decided in WP0, before the specifications are finalised: inclusion as required or alternative relations, a separate descriptive analysis, or remaining on the card only.

### Five bases

For each replicate $r=1,\dots,5$, the base score $b_r(s,f)=b_{\hat{\psi} _ r}(s,f)$, which also covers the unknown $f=\varnothing$, is trained without $\sigma$ on the groups $\mathcal{D} _ {\mathrm{base}}$. It uses the selected configuration `A_M1_selected` on $R^\star$, with initialisation and data order $r$. The temperature $T_r$ is fitted on the internal development groups $\mathcal{D} _ {\mathrm{int}}$. The parameters of $b_r$, the transitions and $T_r$ are finalised **jointly** before the conditions of the replicate. The four conditions and $B_K$ of replicate $r$ share $b_r/T_r$. $B^\star$ uses the same initialisation $r$. No condition-specific calibration or per-family bias term is added to the main conditions, so that a new neural branch cannot cancel the intervention. The base may already know part of the family structure; the result concerns the added benefit on top of it.

### Role summaries

Let $q_j=2c_j-1$ for observed literals of roles R and A, $q_j=1-2c_j$ for observed literals of E and $q_j=0$ when $c_j=?$. Denominators include all literals, so that missingness does not inflate the mean of the rest:

$$
Q_R=|R|^{-1}\sum_{j\in R}q_j,\qquad Q_A=|\mathcal{G}|^{-1}\sum_{G\in\mathcal{G}}|G|^{-1}\sum_{j\in G}q_j,\qquad Q_E=|E|^{-1}\sum_{j\in E}q_j .
$$

Then $Q_f^K=(Q_R,Q_A,Q_E)\in[-1,1]^3$. An empty role gives 0 and empty alternative groups are excluded. Let $W=\lbrace w:\sum_rw_r=1,\ w_r\ge0.1\rbrace$. The three shared weights are fitted with common bounds and a common procedure for all families. The scale of the term is fixed, $\beta=1$ in units of the finalised log-score. This commitment defines the size of the intervention explicitly and testably and does not allow it to be zeroed or reversed. The knowledge term of $F$ compresses information that $\phi$ keeps. For $\phi=(a\vee b)\wedge(c\vee d)$, the states $(1,1,0,0)$ and $(1,0,1,0)$ have the same $Q_A=0$, while the first violates the rule ($\phi=0$) and the second satisfies it ($\phi=1$). The additive knowledge term $w^\top Q$ of $F$ is the same in both states; the base score $b_r$ may already distinguish them. Prespecified descriptive sensitivities are $\beta\in\lbrace 0.5,\thinspace 2\rbrace$, a lower weight bound of 0 instead of 0.1, and complete removal of the term. $\beta$ is not selected on H.

### Logical rule

$$
\phi_f^K=\bigwedge_{j\in R}c_j\ \wedge\ \bigwedge_{G\in\mathcal{G}}\bigvee_{j\in G}c_j\ \wedge\ \bigwedge_{j\in E}\neg c_j .
$$

$\phi$ is computed with Kleene's strong three-valued logic: $0\wedge?=0$, $1\wedge?=?$, $1\vee?=1$, $0\vee?=?$, $\neg?=?$. The main penalty is $v_f^K=\mathbf{1}[\phi_f^K=0]$. An unknown truth value gives zero penalty, because it documents no violation, and is not equated with an absent feature. This policy may favour incomplete evidence. Performance and abstention are therefore reported per level of observability, together with a sensitivity with $\lambda_?=\lambda/2$ for $\phi=?$, without changing the main definition.

### The six conditions

| Condition | Score of a known $f$ in replicate $r$ | Fitted parameters | Knowledge input |
|---|---|---|---|
| $F,V$ | $b_r/T_r+w^\top Q_f^V$ | $w\in W$ | full $T_f^V$ |
| $F,P_l$ | $b_r/T_r+w^\top Q_f^{P_l}$ | $w\in W$, separate fit with the same procedure | full $T_f^{P_l}$ |
| $D,V$ | $b_r/T_r+w^\top Q_f^V-\lambda v_f^V$ | $w\in W$, $\lambda\in[0,2]$ | same $T_f^V$ |
| $D,P_l$ | $b_r/T_r+w^\top Q_f^{P_l}-\lambda v_f^{P_l}$ | $w\in W$, $\lambda\in[0,2]$ | same $T_f^{P_l}$ |
| $B_K$ | $b_r/T_r+a_f^\top[c^0,m]+d_f$ | free $a_f,d_f$, shared prespecified L2 | same concept bank, without $\sigma$ or roles |
| $B^\star$ | $u_f^\top h_\theta(s)+d_f+\gamma\cos(z_\theta(s),\mu_f)+a_f^\top[c^0,m]$ | $\theta,u,d,a,\gamma$ and concept head | same bank and supervision, without $\sigma$ |

The parameters of the four main conditions and of $B_K$ are fitted on $\mathcal{D} _ {\mathrm{int}}$; $B^\star$ follows the allocation described below. Here $c^0_j=m_jc_j$, with zero in the unobserved part. In the four main conditions the unknown family has score $b_r(s,\varnothing)/T_r$, without $Q$ or $v$. In $B_K$ it also has a fitted linear head. In $B^\star$ it has $u_\varnothing,d_\varnothing$, without a prototype. The $\mu_f$ are normalised means of training representations, updated only from training data and finalised before prediction. $B^\star$ trains its representation on the groups $\mathcal{D} _ {\mathrm{base}}$ and uses $\mathcal{D} _ {\mathrm{int}}$ for its declared selection and temperature. It uses the same data, the same initial pre-training, the same admissible input and the same search budget. Its additional capacity is declared: it is a strong external comparator and not a clean factorial ablation.

$B^\star$ minimises $L_{\mathrm{seg}}+\alpha L_{\mathrm{fam}}+\beta_cL_{\mathrm{concept}}+\beta_rL_{\mathrm{rec}}+\beta_sL_{\mathrm{SupCon}}$. $L_{\mathrm{concept}}$ is a masked binary cross-entropy on the same training concept targets that are available to the base of the main conditions. The supervised contrastive loss includes positives from other works and a denominator with all admissible positives and negatives:

$$
L_{\mathrm{SupCon}}=-\sum_i\frac1{|P(i)|}\sum_{p\in P(i)}\log\frac{\exp(z_i^\top z_p/\tau)}{\sum_{a\ne i}\exp(z_i^\top z_a/\tau)} .
$$

Samples without a positive are skipped and their frequency is recorded. The simple attraction of positive pairs in $\mathrm{B2_{fam}}$ of M2 is not called SupCon. $B^\star$ may reuse the pair-encoding code of $\mathrm{B2_{fam}}$, with an explicitly different objective.

### What is isolated

The main estimate concerns constrained families of scoring functions on a finalised representation, given the concept bank and the perturbation set. It does not prove uniqueness of the neural mechanism or a general inability of neural encoders to learn the same relations. A secondary quartet of conditions allows end-to-end training with the same budget. There the practical usefulness of the inductive bias is measured, not certified non-absorption of the knowledge. The reparametrisation $h_P=h_V+g_V-g_P$ shows why the two claims must be kept apart.

## K.4 · Probabilistic model and training

The normalised prediction for a known $s$ is $p(f\mid s)=\mathrm{softmax} _ f\thinspace \ell(s,f)$, over all known families and the unknown one. No choice of $\sigma_y$ is made before scoring.

For joint segmentation and recognition, $Y$ is a set of non-overlapping labelled segments. Uncovered positions are represented by unique skip steps, so that the same $Y$ is not counted more than once. With finalised transitions $a$ and skip scores $\kappa$:

$$
E(Y)=\sum_{(s,f)\in Y}\ell(s,f)+\sum a(f_{\mathrm{prev}},f)+\sum_{t\in\mathrm{skip}(Y)}\kappa_t,\qquad Z(X)=\sum_{Y\in\mathcal{Y}(X)}e^{E(Y)},
$$

$$
L_{\mathrm{partial}}=\log Z(X)-\log\sum_{Y\in\mathcal{Y} _ {\mathrm{obs}}(X)}e^{E(Y)} .
$$

$\mathcal{Y} _ {\mathrm{obs}}$ contains all compatible annotations and accepted boundaries, exactly once per complete path. The sum is computed by forward dynamic programming in log space, with a previous-label state where transitions exist. The maximum length keeps the space finite. Overlapping analytical readings are recorded as alternative paths and not as simultaneous, incompatible reference segments.

The heads $(w,\lambda)$ are fitted with this partially annotated likelihood on the sequences of $\mathcal{D} _ {\mathrm{int}}$, on the finalised $b_r/T_r$. The penalty $-\lambda v$ appears in both numerator and denominator. Then $\partial L_{\mathrm{partial}}/\partial\lambda=\mathbb{E} _ {Y\mid\mathrm{obs}}[V(Y)]-\mathbb{E} _ Y[V(Y)]$; for a known family, $\partial L/\partial\lambda=v_y-\sum_fp_fv_f$. A fixed, non-parametric penalty added only to the final loss does not change the gradient with respect to the scores. Checks T14–T16 test finite differences, enumeration of 39 paths and equality with the dynamic-programming partition function.

For each $(r,K)$ and each $P_l$, $\hat{\lambda}$, its dispersion, the share with $\hat{\lambda}\lt 0.1$ and the frequency of $\hat{\lambda}=2$ are reported. The frequency at the upper bound is reported without changing the interval. A nearly inactive penalty ($\hat{\lambda}$ near 0) and an active penalty without benefit on H are different outcomes and are interpreted separately. In the synthetic checks, heads on $\mathcal{D} _ {\mathrm{int}}$ had a median $\hat{\lambda}$ of 1.70–1.71 and a standard deviation of 0.30. They reached the upper bound in 12–13% of fits, and no estimate was below 0.1.

The prediction-only version of $D$ is obtained from the fitted $F$ by adding $-\lambda v$ at prediction only. Its $\lambda$ is chosen by grouped cross-validation within $\mathcal{D} _ {\mathrm{int}}$. It is compared descriptively with the fitted $D$. In the main estimator the difference concerns head training and not a change of representation. If all $v$ are equal for all candidates, the effect cancels in the softmax; real activation checks are therefore required.

### Small diagnostics of the operator and the scale

Two descriptive ablations are added for the valid V, with the same finalised base and one extra $\lambda\in[0,2]$:

- $D_{\mathrm{count}}=b+w^\top Q-\lambda\nu$, where $\nu$ is the number of violated literals divided by their number, with no penalty for unknowns;
- $D_{\mathrm{nl}}=b+w^\top Q-\lambda g(Q)$, with $g(Q)=[(Q_R+Q_A+Q_E)/3]^2$.

The second has a non-linear basis and the same number of extra parameters, without the composition of $\phi$. If $D$ only improves on $F$, the result concerns that additive basis and inductive structure. The comparison with $D_{\mathrm{nl}}$ shows descriptively how specific the benefit is to the musicological logic. $\lambda=0$, $\beta=0$ and the prediction-only version remain negative and mechanistic checks. The ablations add cost outside the 120 main fits.

Penalising constraint violations inside a structured model has a direct precedent in constrained conditional models (Chang, Ratinov and Roth, 2012). A2 does not present the form of the penalty as new. It tests experimentally whether the penalty, with valid and with perturbed musicological content, adds information on top of the additive use of the same concepts.

## K.5 · Perturbations and the non-equivalence certificate

The perturbation set has ten different banks $P_1,\dots,P_{10}$, shared by $F$ and $D$ and by all replicates. The need for controlled perturbations is documented outside music too: models that use knowledge graphs can perform almost as well with heavily perturbed graphs (Raman et al., 2021).

### Generator

Each $P_l$ results from a universal bijective mapping $\tau$ of concept identities. $\tau$ is applied to all families, preserving roles, alternative-group sizes, the concept–family incidence graph, family intersections and concept multiplicities. Extraction types and modal constraints define the admissible permutation classes. The values of a categorical variable are permuted only among themselves. Binary concepts are permuted within the class of their type. No arbitrary reversal of exclusions is required.

$\tau$ does not come from a uniform permutation checked afterwards. In the synthetic checks uniform permutations almost never met the tolerance. A constrained sampler is used: for each used concept $j$, the image $\tau(j)$ is drawn at random among the free concepts of the same class with

$$
|\pi_{\tau(j)}-\pi_j|\le0.10,\qquad|\mu_{\tau(j)}-\mu_j|\le0.10,
$$

where $\pi$ is the presence frequency and $\mu$ the missingness rate. Both are computed on development data without labels. The remaining concepts of the class are mapped at random. The proposal distribution and the seed are finalised in WP0, before any model performance is seen. The tolerance 0.10 is an initial declared rule and not a scientific law. Changing it after the pilot creates a new preregistered version before main training.

### Acceptance

A proposal is accepted only if it satisfies, in this order:

1. the frequency and missingness tolerance for every used concept;
2. **minimum change:** the canonical card of every family differs from its card in V; a swap inside one alternative group or within one role does not count as a change, even when another family changes;
3. **canonical uniqueness:** the canonical form of the bank differs from V and from the already accepted P; in canonical form, literals are sorted within each role and each alternative group, and groups are sorted among themselves;
4. **satisfaction witness:** for every family there is a state of $\Omega$ with $\phi=1$; $\phi=?$ is not enough;
5. **activation:** for every family there is a state of $\Omega$ with $\phi=0$;
6. **functional uniqueness:** $(Q,v)$ on $\Omega$ differ from those of V and of the already accepted P;
7. **certificate:** verified $d_F$ and $d_D$, as defined below;
8. **non-synonymy:** expert documentation that the substitution is not synonymous or a trivial rewording; low correlation does not by itself prove a different musical meaning.

$\Omega$ is the set of distinct concept states observed in development data, without labels. All rejections are recorded by cause. The number of **immovable families** is also recorded: families with no literal that has a compatible alternative image. An immovable family makes the minimum-change rule infeasible regardless of the sampler; the bank is declared infeasible immediately. A plain file diff or a Hamming-distance check is not enough.

### Certificate

On the states of $\Omega$ the matrices $Q_V,Q_P$ and the columns $v_V,v_P$ are formed. Because the unknown family is unchanged, rows express differences between a known family and the unknown one, which removes the indeterminacy of a common additive softmax shift. The linear programmes are

$$
d_F=\min_{w,w'\in W}\Vert Q_Vw-Q_Pw'\Vert_\infty ,
$$

$$
d_D=\min_{w,w'\in W,\ \lambda,\lambda'\in[0,2]}\Vert Q_Vw-\lambda v_V-Q_Pw'+\lambda'v_P\Vert_\infty .
$$

The certificate covers exactly the family of heads that is fitted: $W$ with lower bound 0.1 and $\lambda\in[0,2]$. Because $\lambda=\lambda'=0$ is feasible, $d_D\le d_F$; both are reported. Changing $W$ or the interval of $\lambda$ requires a new computation. A certificate is accepted only if all of the following hold: the solver terminated successfully and all quantities are finite; the maximum primal feasibility residual, the dual residual and the duality gap are at most $10^{-8}$; the conservative dual lower bound exceeds $10^{-6}$. The dual residual covers stationarity and the signs of the multipliers. The conservative bound is the dual objective minus the $\ell_1$ norm of the stationarity residual times a bound on the variables over the feasible box: weights in $[0.1,\ 0.8]$, $\lambda$ in $[0,2]$ and $t$ up to $\max_i\sum_j|A_{ij}|x^{\max} _ j$. For each acceptance the residuals, the bound, the solver, its version, the tolerances and the witnesses are recorded. A positive lower bound certifies non-overlapping scoring classes on the given state space. A zero value means failure of this strong criterion, not proof of universal equivalence. For few concepts full enumeration is used; for more, certified feasible witnesses or MILP with recorded gap and tolerance. Infeasible combinations are not accepted as musical evidence.

### Feasibility and stopping

The example of the previous revision, with primal and dual checks, gives $d_F=d_D=0.8$; the identity mapping gives $d_F=0$. In 16 synthetic banks, with uniform choice among the compatible images, the constrained sampler found ten accepted P in 10 of the 11 banks without an immovable family, with 16–191 proposals. None of the 5 banks with an immovable family succeeded. LP residuals and duality gaps were below $10^{-14}$ and the smallest conservative dual bound was 0.1. The bank without an immovable family that failed exhausted the 100,000 proposals with nine accepted P. A preference for non-identity images did not improve feasibility and increased duplicate proposals in the poor banks; the main setting is therefore uniform choice ([results](../../../docs/research/a2/support/README.en.md)). These checks do not prove that ten such P exist in the corpus. All checks are repeated in the real pilot. If ten accepted P are not found within the prespecified limit of 100,000 proposals, confirmatory A2 stops. The termination reason is recorded separately: target reached, 100,000 proposals exhausted, or proven infeasibility because of an immovable family. The time limit of the synthetic checks is a practical limit of the simulation and does not replace the proposal limit. The available comparisons are reported descriptively and M1, M2 and M3a continue as planned. The model family and the acceptance rules are not relaxed silently.

No label-dependent acceptance filter is applied, such as requiring a drop in AP. Even on training data only, such a filter would define perturbations that are unfavourable to the labels by construction, and a different estimand. Correlations with training labels are reported as diagnostics after the set is finalised. The ten P are not exchangeable with the musicologically chosen V and do not constitute a randomisation null distribution. A universal $\tau$ can preserve the overall score distribution on a uniform Boolean cube; check T13 tests this symmetry.

## K.6 · Estimands and metrics

For each replicate $r=1,\dots,5$ the $\mathrm{AP_{fam}}$ is computed on the independent evaluation set. $S$ is the mean of these five values, not the AP of an ensemble of mean probabilities. For perturbations, $\bar S(C,P)=10^{-1}\sum_lS(C,P_l)$, where $C\in\lbrace F,D\rbrace$ is the mode of use. The ten P are crossed with all five replicates. The same base $b_r$ and the same data order are matched across conditions. The main estimand is conditional: given the finalised perturbation set, the trained bases and the prespecified evaluation distribution. It is not automatically an expectation over every possible perturbation or future training set.

$$
\Delta_{\mathrm{know}}=\tfrac12\lbrace S(D,V)-\bar S(D,P)+S(F,V)-\bar S(F,P)\rbrace,\qquad \Delta_{\mathrm{logic},V}=S(D,V)-S(F,V).
$$

Secondary quantities are $\Delta_{\mathrm{struct}}=\tfrac12\lbrace S(D,V)-S(F,V)+\bar S(D,P)-\bar S(F,P)\rbrace$ and $I=\lbrace S(D,V)-S(F,V)\rbrace -\lbrace \bar S(D,P)-\bar S(F,P)\rbrace$. The identity $\Delta_{\mathrm{logic},V}=\Delta_{\mathrm{struct}}+I/2$ keeps the factorial interpretation. $DP\approx FP$ is not assumed. A positive $\Delta_{\mathrm{know}}$ can arise from damage done by the P; for practical benefit $B_K$ is examined as well.

**$\mathrm{AP_{fam}}$.** For each real occurrence $i$ with a set of accepted boundaries $B_i$, the score of family $f$ is the arithmetic mean of $p(f\mid s)$ over $s\in B_i$. $B_i$ is set by independent experts and is common to all models. The occurrence counts once. Scores rank occurrences, separately for each $f$ (one against the rest), not families within the same occurrence. In each tie set all elements are inserted simultaneously:

$$
\mathrm{AP} _ f=\sum_k(R_k-R_{k-1})P_k,\qquad \mathrm{AP_{fam}}=|\mathcal{F} _ 0|^{-1}\sum_{f\in\mathcal{F} _ 0}\mathrm{AP} _ f ,
$$

where $k$ runs over successive tie sets and $R_k,P_k$ are recall and precision after inserting set $k$. The definition coincides with the scikit-learn implementation. The synthetic check `test_ap.py` confirms agreement with weights and ties. $\mathcal{F} _ 0$ is finalised from development data. Occurrences of other known families and documented unknowns are negatives for $f$. If positives of some $f$ are missing from the final evaluation, the full $\mathrm{AP_{fam}}$ is undefined; $f$ is not removed after the fact. The available subset and the estimative status are reported. The AP of a random ranking does not equal the prevalence exactly in every finite sample (T20).

**$F1_{\mathrm{seg+fam}}$.** This is exact joint recognition of boundaries and family, as in M1; $F1_{\mathrm{bnd}}$ concerns boundaries only. After decoding, a maximum bipartite matching between predictions and real occurrences is computed, one to one. An edge exists only if the family is correct and both endpoints equal some pair of $B_i$ on the shared atomic scale. TP is the size of the matching, FP the unmatched predictions and FN the unmatched real occurrences: $F1=2TP/(2TP+FP+FN)$. Exact matching comes first; tolerance $\pm1$ and IoU are separate sensitivities. Per-family recall is the mean of $TP_f/N_f$. $F1_{\mathrm{bnd}}$ matches independent endpoints with tolerance $\pm1$, one to one, with a common policy for work endpoints and for merging an end with the next start.

**Abstention and open set.** $\varnothing$ is a positive decision for an unknown family. Abstention signals insufficient certainty. The abstention threshold and the temperature are fitted on $\mathcal{D} _ {\mathrm{int}}$, with leave-one-family-out development for the open set and without using the unknowns of H. Reported are coverage (decisions without abstention over eligible cases), selective risk, the risk–coverage curve, AUROC and AUPRC of the unknown family with its prevalence, the false-unknown rate among known families and recall on unknowns. Not penalising $\varnothing$ does not keep its probability fixed: normalisation raises its share when the scores of known families fall (T18). Rejection of all $\sigma$ does not prove a musicologically unknown family.

## K.7 · Splits, selection and computational budget

1. **WP0.** Inventory of real groups, family coverage, extractors, training time and agreement. Before main performance is seen, $\mathcal{F} _ 0$, $r_{\min}$, substantive differences, group allocation and the design of H are finalised. The calibration of §K.8 is also run in WP0.
2. **Independent H.** If there are enough groups, H is defined in month 12 and stays closed. The main statistical confirmation concerns H only, after everything else is finalised. H is designed for **family coverage**: groups are allocated by stratified random allocation, using only the register of family presence per group and no model output, so that every family of $\mathcal{F} _ 0$ appears in at least $m_H$ groups of H. $m_H\ge2$ is necessary for the jackknife to be defined; it is not sufficient for power or coverage. The value of $m_H$ is set by the operating-characteristics study. The algorithm, the seed and the achieved coverage are recorded. A family that cannot be covered is removed from $\mathcal{F} _ 0$ before H, with a record, and analysed descriptively. Coverage of H must not leave $\mathcal{D} _ {\mathrm{base}}$ and $\mathcal{D} _ {\mathrm{int}}$ without enough families; $m_H$ and the minimum coverage of development are set jointly in the pilot. The primary AP refers to the prespecified evaluation distribution produced by this design. A different target population requires documented sampling or weighting and its own calibration.
3. **Development.** The remaining groups $\mathcal{D}$ are split by group into $\mathcal{D} _ {\mathrm{base}}$, for the base and the extractors, and $\mathcal{D} _ {\mathrm{int}}$, for temperature, heads, $B_K$, abstention and selection of $B^\star$. The ratio is set in WP0. Outer grouped cross-validation on $\mathcal{D}$ estimates the selection procedure. Within each outer training set, inner grouped validation covers the selection of $R^\star$, hyperparameters, calibration, extractors, specifications and P, where these depend on data.
4. **Without H.** If reserving H removes critical coverage, estimation-first nested grouped cross-validation is used. Pooled out-of-fold AP and per-fold AP are reported together with calibration and frequencies. Overlapping training sets are not treated as independent samples. Any bootstrap of the whole pipeline requires retraining and its own validation; it is not replaced by resampling the finished out-of-fold scores.
5. **Same training conditions.** The same split manifests, candidates, minibatches and supervision. A common constrained optimiser and the same multiple starting points for the heads, with convergence and KKT residuals recorded. The partially annotated likelihood can be non-convex; residuals do not prove a global optimum. The LP certificates are independent of this difficulty. No condition gets different early-stopping margins. An equal search is prespecified, e.g. eight trials per condition for a shared L2 and optimiser, with $\lambda\in[0,2]$. If the head is solved directly, eight different models are not created artificially. Nothing is selected to maximise the contrast on H.
6. **Budget.** Per final split: $2\times5$ valid fits, $2\times10\times5$ perturbed fits and $2\times5$ external comparators, **120** in total. Most are small heads on a finalised base. The five bases $b_r$, pre-training, M1, tuning, sensitivities and $B^\star$ are counted separately. Time and GPU memory are measured in the real pilot. 120 is a number of fits, not an estimate of days.

The heads are fitted on $\mathcal{D} _ {\mathrm{int}}$ and not on the base's training groups. In synthetic checks with grouped splits, fitting on the base's groups underestimated $\lambda$, with a median of 1.27–1.36 against 1.70–1.71. It also slightly reduced $\Delta_{\mathrm{logic}}$ on H. Grouped cross-fitting with a consistent temperature gave a similar $\hat{\lambda}$, at five times the base training cost. It is a separate sensitivity: at prediction it combines the five fold models, and the combination itself changes the scores.

## K.8 · Statistical procedure and multiplicity

The primary null hypotheses are $H_1:\Delta_{\mathrm{know}}\le0$ and $H_2:\Delta_{\mathrm{logic},V}\le0$. Directional tests are prespecified at an overall level $\alpha=0.025$ for the family of tests, with Holm's correction: the smaller $p$ is compared with 0.0125 and, if rejected, the other with 0.025. A one-sided 0.025 is not treated as generally equivalent to every two-sided 0.05 procedure.

If **both** are rejected, a secondary Holm family opens at the same $\alpha$: $H_3:S(D,V)-S(B_K)\le0$ and $H_4:S(D,V)-S(B^\star)\le0$. Both are superiority tests; no arbitrary non-inferiority margin is invented. If a musicologically documented $\delta_{\mathrm{NI}}$ exists before registration, a different version $H_4:\text{difference}\le-\delta_{\mathrm{NI}}$ can be defined, with documentation of practical benefit and cost; it does not change after results. The two external comparisons are reported descriptively regardless of the gate.

The sequence controls the FWER at 0.025 in the strong sense provided every individual $p$ is valid. If there is a true null in the first family, any opening of the second already presupposes an error controlled by the first Holm. If all first-family nulls are false, the risk comes from the second Holm. Independence of the $p$ is not required. Check T25 tests only the access logic, not the stochastic validity of the $p$. The interaction, hard cases, the end-to-end quartet and probing classifiers are descriptive, without FWER control.

### Primary candidate uncertainty procedure on H

The primary candidate procedure uses the pooled $\mathrm{AP_{fam}}$ on a fixed $\mathcal{F} _ 0$, equal weight per occurrence and a mean over families. For each primary contrast $\theta$, the original estimate and the delete-one-group standard error over independent work–source groups are computed:

$$
\hat{\theta} = \theta(\text{all } G \text{ groups}), \qquad \hat{\theta} _ {(-g)} = \theta(\text{all except } g), \qquad \bar{\theta} _ {(\cdot)} = \frac{1}{G}\sum_{g=1}^G \hat{\theta} _ {(-g)},,
$$

$$
\mathrm{SE} _ J = \Big[\frac{G-1}{G}\sum_{g=1}^G \big(\hat{\theta} _ {(-g)} - \bar{\theta} _ {(\cdot)}\big)^2\Big]^{1/2}, \qquad T = \frac{\hat{\theta}}{\mathrm{SE} _ J}, \qquad p = 1 - F_{t,G-1}(T).
$$

The numerator is the original estimate $\hat{\theta}$; it is neither the mean $\bar{\theta} _ {(\cdot)}$ nor the bias-corrected jackknife estimate. Each deletion recomputes the pooled AP and exactly the same contrasts, with all occurrences, labels, paired predictions of all conditions, all P and all replicates of the group. P and replicates do not become artificial independent units. The one-sided lower bound is $\hat{\theta} - t_{0.975,G-1}\mathrm{SE} _ J$. The $t(G-1)$ reference is a prespecified approximation that requires empirical calibration. Related $t$-based approaches for few groups have been studied by Ibragimov and Müller (2010); the jackknife variance goes back to Efron and Stein (1981). The conditional interpretation does not include the uncertainty of retraining.

**Issuance rule.** A confirmatory $p$ is issued only if the original estimate and all $G$ deletion estimates are defined, i.e. every family of $\mathcal{F} _ 0$ has positives in every deletion sample. In addition, $\mathrm{SE} _ J$ must be finite and positive for all contrasts of the test family. Otherwise no confirmatory $p$ is issued and the contrasts are reported as estimates. The issuance probability and the denominators of all rates are recorded.

**Sensitivity: bootstrap-t.** The paired group bootstrap-t, with 9999 resamples of groups with replacement and an inner jackknife in each resample, is evaluated separately as a sensitivity: $T_b=(\hat{\theta} _ b-\hat{\theta})/\mathrm{SE} _ {J,b}$ and $p=(1+\lvert\lbrace T_b \ge T \rbrace\rvert)/(B+1)$. Under the strict rule, which issues no $p$ if any resample is undefined, issuance requires near-universal family coverage. For instance, for at most 5% suspension with six families, every family must be present in 8/8, 10/12, 12/20 or 14/30 groups. In a small synthetic study with $G=12$, $B=199$ and 150 datasets per scenario, the strict rule suspended 10–13% of datasets. Coverage was 0.89–0.94. Under the null the FWER was 0.040, with a 95% Monte Carlo interval of 0.015–0.085. Power for $H_1$ was 0.58, against 0.79 for the jackknife-t in the same scenario. The warp-speed method made the bootstrap-t look conservative. The bootstrap-t is therefore no longer the primary procedure.

### Calibration before H

In WP0 an operating-characteristics study is prespecified and run with realistic sizes, dependence and rarity from the pilot. The grid covers $G$, effect size, prevalence, ties, intra-group correlation and family coverage per group. The rules of the study are:

- **Exact nulls.** For $H_1$, V and P have equal laws. For $H_2$, the F and D slots are swapped per group with probability 1/2, with one coin per group for V and all P. Non-null reference values are computed with large $G$ and a recorded Monte Carlo error. A value that is merely set to zero is not treated as a boundary null.
- **Full procedure.** Critical calibrations run the whole procedure on every synthetic dataset. The warp-speed method (Giacomini, Politis and White, 2013) is used only to explore the grid.
- **Independent random streams.** Reference values and every synthetic dataset have separate streams from a common seed. Strengthening the reference does not change the datasets, and every dataset can be regenerated from the seed and its index. The individual reference values are stored too.
- **Composition of H.** The study runs the same prespecified algorithm that allocates groups to H and development, with the same coverage rule and the same policy for $\mathcal{F} _ 0$. It records allocation failures, issuance probability, actual prevalences and the coverage of development.
- **Denominators.** Planned, allocated, defined and issued datasets are reported separately. FWER and power are given over all planned datasets, with non-issued ones counted as non-rejections, and over issued datasets.
- **Criteria.** At least 5000 replications per critical scenario. The upper 95% Monte Carlo bound of the FWER must be $\le0.035$ and the lower bound of the coverage of the 95% interval $\ge0.93$. Power $\ge0.80$ at the declared substantive effect is required. A minimum issuance probability is set in WP0 before H.

Confirmatory use requires that no quantity be undefined, that standard errors be finite and positive and that the operating characteristics in the pilot be acceptable before H is opened. If the calibration gate fails, estimates and uncertainty are reported with exploratory status. No alternative method is chosen on the basis of H results. These criteria test the robustness of the procedure; they do not prove properties of the unknown real population. Statistical readiness also requires enough real groups and positives.

**Synthetic design checks.** In the synthetic model of the support folder, with independent streams for the reference and the datasets, the jackknife-t, with a $t(G-1)$ reference and exact nulls, gave an FWER of 0–0.026 for $G=6$–30, with 1000–3000 datasets per scenario. Coverage of the 95% interval was 0.953–0.994. Power for $\Delta_{\mathrm{know}}\approx0.085$ was 0.48 for $G=8$ and 0.79 for $G=12$ with one base, and 0.89 for $G=12$ with five bases. For the smaller $\Delta_{\mathrm{know}}\approx0.05$ and $\Delta_{\mathrm{logic}}\approx0.027$, power was 0.17–0.20 for $G=8$, 0.32–0.43 for $G=12$ and 0.65–0.74 for $G=20$. In the scenario with one true null and $G=20$ the FWER reached the nominal level (0.026, upper Monte Carlo bound 0.033), close to the 0.035 criterion. An earlier batch with five bases, in which the reference and the datasets shared a random stream, had given an FWER of 0.028 with an upper bound of 0.047 and coverage of 0.926. With independent streams, the same 1000 datasets gave coverage of 0.960 with 20 and 0.957 with 5 reference replications. The number of reference replications therefore explains a small part of the difference; the earlier batch is a different Monte Carlo sample. With sparse family presence and ties, for $G=8$, only 498 of 1000 datasets were issued without a coverage rule. With the allocation algorithm of §K.7 and $m_H=2$, 992 were issued, with an FWER of 0.009; in 37% of datasets, however, some family was left in fewer than two development groups. With $m_H=3$ and $G=12$ or 20 the FWER was 0.014–0.023 and development kept its coverage in every dataset. Calibration with the real characteristics of the pilot is therefore necessary. Exact values and denominators are given in the [results summary](../../../docs/research/a2/support/README.en.md).

### Why shorter alternatives do not solve the problem

- **Sign test.** It tests the probability of a positive difference for an independent group, or the median, with special handling of zeros. It does not in general test a difference in pooled AP or a mean effect.
- **Paired sign-flipping of the mean $\log p$.** It needs symmetric differences or a suitable invariance and concerns a different estimand. Check T19 gives AP 0.8333 against 1.0, while the mean log-score moves the other way.
- **Swapping whole score vectors per group.** It would be exact only under strong joint exchangeability of label and prediction vectors. Equal AP does not imply this assumption.
- **Group randomisation.** It needs a real randomised assignment of the intervention to groups. Training all models on the same corpus is not such an experiment.
- **BCa or percentile bootstrap.** The name does not guarantee small-sample coverage. These are not chosen after the fact because they gave a smaller $p$.
- **Rank tests with exchangeable nulls.** With ten exchangeable null banks the minimum $p$ would be 1/11. With 39 it would be 1/40=0.025. The first Holm step of two tests needs at least 79 banks, for 1/80=0.0125. The generator does not establish exchangeability, so even these numbers do not justify a rank test.
- **Exact one-sided sign-flipping.** The minimum $p$ is $2^{-G}$: 0.015625 for $G=6$ and 0.0078125 for $G=7$. The calculation shows only the resolution under the required assumptions. Seven groups do not guarantee power, generalisation or validity for AP.

## K.9 · Link to M1 and M2

M1 selects the operational representation $R^\star$ with rule J in architecture A ([revised M1](../research/m1-selection-decision.md)):

$$
\widehat J(R)=\frac{1}{5}\sum_{r=1}^5F1^{(r)} _ {\mathrm{seg+fam}}(R,A),\qquad \widehat{\mathcal{A}} _ {\mathrm{dec}}=\lbrace R\in U\times\Phi:\widehat G_A(R)\ge g_{\min}\rbrace,\qquad R^\star=\arg\max_{R\in\widehat{\mathcal{A}} _ {\mathrm{dec}}}\widehat J(R),
$$

with $g_{\min}=\max\lbrace g_{\mathrm{use}},\widehat G_0^{\mathrm{pilot}}+\delta_{\mathrm{use}}\rbrace$. $\widehat G_A$ is the mean recall per known family on complete known segments, with forced choice of a label. A is a neural encoder with a semi-CRF of order zero in family transitions. The encoder is chosen before the grid, on internal, independent development splits: TCN-S as the initial choice and a BiGRU with matched context width as the comparison model. The choice preregisters a common context width, capacity, computational budget, criterion and grouped splits. B and C are evaluated across the whole grid with descriptive and estimative status. They do not take part in selecting $R^\star$.

$R^\star$ is finalised on all development material before A2. The uncertainty set $\mathcal{R}^\star$ and at most one sensitivity representation $R_{\mathrm{sens}}$ are reported separately. A2 runs on $R^\star$; $R_{\mathrm{sens}}$ is used only in a prespecified descriptive sensitivity. The `A_M1_selected` configuration is the architecture of the five bases $b_r$. `m1_checkpoint_id` records the M1 weights for reproduction.

The autoregressive event-level Transformer $T_{\mathrm{evt}}$ of M1 tests the usefulness of explicit segmental scoring with a common $F1_{\mathrm{seg+fam}}$. The boundary cues LBDM, IDyOM and parallelism are examined as standalone boundaries and as shared additional cues. Pitman–Yor segmentation is judged on $F1_{\mathrm{bnd}}$; for a common $F1_{\mathrm{seg+fam}}$ the same supervised family mapper, trained only on training data, is added and the hybrid character is declared. These elements belong to M1 and do not change the A2 base.

**Naming.** M2 uses the symbolic reference models $\mathrm{B0_{sym}}$ and $\mathrm{B0_{profile}}$, the neural condition B1, the condition $\mathrm{B2_{fam}}$ of M2a, supervised by shared family, and the condition $\mathrm{B2_{main}}$ that is compared with EISE in M2b ([revised M2](../research/m2-eise-research-design.md)). $B_K$ and $B^\star$ are A2 comparators and are none of these.

## K.10 · Criteria, fallbacks and timeline

| Status | Testable criterion | Permitted outcome |
|---|---|---|
| Technical readiness ($G_{\mathrm{know}}$) | reliable extractors, independent judgements, at least 4 operational specifications, 10 accepted P with $d_F,d_D\gt 0$, activation and convergence | the whole set of conditions is run; four families are not enough for statistical readiness |
| Confirmatory status | in addition, an adequate independent H with the coverage of §K.7, positives and variance, a prespecified substantive difference and successful calibration as in §K.8 | primary Holm claims and the conditional secondary family |
| Estimative status | A2 technically operational, but too few groups, undefined quantities, failed calibration, limited coverage or nested validation only | estimates, per-family results, uncertainty sensitivities; future independent confirmation |
| Stop confirmatory A2 | inactive or degenerate P, no certificate, label leakage, non-independent reference labels or non-extractable concepts | fix before main training; if unresolved, descriptive A2 and M1, M2 and M3a continue as planned |

Non-rejection does not mean equivalence. A negative or uncertain result is an interpretable finding, with an interval and power limitations. Hard cases are defined with musicological criteria before any scores and reported as a secondary subset. No unstable ratio with B1 minus chance in the denominator is used, and no collective non-inferiority claim without simultaneous testing.

**48-month timeline.** WP0 and pilot, with the calibration of §K.8: months 1–6. Extended encoding, specifications and extractors: 7–12, with H defined in month 12. M3a: 12–20. M1 and shared base: 13–22, with $R^\star$ selected in month 22. A2 and $B^\star$: 22–30. M2: 24–38. M5-min: 30–42. Synthesis: 39–48. $B^\star$ can develop the pair infrastructure early without waiting for a $\mathrm{B2_{fam}}$ result. EISE runs only with enough historical pairs and performances. ECSI, Mthesis, ATL, performance analysis and transfer to Znamenny chant remain prospects with separate criteria.

### Pseudocode of the final run

```text
audit sources, rights, groups, expert labels, extractors           # WP0
run operating-characteristics calibration of §K.8 with pilot data  # gate before H
allocate H for family coverage (m_H per family); freeze it         # month 12
for outer training split (development estimation only):
    inner-select R* with rule J in A; freeze encoder choice
    split development groups into D_base and D_int
    compile full sigma_V tables for ALL candidate families
    generate 10 P with the constrained sampler; record all rejections, LP residuals and termination
    for r in 1..5:
        fit base b_r without sigma on D_base; fit temperature T_r on D_int
        fit heads (w, lambda) for FV, DV, FP_l, DP_l on D_int with the same b_r/T_r
        fit B_K on D_int; fit B* with seed r within its declared budget
        predict complete candidate-by-family matrices; save before labels are joined
    report outer out-of-fold metrics as estimation, not as independent tests
freeze final development procedure, specifications, panel and all choices; lock hashes
fit final models on development groups only
open H once, if the confirmatory status holds
compute AP_fam per replicate, the paired contrasts and jackknife-t(G-1)
apply the primary Holm; open the secondary Holm only if both primary nulls are rejected
report bootstrap-t sensitivity, failed gates, missingness, uncertainty and the run ledger
```

## K.11 · Reproducibility and sources

Source hashes, splits, the specification compiler version, the rejection ledger, LP witnesses and residuals, configurations, parameter counts, optimisation residuals, run times, seeds, predictions before labels are joined and the exact metric version are saved. The mathematical checks T13–T27 of the previous revision (29/29 passed with Python 3.12.14, NumPy 2.3.5 and SciPy 1.17.0) belong to an earlier package that is not yet in the repository. Until it is added, references to T13–T27 point to that package and cannot be reproduced here on their own. T25 and T27 are procedure and interface checks; they do not prove corpus code that has not yet been written. The repository runs `test_ap.py` (AP with weights and ties) and `test_generator.py` (acceptance rules of the generator). The synthetic design checks of this revision, with seeds, configurations and software versions on every result line, are in [`docs/research/a2/support/`](../../../docs/research/a2/support/README.en.md).

**Bibliography**

- Bengio, Y., & Grandvalet, Y. (2004). No unbiased estimator of the variance of K-fold cross-validation. *Journal of Machine Learning Research*, 5, 1089–1105. [JMLR](https://www.jmlr.org/papers/v5/grandvalet04a.html)
- Chang, M.-W., Ratinov, L., & Roth, D. (2012). Structured learning with constrained conditional models. *Machine Learning*, 88(3), 399–431. [DOI](https://doi.org/10.1007/s10994-012-5296-5)
- Efron, B., & Stein, C. (1981). The jackknife estimate of variance. *The Annals of Statistics*, 9(3), 586–596. [DOI](https://doi.org/10.1214/aos/1176345462)
- Giacomini, R., Politis, D. N., & White, H. (2013). A warp-speed method for conducting Monte Carlo experiments involving bootstrap estimators. *Econometric Theory*, 29(3), 567–589. [DOI](https://doi.org/10.1017/S0266466612000655)
- Hemerik, J., & Goeman, J. (2018). Exact testing with random permutations. *TEST*, 27, 811–825. [DOI](https://doi.org/10.1007/s11749-017-0571-1)
- Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics*, 6(2), 65–70. [JSTOR](https://www.jstor.org/stable/4615733)
- Ibragimov, R., & Müller, U. K. (2010). t-Statistic based correlation and heterogeneity robust inference. *Journal of Business & Economic Statistics*, 28(4), 453–468. [DOI](https://doi.org/10.1198/jbes.2009.08046)
- Raman, M., Chan, A., Agarwal, S., Wang, P., Wang, H., Kim, S., Rossi, R., Zhao, H., Lipka, N., & Ren, X. (2021). Learning to deceive knowledge graph augmented models via targeted perturbation. *ICLR 2021*. [arXiv](https://arxiv.org/abs/2010.12872)
- van Krieken, E., Minervini, P., Ponti, E. M., & Vergari, A. (2024). On the independence assumption in neurosymbolic learning. *Proceedings of ICML*, PMLR 235, 49078–49097. [PMLR](https://proceedings.mlr.press/v235/van-krieken24a.html)
- Xu, J., Zhang, Z., Friedman, T., Liang, Y., & Van den Broeck, G. (2018). A semantic loss function for deep learning with symbolic knowledge. *Proceedings of ICML*, PMLR 80, 5502–5511. [PMLR](https://proceedings.mlr.press/v80/xu18h.html)

The numerical settings of this appendix are specifications of this experiment, not conclusions of these sources.

---

[A2 research design](../research/a2-knowledge-design.md) · [Revised M1](../research/m1-selection-decision.md) · [Revised M2](../research/m2-eise-research-design.md) · [Home](../../README.md)
