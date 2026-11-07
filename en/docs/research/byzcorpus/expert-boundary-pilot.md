# ByzCorpus — Pilot protocol for expert agreement on melodic boundaries

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../docs/research/byzcorpus/expert-boundary-pilot.md) · **English**
<!-- language-switch:end -->

[ByzCorpus](README.md) · [Data model (Greek)](../../../../docs/research/byzcorpus/data-model.md) · [Next stage: NHPYLM (Greek)](../../../../docs/research/byzcorpus/segmentation-pilot.md) · [Roadmap (Greek)](../../../../docs/research/byzcorpus/roadmap.md)

> **Standalone exploratory protocol · revision 7 November 2026.** This revision is grounded in a literature review, mathematical analysis of the metrics and controlled synthetic examples. Sources, genre, analytical scale and collection criteria are finalised through preliminary calibration. The current phase comprises the design and synthetic checks; no empirical expert judgements have been collected yet. M1, A2 and M2 retain their own protocols.

## 1. Why it precedes model training

The first study examines whether two independent specialists can reproducibly identify **internal melodic boundaries** at an agreed analytical scale. **Phase B** concerns papadic Koinonika of the New Method and is self-contained. A potential **Phase G** on a Gregorian genre (initially responsories) is designed separately, with its own sources, specialists and readiness criteria; genre selection will be based on source comparability and independent musicological assessment.

The intended outcome is a test of the **feasibility and usefulness of an independent musicological reference**. Its results will allow statistical segments (e.g. NHPYLM) to be evaluated in a subsequent stage. Any family-level classification requires additional independent membership criteria and a larger number of annotated occurrences.

Distinguishing analytical levels is mandatory: textual boundaries, musical boundaries, reusable chunks, complete formulae (*theseis*), functional roles and families are recorded as distinct types of decisions. A shared *evaluation protocol* makes it possible, if Phase G is also undertaken, to study the two traditions in parallel while preserving the specific musicological criteria of each.

## 2. Phases, scale and sampling

**Pipeline trial (Phase B).** One work outside the evaluation set, with an identified witness, an admissible transcription and one verified window. Two complete trial submissions, symbol → event → gap mapping and a manual recount of the evaluator output.

**Calibration B:** four independent practice works. Specialists examine counterexamples for (i) smaller internal subdivisions, (ii) the target boundary scale, and (iii) larger phrase boundaries. The annotation guide, primary scale, visible information (source, text) and thresholds are finalised before main data collection.

**Main collection B:** 12 further independent groups, one work and one pre-declared window per group, scored by the same two specialists. This yields **24 independent first-pass readings** in evaluation and 32 including calibration, subject to source adequacy and verifiable independence across works.

**Potential Phase G:** separate 4+12 groups of the selected Gregorian genre, two dedicated specialists, and dedicated documentation of sources, rights and event geometry. Only if both phases are completed is a joint descriptive summary defined (§4).

Entries are partitioned into connected components of works, witnesses, editorial dependencies, shared exegeses and near-identical melodies. The sampling frame, technical exclusions, source licences and selection seed are fixed before judgements are collected. **Every preselected group** remains in the registry even if a submission is missing.

The [Gheorghiță inventory](../corpus/README.md) serves as a starting point for locating Byzantine sources. Its 338 rows are primarily catalogue metadata rather than complete symbolic scores. The 35 passages with parallel exegeses come from eight works by Daniel and require verification of actual manuscript witnesses and dependencies; they do not determine the size of an independent sample.

## 3. Predetermined window and commonly reviewed gaps

Each window contains **128 consecutive atomic melodic events** indexed 0–127: 16 left-context events, 96 central evaluation events (16–111) and 16 right-context events.

**Numbering convention:** gap $`j`$ lies between events $`j-1`$ and $`j`$. The internal gaps of the central region are $`17,\ldots,111`$, giving **95 initial gap IDs**. Gaps 16 and 112 (centre–context edges) are not scored. The full window has 127 internal gaps; **the pilot denominator can never be 127**.

For each group $`g`$ the following are stored:

- `eligible_gap_ids`: the 95 candidate initial IDs, with separate technical exclusions;
- `annotator_A_reviewed_ids`, `annotator_B_reviewed_ids`: personal masks of positions actually reviewed;
- `annotator_A_boundary_ids`, `annotator_B_boundary_ids`: the boundaries selected by each specialist;
- the state of each gap and each submission according to the table below;
- `level_id`, `source_id`, `work_group_id`, `window_start`, `text_stratum`, editorial provenance and timestamp of judgement.

| Level | State | Meaning | Role in analysis |
|---|---|---|---|
| gap, per specialist | `boundary` | explicit boundary selection | counts towards $`n,\, m,\, h`$ within $`E_g`$ |
| gap, per specialist | `continuation` | explicit non-boundary judgement; never implicit | belongs to $`E_g`$ |
| gap, per specialist | `abstain(reason)` | inability to judge with recorded reason | outside $`E_g`$; mandatory diagnostics in §4.1 |
| gap | `technical_unavailable` | unsuitable for reliable technical reading | outside $`E_{g,\mathrm{technical}}`$ |
| gap, per specialist | `unreviewed` | gap with no recorded state | invalid submission; returned for completion before analysis; never converted into `continuation` |
| submission | `missing_submission` | specialist submission absent | group remains in registry; $`K_g=0`$ in coverage index |
| group | `both_empty` | $`n_g=m_g=0`$ with $`K_g\gt 0`$ | $`a_g`$ undefined; counted separately |

A negative annotation (`continuation`) arises only for a gap that the specialist explicitly declared as reviewed. The commonly reviewed domain is:

```math
E_g = E_{g,\mathrm{technical}} \cap E_{g,A} \cap E_{g,B},\qquad K_g=|E_g|.
```

Initial gap IDs are preserved: holes in the masks **do not create new adjacent pitch events**. A $`\pm 1`$ tolerance is reported only as a separate diagnostic metric, strictly within the same contiguous eligible span and under one-to-one matching.

## 4. Primary agreement estimand

For each group, within the common domain $`E_g`$, let $`A_g,\, B_g`$ be the sets of internal boundaries, $`n_g=|A_g|`$, $`m_g=|B_g|`$ and $`h_g=|A_g\cap B_g|`$.

When $`K_g\gt 0`$ and $`n_g+m_g\gt 0`$:

```math
a_g=\frac{2h_g}{n_g+m_g},\qquad
c_g=\frac{2n_gm_g}{K_g(n_g+m_g)},\qquad
d_g=a_g-c_g.
```

Here $`a_g`$ is exact boundary agreement measured as symmetric F1. The term $`c_g`$ is the expected value of $`a_g`$ when, holding the **observed counts** $`n_g,\, m_g`$ fixed, one specialist's selections are placed uniformly within the common domain $`E_g`$; it also equals the mean across the $`K_g`$ cyclic shifts along the rank order of eligible gaps. This equality holds **only for the mean**: the two distributions differ (e.g. $`K=4`$, $`A=B=\{0,2\}`$: $`P(h=2)=1/2`$ under cyclic shifts versus $`1/6`$ under uniform placement). Thus $`c_g`$ is a descriptive baseline and is not used as a p-value. The difference $`d_g`$ captures excess coincidence beyond this baseline; because the maximum attainable $`d_g`$ depends on $`n_g,\, m_g,\, K_g`$, the counts $`n_g,\, m_g`$ are always reported alongside it.

**Inclusion in the primary mean:** two completed submissions, $`K_g\ge 76`$ (80% of 95) and $`n_g+m_g\gt 0`$. We set $`I_g=1`$ if and only if these conditions hold. Remaining works stay in the report with their reason for exclusion.

- If only one specialist marks boundaries, then $`a_g=c_g=d_g=0`$, provided coverage requirements are met.
- If neither specialist marks boundaries, the group is recorded as `both_empty` (**shared absence of internal articulation** within the reviewed domain) and $`a_g`$ is undefined. The group is reported with its coverage, without artificially assigning a zero F1.
- If judgements are missing or partial abstention occurs, evaluation is restricted strictly to the commonly reviewed domain $`E_g`$, accompanied by the mandatory diagnostics of §4.1.

```math
\widehat{\Delta}_B=\frac{\sum_g I_gd_g}{\sum_g I_g}.
```

For Phase B, **the primary estimand is $`\widehat{\Delta}_B`$**, conditional on evaluable groups ($`I_g=1`$); the counts of `both_empty` and excluded groups are reported alongside it. If Phase G is completed, $`\widehat{\Delta}_G`$ is defined analogously and reported separately; only then is the descriptive summary $`\widehat{\Theta}=\min(\widehat{\Delta}_B,\widehat{\Delta}_G)`$ computed, remaining undefined whenever either mean is undefined. The quantities $`\Delta_B,\, \Delta_G`$ concern **specific specialist pairs, repertoires, genres and conditionally evaluable groups**; they do not rank the relative "ease" of the two traditions.

### 4.1 Selective abstention: mandatory diagnostics

Restricting evaluation to $`E_g`$ is necessary, but if one specialist's abstentions coincide with the other's boundaries, $`a_g`$ can overstate agreement. Synthetic example across 95 gaps: A selects one shared boundary plus 19 additional boundaries, whereas B selects only the shared one. Under full review, $`a=2/21\approx 0.095`$ and $`d=10/133\approx 0.075`$. If B abstains on precisely the 19 contested gaps, then $`K=76`$, $`n=m=h=1`$, $`a=1`$ and $`d=75/76\approx 0.987`$, while the group still satisfies $`K_g\ge 76`$.

For every group, the following are reported mandatorily:

- abstention counts per specialist and per reason;
- $`\omega_B`$: the proportion of A's known boundaries (within the technically available domain explicitly reviewed by A) on which B abstained, and symmetrically $`\omega_A`$. Both numerator and denominator are reported. If the denominator is zero, the corresponding $`\omega`$ is **undefined** and explicitly flagged as such;
- **exact sensitivity bounds** on $`U_g=E_{g,\mathrm{technical}}\cap(E_{g,A}\cup E_{g,B})`$. At each gap in $`U_g\setminus E_g`$ there is one known decision (`boundary`/`continuation`) and one abstention; the unknown decision may take either value. Let $`\mathcal{C}_g`$ be the set of all such compatible binary completions. For each completion we recompute $`K=|U_g|,\, n,\, m,\, h,\, a,\, c,\, d`$. We define **separately** $`a_g^{\min}=\min_{\xi\in\mathcal{C}_g}a(\xi)`$, $`a_g^{\max}=\max_{\xi\in\mathcal{C}_g}a(\xi)`$ and analogously $`d_g^{\min},\, d_g^{\max}`$. Only completions yielding a defined metric are optimised over, while undefined completions are logged. These values describe sensitivity bounds under the declared unknown judgements without substituting for actual annotations.

**Extrema check.** Across 76 commonly reviewed gaps, the two specialists agree on one boundary and 75 continuations. On one additional gap, A marks `continuation` and B abstains. If B's unknown decision is completed as `continuation`, we obtain $`a=1`$ and $`d=76/77`$. If it is completed as `boundary`, we obtain $`a=2/3`$ and $`d=50/77`$. The exact bounds are therefore $`a\in[2/3,\, 1]`$ and $`d\in[50/77,\, 76/77]`$. This example verifies that replacing all abstentions with `continuation` does not necessarily yield the minimum agreement.

**Critical detail:** replacing every abstention with `continuation` represents one specific scenario, not a general lower bound. Whenever the other specialist has recorded `continuation`, an unknown `boundary` decision can lower agreement. Likewise, the extrema of $`d=a-c`$ must be found independently because $`c`$ also varies across completions. With $`K_g\ge 76`$, there are at most 19 singly reviewed gaps in the 95-gap window, so exact enumeration requires at most $`2^{19}`$ completions per evaluable group; an alternative verified implementation is permitted provided it returns the exact same extrema.

Three analyses are pre-declared: (i) $`\widehat{\Delta}_B`$ across all groups with $`I_g=1`$; (ii) the equal-weighted mean of $`d_g^{\min}`$ and of $`d_g^{\max}`$ across the **same initially evaluable groups**, alongside a separate report of the $`a`$ bounds; and (iii) $`\widehat{\Delta}_B`$ after excluding flagged groups. An evaluable group is flagged if any defined $`\omega`$ exceeds $`\omega^\star`$ or if $`a_g^{\max}-a_g^{\min}\gt w^\star`$, with provisional thresholds $`\omega^\star=0.25`$ and $`w^\star=0.30`$ to be finalised after calibration. Undefined $`\omega`$ values are recorded and assessed separately.

## 5. Text-controlled interpretation check

A positive value of $`d_g`$ may be explained by shared textual boundaries. Three predetermined, mutually exclusive categories are checked separately:

1. word end,
2. syllable boundary within a word,
3. within-syllable gap.

The textual check is performed on a **separate domain** $`E'_g \subseteq E_g`$, namely the commonly reviewed gaps with a verified assignment to exactly one textual category. The quantities $`K'_g,\, n'_g,\, m'_g,\, h'_g,\, a'_g`$ are recomputed from scratch on $`E'_g`$, while $`K_{g,s},\, n_{g,s},\, m_{g,s}`$ partition those counts across each category $`s`$:

```math
\sum_s K_{g,s}=K'_g,\qquad \sum_s n_{g,s}=n'_g,\qquad \sum_s m_{g,s}=m'_g,
```

```math
c_{g,\mathrm{text}}=
\frac{2}{n'_g+m'_g}\sum_{s:K_{g,s}\gt 0}\frac{n_{g,s}m_{g,s}}{K_{g,s}},
\qquad d_{g,\mathrm{text}}=a'_g-c_{g,\mathrm{text}}.
```

When $`E'_g`$ is empty or $`n'_g+m'_g=0`$, the text-controlled value remains undefined. We report the coverage $`|E'_g|/|E_g|`$, the ordinary unstratified difference $`d'_g=a'_g-c'_g`$ on the same $`E'_g`$, the groups contributing to the text-controlled mean and the reason for any undefined value. The primary unstratified metric uses the original $`E_g`$. Mixing $`a_g`$ (computed on $`E_g`$) with category counts from $`E'_g`$ is prohibited, as it can reverse the sign of the textual contrast.

The metric $`d_{\mathrm{text}}`$ evaluates excess coincidence after preserving each specialist's allocation of boundaries across textual categories. Example: if both specialists select the exact same 19 gaps and these constitute **all** word ends in $`E'`$ ($`K_{\mathrm{word}}=19`$, $`K'=95`$), then $`a=1`$, $`c=0.20`$, $`d=0.80`$, $`c_{\mathrm{text}}=1`$ and $`d_{\mathrm{text}}=0`$. If the same domain contained 30 word ends, we would obtain $`c_{\mathrm{text}}=19/30`$ and $`d_{\mathrm{text}}\approx 0.37`$. Textual and melodic cues may jointly contribute to phrasing; interpretation examines both scores together.

## 6. Reporting, uncertainty and progression criteria

**Per-phase reporting:** a full registry of all 12 preselected groups, $`K,\, n,\, m,\, h,\, a,\, c,\, d,\, I`$, exclusion reasons, individual abstentions and $`\omega`$ (including undefined values), exact sensitivity bounds for $`a,\, d`$, technical coverage, `both_empty` counts, textual categories and $`E'`$, boundary rate, median and mean. A separate corpus-level micro-F1 is also reported without replacing the equal-weighted group mean.

**Coverage index:** $`C=\sum_g K_g/(12\times 95)`$, with $`K_g=0`$ for any group with `missing_submission`. Technical availability, coverage among participating specialists and per-specialist abstentions are reported separately.

**Uncertainty:** leave-one-group-out and descriptive grouped bootstrap (e.g. 5,000 replications with a logged seed), resampling **all 12 preselected groups** and recomputing eligibility within each replication. Resampling only the evaluable groups is not permitted because it ignores variability in eligibility itself. Undefined replications are counted explicitly (e.g. with one evaluable group out of 12, the probability of an undefined replication is $`(11/12)^{12}\approx 0.352`$). With a single pair of specialists, intervals describe variability across work groups rather than across a population of readers, and therefore have an exploratory character.

**Collection-readiness gate:** valid sources and licences, two available specialists for Phase B, locked scale level and annotation guide, successful pipeline trial, verified events and gaps, complete manifest and an evaluator passing all acceptance tests below.

**Technical-feasibility gate:** $`C\ge 0.80`$ and at least 10 out of 12 defined groups. **Abstention-integrity gate:** at least 10 out of the 12 preselected groups must be **simultaneously evaluable ($`I_g=1`$) and unflagged** under §4.1; otherwise the report remains descriptive with respect to abstention sensitivity. **Reference-usefulness gate:** an initial target mean of $`a_g\ge 0.70`$, accompanied by sensitivity bounds, uncertainty and disagreement types. A positive $`d`$ is treated as a separate research observation. All thresholds are provisional choices to be finalised after calibration and before main collection.

**Implementation status.** No tool is yet deployed for real submissions. An initial prototype implementation passed 12/12 synthetic tests on complete inputs, but ignores personal masks and the `missing_submission` flag, computes the baseline $`c`$ over all 127 internal window gaps rather than $`E_g`$, does not restrict boundaries to gaps 17–111, rejects non-empty unresolved spans and resamples only defined groups during bootstrapping; it is not used on empirical data. A separate numerical specification verified the formulas of §§4–5 on synthetic data (11/11 tests; exhaustive checks across 5,454 and 22,500 cases). The new implementation is accepted only when it reproduces the specification across: punctured masks, full and selective abstention (including $`\omega`$, undefined denominators and **exact** bounds on $`U_g`$), `technical_unavailable`, `missing_submission`, `unreviewed` (rejection), `both_empty`, partial textual alignment ($`E'`$), $`\pm 1`$ tolerance within contiguous spans, registry-wide bootstrap, and one trial double submission on a real source with manual recount. Evaluator code is **not included** in the present repository.

## 7. Relationship to the next computational stage and to M1

Following independent annotation and reference validation, fixed-length partitions, textual boundary sets and NHPYLM can be evaluated. Reproducing the interval/pitch encoding of the public Lanz–Hajič code requires a strict check of conventions and source versions. Outputs of n-gram features extracted from overlapping windows are recorded separately from full-melody segmentation.

The main **M1** study in the core research proposal continues to estimate *complete formula boundaries and correct family identity* via **architecture A** and **selection rule J**. The present internal-boundary annotation has a different estimand, different reference labels and separate data identifiers. The M1 test/held-out set is kept strictly independent of this procedure. NHPYLM remains a comparison model.

## 8. Literature references on scale and next steps

The need to distinguish annotation scales explicitly before data collection follows directly from existing computational chant scholarship. In Byzantine chant, Mavromatis (2005, §5.3, Fig. 5.4, p. 78 / PDF p. 89) represents through decision points and chunks the three most probable HMM-generated settings of a text phrase, where the phrase end is supplied externally (footnote 1). Those decision points, however, are branching nodes of a generative solution tree rather than boundaries marked by a specialist on a specific score; to what extent they coincide with the boundaries of the present pilot remains an open empirical question. Similarly, in Gregorian chant, Lanz and Hajič (2025, Fig. 2) contrast short statistically induced NHPYLM segments with broader musicological units. Both cases demonstrate why the protocol must define the analytical scale and testable criteria of segmentability in advance.

Finalising the annotation guide requires an authentic Byzantine example from a documented source, independent calibration of instructions on the practice works and a clear record of visible information (and, if Phase G is activated, a corresponding eligible Gregorian case).

**Primary intended deliverable:** a fully documented pilot study of expert agreement on melodic boundaries in Phase B, while symbolic infrastructure and processing tools are developed in parallel within ByzCorpus.
