# M1-X — Family structure as an inductive bias for formula boundaries

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/research/m1-x-design.md) · **English**
<!-- language-switch:end -->

[Core research programme](../../README.md) · [M1 and selection rule J](m1-selection-decision.md) · [Chapter 5 (Greek)](../../../docs/full/05-m1.md#r038x) · [Appendix G (Greek)](../../../docs/appendices/g.md#r186x)

## 1. Research question and place within the programme

**M1-X** is a self-contained methodological extension of M1. It investigates whether explicitly incorporating family compatibility into model parameterisation improves the recognition of complete melodic formulae. The main question of M1 concerns symbolic representation selection across the twelve conditions of the $`U\times\Phi`$ grid. The operational representation $`R^\star`$ is selected with architecture A and rule J, and remains the input to A2 and M2.

The principal shared input for M1-X is the previously selected $`R_A^\star`$. The representation selected by C on development data is assessed separately. M1-X results are reported independently of input selection and of the confirmatory estimands in A2/M2.

**Research question.** What contribution does musicology-informed parameterisation of boundary scores make relative to a strong factorised model, given the same family supervision and matched computational resources? How much of the resulting performance difference is associated with parameterisation and training, and how much with the breadth of search?

## 2. Common output space and probability models

The input sequence consists of atomic events $`X=(e_1,\ldots,e_T)`$. A candidate segment $`s=[a,b]`$ has inclusive endpoints and length $`1\le b-a+1\le L_{\max}`$. The family label set is $`\mathcal F^+=\mathcal F_{\rm known}\cup\lbrace \varnothing_F\rbrace`$, where $`\varnothing_F`$ denotes a valid decision not to assign a known family. Legal outputs are non-overlapping collections of segment–family pairs $`(s,f)`$, including the empty output. Uncovered events are assigned a unique structural skip with potential $`\chi_t`$.

Architecture A is the shared zero-order semi-Markov CRF defined in [G.2 (Greek)](../../../docs/appendices/g.md#r181):

```math
p_A(y\mid X)\propto\exp S_A(y),\quad
S_A(y)=\sum_{(s,f)\in y}\phi_A(s,f)+\sum_{t\notin\cup y}\chi_{A,t}.
```

The marginal score of a complete boundary configuration $`B`$ is:

```math
\beta_A(B)=\sum_{s\in B}\operatorname{LSE}_{f\in\mathcal F^+}\phi_A(s,f)
+\sum_{t\notin\cup B}\chi_{A,t}.
```

C_fac uses a shared trainable encoder, a free boundary-scoring head, and a locally normalised family head:

```math
p_C(B,\mathbf f\mid X)=p_B(B\mid X)
\prod_{s\in B}p_F(f_s\mid s,X).
```

The factor $`p_B`$ is a semi-Markov CRF over boundaries. The factor $`p_F`$ is a normalised softmax over the same $`\mathcal F^+`$. C uses a shared encoder that also learns from family labels. Its initial marginal boundary decision is $`\arg\max_B\log p_B(B\mid X)`$. Full joint decoding uses the score $`\log p_B+\sum_s\log p_F`$, with unit weight on the family term. Rescoring with raw, unnormalised logits is excluded.

### 2.1 Equivalence of model classes and the controlled contrast

Given sufficient parameterisation capacity, these two forms represent the same class of zero-order distributions. For $`\phi_A(s,f)=b_A(s)+c_A(s,f)`$, define:

```math
m_A(s)=\operatorname{LSE}_f c_A(s,f),\quad
b_C(s)=b_A(s)+m_A(s),\quad
\log p_F(f\mid s)=c_A(s,f)-m_A(s).
```

The resulting C can exactly represent A's joint distribution. Conversely, adding a boundary potential and $`\log p_F`$ yields a model of the form A. These identities hold for the probabilistic model classes when the legal output space and skip potentials are shared.

The empirical comparison concerns **parameterisation and inductive bias**. In A, compatibility between a segment and family patterns contributes by construction to the marginal boundary score. In C_fac, the corresponding boundary score is learned by a free head with a family-informed shared encoder. Equivalent expressive capacity provides a controlled setting for evaluating generalisation and data efficiency.

## 3. Joint training with partial annotation

Both conditions use the **same sets of complete, legally admissible analyses** $`\mathcal C_j`$ defined in G.2. The loss for C is:

```math
\mathcal L_{C,j}=-\log\sum_{(B,\mathbf f)\in\mathcal C_j}
p_B(B\mid X)\prod_{s\in B}p_F(f_s\mid s,X).
```

The union of admissible branches counts each structured output once. Dependencies between boundaries and family labels are preserved within every complete analysis. Projecting the admissible boundary sets and label sets separately can introduce combinations unsupported by the annotation. The D1 weighting specification, defined over unique annotation obligations and independent groups, is applied consistently after finalisation and before confirmatory training.

Initialisations, model capacity, available context, length constraints, temperature/family-distance metric, reference annotation, output format, and tuning budget are matched between A and C_fac.

## 4. Training-by-search comparison matrix

| Trained model | 1 — marginal boundary decision | K — candidate segmentations | global — full joint MAP |
|---|---|---|---|
| A | $`\arg\max_B\beta_A(B)`$, then assign families | Top-K by $`\beta_A`$, followed by joint rescoring | $`\arg\max_{y}S_A(y)`$ |
| C_fac | $`\arg\max_B\log p_B(B)`$, then assign families | Top-K by $`\log p_B`$, followed by joint rescoring | $`\arg\max_{B,\mathbf f}\log p_C(B,\mathbf f)`$ |

The three decoding conditions in each row use **identical trained weights**. Thus, the minimal matrix requires two training runs per representation and initialisation. The global comparisons evaluate differently learned parameterisations with the same final decoding rule.

The total tie-breaking order is: higher score, then fewer segments, then lexicographic order of $`(a,b,f)`$. The empty output participates in every procedure. For a fixed legal output space, rescoring all possible segmentations attains the same optimal score as joint MAP decoding. A finite K-best list attains this score only if it contains a segmentation supporting a global maximiser.

For A, $`\max_{\mathbf f}S_A(B,\mathbf f)\le\beta_A(B)`$; for C, $`\max_{\mathbf f}\log p_C(B,\mathbf f)\le\log p_B(B)`$. When candidates are sorted in descending marginal score $`\beta`$, the upper bound for the first unexamined candidate is compared with the best joint score $`v_K`$ already found. If $`\beta(B_{K+1})<v_K`$, global optimality is certified; equality is resolved using the common tie-breaking rule. Performance, coverage, and computational cost are reported as functions of K.

## 5. Estimands and hypotheses

The common criterion $`J`$ is exact micro-$`F_{1,\mathrm{seg+fam}}`$ for complete admissible occurrences with both correct boundaries and family identity. The primary contrast uses $`R_A^\star`$:

```math
\Delta_X=J(A_{\mathrm{global}},R_A^\star)
-J(C_{\mathrm{seq}}^\star,R_A^\star),
```

Here, the strongest C decoder is selected on development data from the 1 condition, prespecified K values, and global decoding. The following contrasts are also reported:

```math
\Delta_{\mathrm{param}}=J(A_{\mathrm{global}})-J(C_{\mathrm{global}}),
\qquad
\Delta_{\mathrm{search}}^C=J(C_{\mathrm{global}})-J(C_1).
```

The sum of these two quantities equals $`J(A_{\mathrm{global}})-J(C_1)`$. The remaining columns diagnose interactions between search and parameterisation. In the secondary $`\Delta_{\mathrm{own}}`$ analysis, each method chooses its own representation using development data alone, with the same eligibility rule and threshold $`g_{\min}`$. The full profile across all twelve representations is reported descriptively.

**H_X1 (primary):** a positive $`\Delta_X`$ on independent held-out complete works. **H_X2 (secondary):** the A-global versus C-global difference, with global search in both models. **H_X3 (mechanism):** the effect of family compatibility specific to the segment's musical content. **H_X4 (exploratory):** greater sensitivity at within-syllable boundaries and at boundaries with multiple admissible annotations. **H_X5 (secondary):** an interaction between parameterisation and the amount of available training data, assessed through learning curves using 25%, 50%, and 100% of training groups, with separate evaluation of unseen families and boundary quality.

H_X5 tests prespecified interactions and analyses separately the sources of variation associated with training set size, family coverage, and work scale. The directional prediction is that $`\Delta_X`$ decreases as the training set grows. For families absent from training, the boundary benefit may diminish or reverse.

## 6. Diagnostic interventions and strong comparators

The N2 diagnostic holds model weights fixed and permutes the family-compatibility score $`q(s)=\max_f c(s,f)`$ among candidate segments of equal length within the same work. It measures the informational value of the association between score and specific musical content for the trained parameters of A. Twenty permutation repetitions are planned, together with an additional check of mean compatibility by segment length.

The C_B control trains a boundary model without a family loss, while A_shuf uses controlled permutations of family labels during training. N2, with A's weights fixed, measures the role of the family score in the decision. C_B and A_shuf measure the contribution of family supervision during learning.

Additional strong comparators include event-level BILOU × family + O tagging with legal transitions and matched context, as well as local alignment and subsequence DTW. Boundary accuracy, family recall at known boundaries, prediction count, and computational cost are reported separately.

## 7. Evaluation over legally admissible analyses

For each complete legal analysis $`c`$, the match count $`M(c)`$ is computed using prediction–reference edges that agree on an entire boundary pair **and** the family. The corpus-level criterion is:

```math
J^\star=\max_{c\in\mathcal C^{\mathrm{corpus}}_{\mathrm{legal}}}
\frac{2M(c)}{P+X(c)}.
```

The number of occurrences $`X(c)`$ may vary across admissible analyses. The best analysis is selected by maximising corpus-level micro-F1, with $`P+X(c)>0`$. When groups are independent, fractional optimisation is obtained through:

```math
H(q)=\sum_g\max_{c_g\in\mathcal C_g}\lbrace 2M_g(c_g)-qX_g(c_g)\rbrace -qP,
\qquad H(q^\star)=0.
```

For a fixed legal-analysis set and identical predictions, $`F_{1,\mathrm{span}}\ge F_{1,\mathrm{seg+fam}}`$ holds for each analysis and therefore also after separate maximisation over analyses. Family errors are additionally interpreted on the **same** legal analysis. A range of between-model differences obtained using the same admissible analysis is reported separately from the difference between individually optimised admissible scores.

## 8. Statistical decision and pilot adequacy

The independence unit is a group of related works and source witnesses. The confirmatory procedure is selected **before** external evaluation using prespecified simulations reflecting unequal group sizes, ties among admissible analyses, rare families, and variable $`X(c)`$. Candidate procedures are a studentized sign-flip test, provided its validity assumptions are satisfied, cluster bootstrap-t, and jackknife-t. Simulations estimate type-I error and power at a nominal one-sided level of $`\alpha=0{,}025`$, with a proposed maximum empirical error estimate of 0.03 and explicitly reported Monte Carlo uncertainty. TOST procedures and equivalence intervals require separate coverage calibration. If none of the candidate procedures meets the prespecified criterion, the result is reported descriptively. For the corresponding complete enumeration, a sign-flip test requires at least six independent test groups as a resolution limit.

Each resampling replicate recomputes the complete admissible corpus analysis and its associated $`J^\star`$. Training replicates reduce sensitivity to random initialisation; the statistical unit of independence remains the work–source group. A pilot with few groups primarily estimates variability, annotation adequacy, and the sample size needed for the main study.

Trained A/C models may be reused only if they were fitted with the same finalised protocol, including D1. Practical feasibility and actual computational cost are documented in WP0/WP1 before confirmatory evaluation.

## 9. Relationship to the musical unit and earlier research

Comparing statistically induced segments with complete, musicologically recognised formulae is a diagnostic of **the main M1 study**, conducted through the [ByzCorpus pilot (Greek)](../../../../docs/research/byzcorpus/segmentation-pilot.md) outside selection rule J. The study includes NHPYLM, HMM/MDL, and explicit reference to the melodic chunks of Mavromatis (2005), with shared boundary conventions and independent musicological analyses. NHPYLM segments are algorithmically induced units in attested compositions; the chunks discussed by Mavromatis concern the analytical organisation of generated melodic realisations.

Architectural precedents include Sarawagi and Cohen (2004); Kong, Dyer and Smith (2016); Masada and Bunescu (2017, 2018); and Yan, Cwitkowitz and Duan (2021). Lanz and Hajič (2023, 2025) provide comparative questions for induced segmentation in liturgical melodies. M1-X contributes a quantitative assessment of a musicologically specified unit through matched comparisons of parameterisation, training, and search.

## 10. Protocol status and pending decisions

The model definitions, mathematical identities, and computational conditions specify the **proposed methodology**. Differences in empirical performance, generalisation to unseen families, and statistical power will be estimated using real data. Before the confirmatory phase, the following are finalised: D1 weighting, an operationally justified practically meaningful effect threshold, independent test groups, challenging passages, and statistical reliability criteria.

M1-X retains A as its reference parameterisation, selection rule J, and the operational input to A2/M2.
