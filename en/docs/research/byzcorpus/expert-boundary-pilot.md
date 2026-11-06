# ByzCorpus — Expert boundary-agreement feasibility pilot

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά — full protocol](../../../../docs/research/byzcorpus/expert-boundary-pilot.md) · **English**
<!-- language-switch:end -->

[ByzCorpus](README.md) · [Data model (Greek)](../../../../docs/research/byzcorpus/data-model.md) · [NHPYLM pilot (Greek)](../../../../docs/research/byzcorpus/segmentation-pilot.md)

> **Status: draft for discussion, 6 November 2026.** Proposed research design for the meeting with Dr Jan Hajič Jr on 23 November. All quantities and eligibility thresholds remain subject to a joint calibration decision. No empirical annotations, validated performances, or collaboration agreement are being claimed.

## Rationale and objective

Our first proposed collaborative experiment asks whether **two independent specialists within each tradition** identify the same *internal melodic boundaries* at a mutually specified analytical scale. The preliminary repertoire pair is Byzantine papadic Koinonika and Gregorian responsories, subject to source availability and expert judgement.

This pilot aims to evaluate the **feasibility, coverage and usefulness of an independent musicological reference**. Reproducible NHPYLM and other computational segmentation baselines follow once this reference has been demonstrated. Recurrence, formula identity, memory efficiency and mode prediction are separate research questions.

## Proposed sample and annotation design

- **Calibration:** four independent works per tradition, with shared examples illustrating sub-chunk, target-scale and higher phrase boundaries; freeze the written guide before evaluation.
- **Evaluation:** twelve further independent source/work groups per tradition, one predetermined window per group; two independently submitting specialists per tradition. Total provisional design: 32 works and 64 first-pass judgements.
- **Window:** 128 atomic melodic events with 16 context events on either side of a 96-event scored centre, providing **95 candidate internal gaps**. Original gap identifiers are 17–111 in the full window; cropped endpoints are excluded.
- **Recording:** the two annotators mark each reviewed gap as boundary or continuation, with an abstention reason when appropriate. Reviewed-gap masks are stored separately; missing submissions, technical failures and two valid all-continuation submissions are distinct outcomes.
- **Sampling:** freeze candidate works, source dependencies, musical context and sampling seeds before reading labels. Linked variants, witnesses and co-exegeses form grouped components. All twelve selected groups remain in the final registry regardless of missingness.

## Primary estimand

For each group `g`, let `E_g` be the intersection of technically available gaps reviewed by **both** annotators; `K_g=|E_g|`. Within `E_g`, let `n_g,m_g` be their boundary counts and `h_g` the count selected by both.

For `K_g>0` and `n_g+m_g>0`:

$$
a_g=\frac{2h_g}{n_g+m_g},\qquad
c_g=\frac{2n_gm_g}{K_g(n_g+m_g)},\qquad
d_g=a_g-c_g.
$$

Here `a_g` measures exact boundary F1 and `c_g` is its expectation given the two counts if boundaries are placed uniformly within the common eligible gaps. The `d_g` difference is excess coincidence relative to that count-based baseline. It does **not** identify the musical or textual cause of the shared choices.

The primary conditional average includes groups with both submissions, `K_g≥76` (80% of 95 gaps) and at least one boundary chosen in total. Both-empty valid judgements are recorded separately with undefined F1. We report a mean `Δ_B` for the Byzantine annotator pair and `Δ_G` for the Gregorian pair, with `Θ=min(Δ_B,Δ_G)` as a descriptive conjunction of positive within-tradition effects. No ranking of the two traditions is implied.

## Critical text-control analysis

A positive `d_g` could be due to shared decisions at word or syllable boundaries. Pre-register three exclusive gap strata: word boundary; syllable boundary within a word; within-syllable gap. With `K_s,n_s,m_s` per stratum and common total `n,m`:

$$
c_{\mathrm{text}}=\frac{2}{n+m}\sum_{s:K_s>0}\frac{n_sm_s}{K_s},
\qquad d_{\mathrm{text}}=a-c_{\mathrm{text}}.
$$

For example, two annotators choosing the same 19 word ends among 95 gaps yield `a=1`, `c=0.20`, `d=0.80` but `d_text=0`. Musical–textual interaction is itself informative and will be reported alongside these estimates.

## Feasibility decisions

We propose overall common coverage of at least 80%, and at least 10 of 12 groups per tradition with defined primary scores, as provisional *technical feasibility* criteria. A mean exact agreement `a≥0.70` in both traditions is a separate provisional criterion for expanding musicological reference annotation. Evidence of positive excess coincidence is evaluated separately. These thresholds are protocol choices, not established empirical results.

The first Work reference evaluator passed 12/12 synthetic tests on fully audited inputs, but its current parser does not yet support partial annotation masks. **Real data collection requires** a complete work registry, explicit personal masks and abstentions, text strata, non-scoring endpoints and checks for missing submissions. Any resampling must draw from all twelve preselected groups per tradition, recompute group eligibility and count undefined resamples.

## Relationship to the PhD and further work

The PhD study M1 remains a joint *complete-position localisation plus family identity* task, with its existing architecture A and representation-selection rule J. This feasibility pilot has distinct targets, labels and test groups. NHPYLM enters later as an independent segmentation comparator.

The conceptual meeting examples are **Mavromatis (2005), Figure 5.4**, illustrating decision points and alternative melodic realisations, and **Lanz & Hajič (2025), Figure 2**, illustrating statistical segments in relation to larger musicological units. The opening question for Jan is which dimension of *segmentability* he primarily has in mind: boundary placement, recombination, reuse or variation. His answer should guide the annotation scale and the choice of Gregorian repertoire.

**Immediate proposed joint output:** a modest, source-grounded and independently annotated boundary-feasibility study, with a possible longer-term data/tooling track inspired by CantusCorpus and PyCantus.
