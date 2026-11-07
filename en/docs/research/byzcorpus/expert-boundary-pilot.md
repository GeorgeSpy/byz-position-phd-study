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
- **Window:** 128 atomic melodic events (indices 0–127) with 16 context events on either side of a 96-event scored centre (events 16–111). Gap `j` lies between events `j−1` and `j`; the **95 candidate internal gaps** are 17–111. Gaps 16 and 112 (centre/context edges) are not scored; the whole window has 127 internal gaps, which is never the pilot denominator.
- **Recording:** per gap and annotator, `boundary`, explicit `continuation`, or `abstain(reason)`; per gap, `technical_unavailable`; a gap with no recorded state (`unreviewed`) invalidates the submission until corrected and is never read as continuation. `missing_submission` and `both_empty` (two valid all-continuation submissions) are distinct outcomes.
- **Sampling:** freeze candidate works, source dependencies, musical context and sampling seeds before reading labels. Linked variants, witnesses and co-exegeses form grouped components. All twelve selected groups remain in the final registry regardless of missingness.

## Primary estimand

For each group `g`, let `E_g` be the intersection of technically available gaps reviewed by **both** annotators; `K_g=|E_g|`. Within `E_g`, let `n_g,m_g` be their boundary counts and `h_g` the count selected by both.

For `K_g>0` and `n_g+m_g>0`:

$$
a_g=\frac{2h_g}{n_g+m_g},\qquad
c_g=\frac{2n_gm_g}{K_g(n_g+m_g)},\qquad
d_g=a_g-c_g.
$$

Here `a_g` measures exact boundary F1 and `c_g` is its expectation given the two counts if one annotator's boundaries are placed uniformly within the common eligible gaps; it also equals the mean over the `K_g` rank-cyclic shifts. Only the means coincide: the two distributions differ (e.g. `K=4`, `A=B={0,2}`: `P(h=2)=1/2` under shifts, `1/6` under uniform placement), so `c_g` is a descriptive baseline, not a p-value. The `d_g` difference is excess coincidence relative to that count-based baseline. It does **not** identify the musical or textual cause of the shared choices.

The primary conditional average `Δ_B` includes groups with both submissions, `K_g≥76` (80% of 95 gaps) and at least one boundary chosen in total; both-empty groups are counted separately. If Phase G is completed, `Δ_G` is reported separately and only then `Θ=min(Δ_B,Δ_G)` as a descriptive conjunction. No ranking of the two traditions is implied.

**Selective abstention.** Restricting to `E_g` can inflate agreement if one annotator abstains where the other marks boundaries. Synthetic case: A marks one shared and 19 further boundaries, B only the shared one: `a=2/21`; if B abstains on exactly those 19 gaps, `K=76`, `a=1`, and the group still meets `K_g≥76`. Each group reports abstentions by annotator and reason and the shares `ω_A, ω_B` of one annotator's known boundaries falling in the other's abstentions (numerator and denominator; undefined when the denominator is zero). On the union `U_g` of technically available gaps reviewed by at least one annotator, calculate **exact sensitivity extrema** `[a_g^min,a_g^max]` and, separately, `[d_g^min,d_g^max]` over every binary completion of singly reviewed gaps. Recompute `n,m,h` and `c` for each completion, recording undefined cases. An additional synthetic check uses 76 commonly reviewed gaps with one shared boundary and 75 shared continuations, plus one gap where A records continuation and B abstains. Completing B as continuation gives `a=1, d=76/77`; completing B as boundary gives `a=2/3, d=50/77`. The exact intervals are therefore `a∈[2/3,1]` and `d∈[50/77,76/77]`. Assigning all missing decisions to continuation is only one scenario and may overstate a lower bound when the known decision is continuation. With `K_g≥76`, no more than 19 single-sided gaps exist, making exhaustive enumeration of at most `2^19` completions feasible per eligible group. Report `Δ_B` on its originally eligible groups, the average extrema of `d` on these **same groups**, and `Δ_B` after excluding flagged groups (provisional flags: any defined `ω>0.25` or `a_g^max−a_g^min>0.30`). These extrema describe sensitivity, not imputed expert judgements.

## Critical text-control analysis

A positive `d_g` could be due to shared decisions at word or syllable boundaries. Pre-register three exclusive gap strata: word boundary; syllable boundary within a word; within-syllable gap. The text analysis uses a **separate domain** `E′_g ⊆ E_g` of commonly reviewed gaps with verified alignment to exactly one stratum; `K′,n′,m′,h′,a′` are recomputed on `E′_g` and partitioned into `K_s,n_s,m_s`:

$$
c_{\mathrm{text}}=\frac{2}{n'+m'}\sum_{s:K_s>0}\frac{n_sm_s}{K_s},
\qquad d_{\mathrm{text}}=a'-c_{\mathrm{text}}.
$$

Mixing `a` from `E_g` with stratum counts from `E′_g` is not allowed: it can reverse the sign of the contrast. Coverage `|E′|/|E|` and the ordinary `d′` on `E′` are reported. Example: two annotators choosing the same 19 gaps that are **all** the word ends of `E′` (`K_word=19`, `K′=95`) yield `a=1`, `c=0.20`, `d=0.80`, `c_text=1`, `d_text=0`; with 30 word ends in the same domain, `d_text≈0.37`. Musical–textual interaction is itself informative and will be reported alongside these estimates.

## Feasibility decisions

We propose overall common coverage `ΣK_g/(12×95)` of at least 80%, and at least 10 of 12 groups with defined primary scores, as provisional *technical feasibility* criteria; at least 10 of 12 groups that are **both eligible for the primary average and unflagged** as an *abstention-integrity* criterion; and a mean exact agreement `a≥0.70` in Phase B as a separate provisional criterion for expanding musicological reference annotation. Evidence of positive excess coincidence is evaluated separately. These thresholds are protocol choices, not established empirical results.

An initial reference implementation passed 12/12 synthetic tests on fully reviewed inputs but ignores personal masks and missing-submission flags, computes the baseline over all 127 window gaps, does not restrict boundaries to gaps 17–111 and bootstraps only defined groups; it is not used for real data. A separate numerical specification reproduces the formulas above on synthetic cases (11/11 tests, exhaustive checks). **Real data collection requires** a new evaluator that passes acceptance tests for punctured masks, selective abstention diagnostics, `E′`, missing and both-empty groups, registry-wide bootstrap and one real trial double submission with manual recount. Any resampling must draw from all twelve preselected groups, recompute group eligibility and count undefined resamples.

## Relationship to the PhD and further work

The PhD study M1 remains a joint *complete-position localisation plus family identity* task, with its existing architecture A and representation-selection rule J. This feasibility pilot has distinct targets, labels and test groups. NHPYLM enters later as an independent segmentation comparator.

**Mavromatis (2005), Figure 5.4** (§5.3, printed p. 78 / PDF p. 89) organises, through decision points and chunks, the three most probable HMM-generated settings of a given text phrase whose end is supplied by hand (footnote 1); decision points are branch points of a solution tree, not boundaries marked by a reader in one score. **Lanz & Hajič (2025), Figure 2** relates statistical segments to larger musicological units. Both inform the study's distinction between boundary placement, recombination, reuse and variation; each interpretation requires independently justified operational criteria and appropriate source material.

**Initial planned output:** a modest, source-grounded feasibility study of independent boundary annotation in Phase B. Symbolic-corpus development and research tooling proceed as a parallel component of ByzCorpus.
