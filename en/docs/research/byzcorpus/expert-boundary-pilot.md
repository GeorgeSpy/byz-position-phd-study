# ByzCorpus — Expert boundary-agreement feasibility pilot

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά — full protocol](../../../../docs/research/byzcorpus/expert-boundary-pilot.md) · **English**
<!-- language-switch:end -->

[ByzCorpus](README.md) · [Data model (Greek)](../../../../docs/research/byzcorpus/data-model.md) · [NHPYLM pilot (Greek)](../../../../docs/research/byzcorpus/segmentation-pilot.md)

> **Status: independent exploratory protocol · revised 7 November 2026.** This research plan specifies a feasibility study for musicologically informed boundary annotation. Sample targets, repertoire eligibility and thresholds will be fixed after source verification and calibration. Current deliverables comprise methodological specifications and synthetic checks; no expert judgements have been collected yet.

## Rationale and objective

The initial empirical study asks whether **two independent specialists** identify the same *internal melodic boundaries* at a predefined analytical scale. **Phase B** (Byzantine papadic Koinonika) is self-contained. A possible **Phase G** (initially Gregorian responsories) would be designed separately, with its own sources, specialists and readiness criteria.

This pilot aims to evaluate the **feasibility, coverage and usefulness of an independent musicological reference**. Reproducible NHPYLM and other computational segmentation baselines follow once this reference has been demonstrated. Recurrence, formula identity, memory efficiency and mode prediction are separate research questions.

## Proposed sample and annotation design

- **Pipeline trial (Phase B):** one work outside the evaluation set, with an identified witness, a usable transcription and one checked window; two complete trial submissions; symbol → event → gap mapping; manual recount of the evaluator output.
- **Calibration:** four independent works with shared examples illustrating sub-chunk, target-scale and higher phrase boundaries; freeze the written guide, visible information and thresholds before evaluation.
- **Evaluation:** twelve further independent source/work groups, one predetermined window per group, the same two independently submitting specialists: 24 first-pass judgements in evaluation, 32 including calibration. Phase G, if undertaken, has its own 4+12 groups and its own two specialists.
- **Window:** 128 atomic melodic events (indices 0–127) with 16 context events on either side of a 96-event scored centre (events 16–111). Gap $j$ lies between events $j-1$ and $j$; the **95 candidate internal gaps** are $17,\ldots,111$. Gaps 16 and 112 (centre/context edges) are not scored; the whole window has 127 internal gaps, which is never the pilot denominator.
- **Recording:** per gap and annotator, `boundary`, explicit `continuation`, or `abstain(reason)`; per gap, `technical_unavailable`; a gap with no recorded state (`unreviewed`) invalidates the submission until corrected and is never read as continuation. `missing_submission` and `both_empty` (two valid all-continuation submissions) are distinct outcomes.
- **Sampling:** freeze candidate works, source dependencies, musical context and sampling seeds before reading labels. Linked variants, witnesses and co-exegeses form grouped components. All twelve selected groups remain in the final registry regardless of missingness.

## Primary estimand

For each group $g$, let $E_g$ be the intersection of technically available gaps reviewed by **both** annotators; $K_g=|E_g|$. Within $E_g$, let $n_g,m_g$ be their boundary counts and $h_g=|A_g\cap B_g|$ the count selected by both.

For $K_g\gt 0$ and $n_g+m_g\gt 0$:

$$
a_g=\frac{2h_g}{n_g+m_g},\qquad
c_g=\frac{2n_gm_g}{K_g(n_g+m_g)},\qquad
d_g=a_g-c_g.
$$

Here $a_g$ measures exact boundary F1 and $c_g$ is its expectation given the two observed counts if one annotator's boundaries are placed uniformly within the common eligible gaps $E_g$; it also equals the mean over the $K_g$ rank-cyclic shifts. Only the means coincide: the two distributions differ (e.g. $K=4$, $A=B=\{0,2\}$: $P(h=2)=1/2$ under shifts, $1/6$ under uniform placement), so $c_g$ is a descriptive baseline, not a p-value. The difference $d_g$ measures excess coincidence relative to that count-based baseline. It does **not** identify the musical or textual cause of the shared choices.

The primary conditional average $\widehat{\Delta}_B$ includes groups with both submissions, $K_g\ge 76$ (80% of 95 gaps) and $n_g+m_g\gt 0$ ($I_g=1$); `both_empty` groups are counted separately. If Phase G is completed, $\widehat{\Delta}_G$ is reported separately and only then $\widehat{\Theta}=\min(\widehat{\Delta}_B,\widehat{\Delta}_G)$ is computed as a descriptive conjunction. No ranking of the two traditions is implied.

**Selective abstention.** Restricting to $E_g$ can inflate agreement if one annotator abstains where the other marks boundaries. Synthetic case: A marks one shared and 19 further boundaries, B only the shared one ($a=2/21\approx 0.095$, $d=10/133\approx 0.075$); if B abstains on exactly those 19 gaps, $K=76$, $n=m=h=1$, $a=1$, $d=75/76\approx 0.987$, and the group still meets $K_g\ge 76$. Each group therefore reports abstentions by annotator and reason, together with the shares $\omega_A, \omega_B$ of one annotator's known boundaries falling in the other's abstentions (numerator and denominator; undefined when the denominator is zero). On the union $U_g=E_{g,\mathrm{technical}}\cap(E_{g,A}\cup E_{g,B})$ of technically available gaps reviewed by at least one annotator, we compute **exact sensitivity extrema** $[a_g^{\min},a_g^{\max}]$ and, separately, $[d_g^{\min},d_g^{\max}]$ over the set $\mathcal{C}_g$ of all binary completions of singly reviewed gaps $U_g\setminus E_g$. We recompute $n,m,h$ and $c$ for each completion, recording undefined cases. An additional synthetic check uses 76 commonly reviewed gaps with one shared boundary and 75 shared continuations, plus one gap where A records continuation and B abstains: completing B as continuation gives $a=1, d=76/77$, whereas completing B as boundary gives $a=2/3, d=50/77$. The exact intervals are therefore $a\in[2/3,1]$ and $d\in[50/77,76/77]$, showing that assigning all missing decisions to continuation is only one scenario and may overstate a lower bound when the known decision is continuation. With $K_g\ge 76$, no more than 19 single-sided gaps exist, making exhaustive enumeration of at most $2^{19}$ completions feasible per eligible group. We report $\widehat{\Delta}_B$ on its originally eligible groups ($I_g=1$), the equal-weighted average extrema of $d$ on these **same groups**, and $\widehat{\Delta}_B$ after excluding flagged groups (provisional flags: any defined $\omega\gt \omega^\star$ or $a_g^{\max}-a_g^{\min}\gt w^\star$, with provisional $\omega^\star=0.25$ and $w^\star=0.30$ to be finalised after calibration). These extrema describe sensitivity, not imputed expert judgements.

## Critical text-control analysis

A positive $d_g$ could be explained by shared decisions at word or syllable boundaries. We pre-register three mutually exclusive gap strata: (1) word boundary, (2) syllable boundary within a word, and (3) within-syllable gap. The text analysis uses a **separate domain** $E'_g \subseteq E_g$ of commonly reviewed gaps with verified alignment to exactly one stratum; $K'_g,n'_g,m'_g,h'_g,a'_g$ are recomputed from scratch on $E'_g$ and partitioned into $K_{g,s},n_{g,s},m_{g,s}$ ($\sum_s K_{g,s}=K'_g$, $\sum_s n_{g,s}=n'_g$, $\sum_s m_{g,s}=m'_g$):

$$
c_{g,\mathrm{text}}=\frac{2}{n'_g+m'_g}\sum_{s:K_{g,s}\gt 0}\frac{n_{g,s}m_{g,s}}{K_{g,s}},
\qquad d_{g,\mathrm{text}}=a'_g-c_{g,\mathrm{text}}.
$$

Mixing $a_g$ from $E_g$ with stratum counts from $E'_g$ is prohibited, as it can reverse the sign of the contrast. Coverage $|E'_g|/|E_g|$ and the unstratified $d'_g=a'_g-c'_g$ on the same $E'_g$ are reported alongside $d_{g,\mathrm{text}}$. Example: two annotators choosing the same 19 gaps that constitute **all** word ends of $E'$ ($K_{\mathrm{word}}=19$, $K'=95$) yield $a=1$, $c=0.20$, $d=0.80$, $c_{\mathrm{text}}=1$ and $d_{\mathrm{text}}=0$; with 30 word ends in the same domain, $c_{\mathrm{text}}=19/30$ and $d_{\mathrm{text}}\approx 0.37$. Musical–textual interaction is itself informative and is interpreted using both scores.

## Feasibility decisions

We propose overall common coverage $C=\sum_g K_g/(12\times 95)\ge 0.80$ ($K_g=0$ for `missing_submission`), and at least 10 of 12 groups with defined primary scores, as provisional *technical feasibility* criteria; at least 10 of 12 preselected groups that are **simultaneously eligible ($I_g=1$) and unflagged** as an *abstention-integrity* criterion; and a mean exact agreement $a_g\ge 0.70$ in Phase B as a separate provisional criterion for expanding musicological reference annotation. Evidence of positive excess coincidence is evaluated separately. These thresholds are protocol choices to be locked after calibration, not established empirical results.

An initial reference implementation passed 12/12 synthetic tests on fully reviewed inputs but ignores personal masks and `missing_submission` flags, computes the baseline $c$ over all 127 window gaps instead of $E_g$, does not restrict boundaries to gaps 17–111, rejects non-empty unresolved spans and bootstraps only defined groups; it is not used for empirical data. A separate numerical specification verified the formulas of the primary and text-stratified metrics on synthetic cases (11/11 tests; exhaustive checks over 5,454 and 22,500 cases). **Empirical data collection requires** a new evaluator that passes acceptance tests for punctured masks, full and selective abstention diagnostics (including $\omega$, undefined denominators and exact bounds on $U_g$), `technical_unavailable`, `missing_submission`, `unreviewed` rejection, `both_empty`, partial text alignment ($E'$), $\pm 1$ tolerance within contiguous eligible spans, registry-wide bootstrap and one real trial double submission with manual recount. Any bootstrap resampling must draw from all twelve preselected groups, recompute group eligibility in each replicate and count undefined resamples (e.g. with 1 eligible group out of 12, the probability of an undefined resample is $(11/12)^{12}\approx 0.352$).

## Relationship to the PhD and further work

The main PhD study M1 remains a joint *complete-position localisation plus family identity* task, using architecture A and representation-selection rule J. This boundary-agreement pilot has a different estimand, different reference labels and separate data splits; the M1 held-out test set remains strictly independent of this process. NHPYLM enters subsequently as a computational segmentation comparator.

The need to pre-specify the analytical scale of annotation before data collection is directly motivated by existing computational chant scholarship. In Byzantine chant, Mavromatis (2005, §5.3, Fig. 5.4, p. 78 / PDF p. 89) represents the three most probable HMM-generated settings of a given text phrase through decision points and chunks, where the phrase end is supplied externally (footnote 1). Those decision points, however, are branching nodes of a generative solution tree rather than boundaries marked by an expert on a single score; how they relate to expert-annotated boundaries remains an empirical question. Similarly, in Gregorian chant, Lanz and Hajič (2025, Fig. 2) contrast short statistically induced NHPYLM segments with broader musicological units. Together, these published examples underscore why boundary placement, recombination, reuse and variation must be kept analytically distinct, each requiring independently justified operational criteria and verified source material.

**Primary planned deliverable:** a fully documented, source-grounded feasibility study of independent expert boundary annotation in Phase B, while symbolic-corpus infrastructure and processing tools are developed in parallel within ByzCorpus.
