# A2–S3 · Protocol for paired delimitation comparisons

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../docs/research/byzcorpus/a2-s3-delimitation/protocol.md) · **English**
<!-- language-switch:end -->

[Overview](README.md) · [Evidence](evidence-and-next-steps.md) · [ByzCorpus](../README.md) · [Core A2](../../a2-knowledge-design.md)

**Specification:** S3 technical definition following the numerical checks of November 2026. **Scope:** secondary, descriptive comparison of the **right endpoint**, with a common start and a known family. Core A2 and Appendix K retain their primary measures and statistical procedures.

## 1. Unit and accepted reference sets

Occurrence \(i\) has a documented family \(f_i\), preferred accepted start \(a_i^\star\) and a full set \(B_i\) of acceptable start–end pairs. Spans are indexed on atomic melodic events: \([a,b]\) includes events \(a\) through \(b\), with boundaries at gaps \(a\) and \(b+1\).

The right-endpoint analysis uses only accepted extents that share the preferred start:

\`\`\`math
B_i^{a^\star}=\{s\in B_i:\operatorname{start}(s)=a_i^\star\}.
\`\`\`

\(B_i^{a^\star}\) must be nonempty. The **general** union across all accepted delimitations continues to use the full \(B_i\) as a separate probabilistic readout. The core A2 family AP retains its established fixed-boundary definition in [Appendix K](../../../appendices/k.md).

## 2. Common local window

A common window \(W_i=[u_i,e_i]\) is selected, forcing boundaries at gaps \(u_i\) and \(e_i+1\):

- **Left edge:** the last expert-agreed boundary gap at or before the earliest accepted start.
- **Right edge:** the first expert-agreed boundary gap **after the furthest endpoint** of all accepted extents in \(B_i\) and every eligible variant to be scored.
- **Coverage:** the window fully contains every member of \(B_i\) and every scored variant. The window is fixed before model scoring.

If no appropriate agreed edge exists within the reviewed material, the occurrence is ineligible for S3 with a recorded reason. Technical, unreviewed and abstention masks remain explicit.

## 3. Eligible variants

Variants \(v^-=[a_i^\star,b^-]\) and \(v^+=[a_i^\star,b^+]\) denote truncation and extension. Both preserve the same start and family \(f_i\). Candidate right endpoints are selected from a **prespecified notation-and-text articulation scale**: choose the strongest articulated gap in the relevant search region, breaking ties in favour of the nearest gap to the formula ending. Selection relies on annotations and observable articulation, separately from model predictions and statistical cuts.

**Truncation:** the right endpoint precedes the earliest accepted end with the same start; no accepted reading of the occurrence adopts it; every expert who reviewed the candidate gap marked continuation, with no technical mask or abstention.

**Extension:** only documented connective material lying outside **every** accepted extent is eligible. The extension excludes events of the next formula and any masked or abstained material; no accepted reading treats it as the complete extent of the current formula. Its end gap may lie **exactly at the start of the next formula**, at the end of the reviewed region, or at a unanimously reviewed continuation gap. Every candidate must fit the declared span search space and be covered by the common window.

Eligible and rejected candidates, together with a reasoned status for each proposed endpoint, are recorded.

## 4. Probability contrast and numerical algorithm

For each experimental cell \(c\), S3 computes:

\`\`\`math
D_i^{(c)}(v)=
\log P_c\!\big(\exists s\in B_i^{a^\star}:(s,f_i)\in Y\mid W_i,X\big)
-\log P_c\!\big((v,f_i)\in Y\mid W_i,X\big).
\`\`\`

Both terms use the same window and family. The log probability of the accepted union is obtained **directly in log space**, via a two-state forward recursion (whether or not an accepted member has been used). This includes skip potentials, jointly permissible segments and overlapping accepted alternatives; it avoids subtracting nearly equal probabilities.

The full \(B_i\) is retained for the general union probability and variant admissibility checks. The specific S3 numerator uses \(B_i^{a^\star}\). Report coverage against the maximum segment length, eligible occurrence counts and reasons for exclusion.

## 5. A2 conditions and reference model B_L

S3 uses the **existing** FV, FP, DV and DP model scores, with a common frozen neural base within each repetition. The core A2 perturbation generator and V/P × F/D experiment are unchanged; S3 contributes distinct secondary readouts.

\(B_L\) is the **S3-specific reference model**, adding terms for **exact length per candidate family**, articulation and text boundaries, with prespecified **L2** regularisation. Its original base remains fixed, and the extra terms are fitted using eligible development data alone. \(B_L\) does not use musicological R/A/E concepts. Exact length addresses one- and two-event endpoint movements that fall within the same coarse length bin.

Family \(f_i\) is **known only within this diagnostic comparison**. Recognition in complete unseen works must be evaluated separately without supplying the true family label to the decoder.

## 6. Paired aggregation and interpretation rule

A **common occurrence sample** contains cases where both eligible variants are available and all required scores for every compared cell, including enabled reference models, are finite.

Average \(D_i^{(c)}(v)\) first within each family in the **prespecified fixed** \(\mathcal F_0\), then equally across families, then over paired bases. Perturbed cards are averaged according to core A2 conventions. Report the S3-specific knowledge-validity and logical-integration contrasts and contrasts versus the knowledge-free base and \(B_L\), **separately for truncation and extension**.

A two-sided delimitation finding requires valid knowledge to outperform perturbed cards, the knowledge-free base and \(B_L\) **on the same occurrences and for both variants**. One-sided observations are reported separately. S3 remains a **descriptive secondary analysis**; its unadjusted 95% intervals are outside the multiplicity family of core A2 primary hypotheses.

## 7. Intervals and issuance requirements

Use delete-one-independent-group jackknife, preserving the fixed \(\mathcal F_0\) across every deletion, with \(t(G-1)\) as reference. Every family in \(\mathcal F_0\) must remain represented in every required deletion. Where no valid interval can be issued, report **the estimate and a specific reason**: family missing from common sample or a deletion, nonfinite values, fewer than two groups or zero/numerically negligible standard error.

The near-zero numerical check is:

\`\`\`math
\varepsilon_{\mathrm{num}}=
32\varepsilon_{\mathrm{mach}}\sqrt{G}
\max\left(1,|\hat\theta|,\max_g|\hat\theta_{(-g)}|\right).
\`\`\`

An interval is issued only when \(\mathrm{SE}_J>\varepsilon_{\mathrm{num}}\), subject to the other conditions. Report group counts, family coverage, estimates, tolerances and non-issuance reasons.

## 8. WP0, M3a and separate NHPYLM comparison

**WP0** develops the R/A/E musicological cards, tests candidate construction, specifies the articulation scale and inventories observed exact lengths per family. Development data are used to estimate and tune \(B_L\), with grouped splits. **M3a** evaluates the finalised cards and instructions on separate independent material.

The additional **NHPYLM** comparison uses frozen, out-of-fold statistical cuts. It compares eligible cut and non-cut points while controlling for articulation, textual boundary and distance from the accepted end. Different right endpoints of a single occurrence necessarily have different exact lengths, so \(B_L\) remains necessary; equal-exact-length matching can additionally be conducted **across occurrences**. NHPYLM cuts **do not determine eligibility** for the main S3 candidates.

[Evidence and next steps](evidence-and-next-steps.md).
