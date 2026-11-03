# Appendix K — A2 methodology and feasibility

**Language / Γλώσσα:** [Ελληνικά](../../../docs/appendices/k.md) · English

[A2 explanation](../research/a2-knowledge-design.md) · [Executable tools](../../../docs/research/a2/support/README.md)

**Status:** candidate operational specification for implementation and pilot calibration. PE0/PE1 determine scale and confirmatory status before the final H. Examples and current simulations are synthetic.

## K.1 Units and data contract

The independent unit is a connected component of the work–source dependency graph. Copies, dependent editions and related historical passages stay in the same group. Occurrences, fitting repetitions and perturbations have separate roles.

Required tables cover works/groups, atomic symbolic events, occurrences with stable IDs, label status and accepted complete boundary pairs B_x, the concept bank, specification cards and splits. Unresolved occurrences are tracked separately. Documented unknown families count as negatives for each known family.

Membership judgements precede application of the tested specification. Rule-informed judgements receive a separate provenance flag and are excluded from the independent primary evaluation. Extractors receive no evaluation family label. Learned extractors produce out-of-fold development values. Candidate segments and maximum length are identical across conditions.

## K.2 Common input and summaries

The concept bank contains c_j∈{0,1,?} and observability masks. Each specification produces T_f^K=(concept ID,value,mask,role,group). Bank values are independent of K∈{V,P}; specification assignments change T/Q/φ.

For observed R/A literals q_j=2c_j−1; for E literals q_j=1−2c_j. Unknown contributes zero while remaining in the denominator:

$$
Q_R=|R|^{-1}\sum_{j\in R}q_j,\quad
Q_A=|\mathcal G|^{-1}\sum_{G\in\mathcal G}|G|^{-1}\sum_{j\in G}q_j,\quad
Q_E=|E|^{-1}\sum_{j\in E}q_j.
$$

An empty role contributes zero. An empty alternative group invalidates the specification. Each Q component lies in [−1,1]. Supportive observations remain metadata until their computational role is established.

## K.3 Logic and scores

$$
\phi_f^K=\bigwedge_{j\in R}c_j\wedge
\bigwedge_{G\in\mathcal G}\bigvee_{j\in G}c_j\wedge
\bigwedge_{j\in E}\neg c_j,\qquad v_f^K=1[\phi_f^K=0].
$$

Kleene logic gives 0∧?=0, 1∧?=?, 1∨?=1, 0∨?=?, ¬?=?. True and unknown are distinguished in support checks even though both give v=0.

$$
\ell_{F,K}=b_r+w^\top Q_f^K,\qquad
\ell_{D,K}=b_r+w^\top Q_f^K-\lambda v_f^K,
$$
$$
w\in W=\{w:\sum_jw_j=1,\ w_j\ge0.1\},\qquad \lambda\in[0,2].
$$

Weights are shared across families. Beta is fixed at one; predeclared sensitivities use beta 0.5/2, removal of the knowledge term, and half-lambda for unknown logic. The unknown-family class uses its common base score without Q/φ. Report abstention, coverage and unknown-family errors.

For b=0.4, w=(0.4,0.3,0.3), Q=(1,0,1), F scores 1.1. With false φ and λ=0.8, D scores 0.3; unknown φ retains 1.1. F and D have separately fitted weights in the experiment.

## K.4 Probabilistic model and fitting

At known boundaries p(f|s)=softmax_f ℓ(s,f), including the unknown family. For legal segmentation Y, E(Y) sums segment scores and common fixed skip scores. Main A has zero-order family transitions. Each uncovered event has a unique skip step.

$$
Z(X)=\sum_{Y\in\mathcal Y_{legal}(X)}e^{E(Y)},\qquad
L_{partial}=\log Z(X)-\log\sum_{Y\in\mathcal Y_{obs}(X)}e^{E(Y)}.
$$

Each compatible complete path is counted once. The penalty enters both constrained numerator and partition during fitting, and decoding. Verify forward computation and gradients against exhaustive small examples. Partial likelihood can be nonconvex.

B_K fits unrestricted family-specific linear weights to the full concept bank/masks using the common frozen base. B⋆ adds neural adaptation, SupCon with cross-work positives and negatives in the denominator, train-derived prototypes and the same available concept supervision. Report its capacity and extra cost separately.

## K.5 Splits and five bases

Define independent groups and sealed H before M1. Preliminary TCN-S/BiGRU selection stays within development. M1 selects R⋆ using J on A and its separate family gate G_A; B/C remain comparators.

For r=1,…,5:

1. Fit A(R⋆) on D_base without family specifications.
2. Fit a common temperature on disjoint D_head, then freeze base and temperature.
3. Fit all FV/DV/FP/DP heads and B_K on D_head with common labels and matched tuning procedures.
4. Give B⋆ the declared eligible development information under its additional budget.
5. Save H predictions before joining H labels.

Choose the D_base/D_head allocation and hyperparameters through grouped development evaluation. D_head is training data for the overall system. Grouped cross-fitting is a separately costed sensitivity with a consistent calibration transfer.

The 2×5+2×10×5+2×5=120 budget covers main fits. Base fitting, tuning, pilot and further diagnostics add to it.

## K.6 Generator and certificates

Use a single typed bijection of concept identities for all families. Preserve role structure, alternative-group sizes and cross-family intersections. The constrained sampler allows mappings within compatible type/scale blocks and frequency/missingness differences ≤0.10 on training data, without evaluation labels.

Every family changes at least one R/A/E literal. Log exclusion-only changes, v agreement, canonical-card uniqueness and equality of observed Q/v across candidates. Require witnessed φ=1 support and φ=0 activation. Any completion-based satisfiability criterion requires a separate SAT check respecting actual concept dependencies.

On feasible witness states Ω compute:

$$
d_F=\min_{w,w'\in W}\|Q_Vw-Q_Pw'\|_\infty,
$$
$$
d_D=\min_{w,w'\in W,\lambda,\lambda'\in[0,2]}
\|Q_Vw-\lambda v_V-Q_Pw'+\lambda'v_P\|_\infty.
$$

Require numerical lower bounds >10⁻⁶, recorded feasibility residuals and dual gaps within tolerance. The certificate concerns the knowledge score on the declared Ω; effects on normalised probabilities and rankings are evaluated separately. The λ,λ′≥0.1 certificate concerns an active subclass and is reported with that scope.

Actual acceptance also requires independent expert non-synonymy and musical applicability review before model outcomes. Use real development states for operational checks; a theoretical Boolean cube is a separate diagnostic. Failure to obtain ten accepted P within the predeclared cap of up to 100,000 proposals makes A2 exploratory. A time limit is recorded as interrupted search.

## K.7 Metric and estimands

Fix F₀ from development. Each occurrence x counts once; its family score is the average p(f|s) over independently accepted complete boundary pairs s∈B_x. Rank occurrences separately for each f. Insert tied-score blocks together:

$$
AP_f=\sum_k(R_k-R_{k-1})P_k,\qquad
AP_{fam}=|F_0|^{-1}\sum_{f\in F_0}AP_f.
$$

Any family without positives makes the complete fixed-family metric undefined. Unknown-family examples are negatives for known families. Equal-group weighting is a sensitivity.

S averages five AP values, then averages ten perturbations for P. Main contrasts are Δ_know and Δ_logic,V from the explanatory page. Mean structural effect and interaction are secondary. F1_seg+fam uses accepted complete B_x pairs and legal one-to-one matching; F1_bnd concerns boundaries.

## K.8 Uncertainty and statistical feasibility

Inference is conditional on the ten specific P and five fitted bases. Report between-P dispersion without treating perturbations as independent musical observations.

$$
SE_J^2=\frac{G-1}{G}\sum_g(\widehat\theta_{-g}-\overline\theta_{-})^2,\qquad
T=\widehat\theta/SE_J.
$$

Candidate primary p-values use a Student t(G−1) reference. The original pooled estimate is retained. This approximation requires pilot calibration. Test the two one-sided θ≤0 hypotheses with Holm at 0.025: first 0.0125, then 0.025. Rejection of both opens a second Holm family testing DV superiority to B_K and B⋆. Component p-values require valid calibration.

Evaluate H once after choices. Gates include fixed F₀, positives after each group deletion, finite positive SE, adequate discrimination and acceptable operating characteristics. Two positive groups per family ensure only a necessary definability condition. Pilot accuracy/power targets determine the final group count.

The calibration grid includes exact boundary nulls, both partial nulls, sparse families, unequal group sizes, ties and reference-target uncertainty. Report Monte Carlo intervals. Candidate design gates are MC95% upper FWER≤0.035, MC95% lower coverage of nominal 95% intervals≥0.93, and power≥0.80 at the predeclared meaningful effect. These design tolerances are finalised before H.

Report valid-result probability, FWER and power both among all repetitions and among valid samples, and coverage of issued intervals. Calibration precedes confirmatory activation; failed gates yield estimation and sensitivities.

Full bootstrap-t with inner jackknife is a sensitivity. Undefined roots suspend that analysis and are counted. Warp-speed is a screening tool requiring agreement checks against the final procedure.

## K.9 Diagnostics and deliverables

Record lambda by condition, perturbation and repetition; rates below 0.1 and at 2; true/false/unknown activation; and common base/temperature settings. Supplementary diagnostics include rule-only, inference-only D with development-selected lambda, violation-count penalty and a nonlinear head with matched additional parameter count.

PE0 inventories sources, families, independent groups, rights, extractor reliability and cost. PE1 delivers a stable representation/annotation/split contract. M1 selects R⋆; A2 runs in months 22–30; M5-min in months 30–42 applies evaluated recognition. M2a and conditional historical M2b retain their own metrics and gates.

Record source/card/extractor versions, checkpoint and seed per repetition, splits, canonical P, LP witnesses and residuals, hyperparameters, time/memory, predictions before label joining and all gate failures.

## K.10 Implementation order

1. Validate occurrence IDs, complete boundary pairs, group independence and judgement provenance.
2. Implement common concepts, Q/φ/v, Kleene checks, canonical cards and expert review.
3. Generate ten P and save mappings, witnesses and rejection reasons.
4. Implement known-boundary frozen-base heads, temperature, softmax loss and gradient checks.
5. Implement shared segment space, forward/partition and partial likelihood; verify exhaustively on small examples.
6. Run a complete feasibility pilot covering cost, concept reliability, family coverage, lambda and statistical calibration.
7. Freeze panels/settings, save H predictions, join independent labels, and run main and supplementary analyses.

```text
prepare grouped splits, independent labels, concept bank and fixed F0
validate V; generate and validate P[1..10] on development support
for r in 1..5:
    fit/load A(R*) checkpoint r trained only on D_base
    fit common temperature r on D_head; freeze base and temperature
    for K in [V, P1, ..., P10]:
        fit F_K and D_K on D_head
        save H probabilities, lambda, diagnostics and cost
    fit/evaluate B_K and Bstar under declared budgets
compute occurrence APs, repeated means and paired contrasts
apply pre-H calibration gate, then group jackknife and Holm
report valid-result probability, uncertainty and gate failures
```

The [Greek appendix](../../../docs/appendices/k.md#k10-σειρά-υλοποίησης-και-λειτουργική-καταγραφή) includes the machine-readable registry fields. Support tools exercise synthetic subsystems. The complete pilot connects them to the actual A.
