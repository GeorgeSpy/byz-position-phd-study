# Statistical Segmentation and Musicological Boundaries in Gregorian and Byzantine Chant

*ByzCorpus comparative pilot study*

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../docs/research/byzcorpus/gregorian-nhpylm-helsen-pilot.md) · **English**
<!-- language-switch:end -->

[ByzCorpus](README.md) · [Expert-boundary agreement pilot](expert-boundary-pilot.md) · [Byzantine NHPYLM protocol (Greek)](../../../../docs/research/byzcorpus/segmentation-pilot.md) · [Roadmap (Greek)](../../../../docs/research/byzcorpus/roadmap.md) · [M1-X](../m1-x-design.md) · [Gheorghiță inventory](../corpus/README.md)

## 1. Purpose

This pilot study examines how statistically induced melodic segments relate to musicological boundaries and to the internal organisation of larger melodic units. The Nested Hierarchical Pitman–Yor Language Model (NHPYLM) [2] induces recurrent melodic segments directly from continuous symbolic sequences. Lanz and Hajič (2025) evaluated it in Gregorian chant in terms of memorisation efficiency (perplexity) and mode classification. Their visual comparison of a single example (Figure 2 in [1]) with Levy's musicological analysis revealed that the induced segments were much more fragmented than the units associated with *centonisation*. They also proposed comparisons with other traditions possessing documented melodic formulae, including Byzantine chant, and emphasised the need for suitable datasets [1]. Probabilistic models of melodic generation have also been proposed for the echoi of modern Greek church chant [3, 4]. Musicological analysis identifies larger units—elements, melodic types and complete positions—organised by modal and functional relationships.

To examine this difference in analytical scale systematically, the study develops and evaluates a **comparative framework** based on musicologically documented boundaries and analytical categories. Its tests distinguish information supplied by the model from the effects of boundary density and melodic similarity. The Gregorian component has been carried out on Great Responsories, using Helsen's analysis as the reference [5, 6]. The Byzantine component is planned for papadic Koinonika in New Method notation, with Gheorghiță's study [9] as its principal historical reference and independent expert annotation of complete melodic-position boundaries.

### 1.1 Terminology

- **Statistical segment:** a contiguous subsequence of note events automatically induced by the NHPYLM.
- **Helsen element:** a musicologically delimited unit of a responsory. Each element begins after the preceding element's cadential figure [5, p. 57]. It receives a standard label if it occurs at least five times in at least three responsories; otherwise it receives a provisional label.
- **Analytical family:** a category of occurrences sharing structural and modal criteria. In the Gregorian component, standard Helsen labels serve as a proxy; in the Byzantine component, the relevant categories are the analytical families of ByzCorpus, with Gheorghiță's historically documented notational formations treated as distinct evidence categories.
- **Complete melodic position (θέσις):** the central structural unit studied in ByzCorpus. Comparison with a Helsen element concerns the analytical scale of the two traditions and does not presume equivalence between their units.
- **Occurrence / realisation / historically named type:** distinct levels of documentation. Helsen's and Frere's labels are modern analytical categories, whereas Gheorghiță's formations bear historical names associated with the great signs of the older notation.

## 2. Research questions and hypotheses

- **RQ1 — Boundary alignment.** To what extent do NHPYLM boundaries in held-out works coincide with musicological boundaries, compared with random segmentation preserving both segment count and segment lengths?
- **RQ2 — Boundary selection.** How effectively can musicological boundaries be recovered from the dense set of statistical cuts, and how does the model compare with simple rules specified in advance?
- **RQ3 — Internal organisation.** Are internal cuts more consistent among occurrences of the same family than among occurrences of different families matched for melodic similarity?
- **RQ4 — Larger-scale units.** Do shared internal coherence and family-specific structural relationships provide additional predictive information for recognising complete melodic units?
- **RQ5 — Cross-tradition comparison.** Which findings from RQ1–RQ4 persist in papadic chant, where multiple positions can unfold within one syllable?

The Gregorian pilot provides empirical evidence for RQ1–RQ3 (§3). The following hypotheses are specified for the Byzantine component. Each confirmatory hypothesis has three possible outcomes: **supported** when the entire 95% confidence interval (CI) falls on the predicted side of its reference value, **rejected** when it falls entirely on the opposite side, and **unresolved** when it includes the reference value. The bootstrap sampling unit for the Byzantine component is the work, with composer-level sensitivity analysis.

| Hypothesis | Prediction | Measure and reference value |
|---|---|---|
| **H-S1** | A substantially smaller proportion of reference boundaries in Koinonika coincides with word endings than in responsories | Share of reference boundaries at word endings; Gregorian reference 0.9937 |
| **H-S2** | NHPYLM boundaries align with reference boundaries in both traditions | $`\Delta_R`$ versus a length-preserving random reference; reference 0 |
| **H-S3** | Given the same number of predicted boundaries in Koinonika, NHPYLM boundary probabilities outperform a mode-specific cadence rule | Paired F1 difference in expert-annotated windows with complete boundary annotation; reference 0. Supplementary recall at identified Gheorghiță-formation boundaries |
| **H-S4** | Occurrences of the same historically documented formation, and separately of the same musicologically validated analytical family, have more consistent internal cuts than matched occurrences from another category | Matched $`\Delta J`$ at each category level; reference 0 |
| **H-S5** (exploratory) | The two exegeses of the same historical passage (Gregory and Chourmouzios) yield more consistent segmentation than different passages of the same formation | Paired Jaccard difference across 35 parallel cases; reference 0 |

For H-S1, a word ending is the gap after the last note event of the last syllable of a word. H-S1–H-S4 are confirmatory; H-S5 is exploratory because the 35 parallel exegeses come from eight Koinonika by Daniel Protopsaltes. No direction is predicted for the between-tradition difference in H-S4.

## 3. Gregorian chant pilot: methods and results

### 3.1 Material

**Phase A (CantusCorpus).** From CantusCorpus v0.2 [7], 995 complete responsories from Paris, BnF, lat. 12044 were selected in Volpiano representation. We used the `full_melodies` representation from the code of Lanz and Hajič [1], in which a flat replaces the note symbol it modifies. Text-related boundaries (neume, syllable, word and division) were removed from model input and retained solely for evaluation.

Duplicate entries and closely related melodic versions were grouped into 935 melody clusters, using identical Cantus IDs or a Jaccard similarity of at least 0.5 between note eight-grams. The two-fold split was performed by cluster. The NHPYLM was trained for 200 epochs in each fold using the published hyperparameters, a maximum segment length of $`L_{\max}=7`$ and Viterbi decoding. Each work was therefore segmented with a model that had not encountered its cluster during training.

The *repetenda* boundary was evaluated in 887 responsories with one internal division. In 883 of 900 cases with both a division and a verse-text cue, the cue agreed with the text following the division. The Phase A protocol was recorded before training.

**Phase B (Helsen database).** The 1,668 Mode 1 records from Helsen's database [5] were extracted: 214 responsories, comprising 1,056 records with standard labels and 612 with provisional labels. Each responsory was reconstructed from consecutive phrases ordered by the `Position` field. Works were identified through their CAO number and *incipit*; the database's `Source` field denotes a biblical textual source rather than a manuscript. Phase B reuses the out-of-fold segmentations from Phase A.

Comparison with CantusCorpus yielded 19 exact matches, 129 melodies at normalised edit distance up to 0.05, 51 at distances between 0.05 and 0.15, four above 0.15 and 11 with no match. The **primary analysis** comprises the **148 melodies** at distance at most 0.05, belonging to 146 melody clusters. Sequence alignment projected **954 internal Helsen-element boundaries** onto the Cantus melodies; 28 boundaries were excluded because of local alignment ambiguity. As a validation check, the Helsen *repetenda* boundary coincided exactly with the Cantus division in 134 of 137 evaluable instances.

**Departures from the preregistered protocol.** The original Phase B code was run first. Three errors were then corrected:

1. The work-matching key included the `Source` field.
2. Alignment distinguished upper- and lower-case letters, thereby treating liquescent differences as mismatches.
3. The *incipit* matching procedure was excessively strict.

Results from the original code are reported separately (§3.4).

### 3.2 Measures

Let $`E`$ denote the reference boundaries and $`B`$ the boundaries predicted by the model. We use $`\mathrm{Recall}=|E\cap B|/|E|`$, $`\mathrm{Precision}=|E\cap B|/|B|`$, and $`F_1`$ as their harmonic mean. The definitions are retained for the Byzantine component: precision and F1 for complete positions are computed in jointly annotated windows with a complete boundary partition, whereas recall of identified boundaries is computed for Gheorghiță's documented formations.

- **Recall against a random reference.** Greater boundary density increases expected recall even in the absence of informative placement. The principal reference therefore randomly permutes the same statistical-segment lengths within each chant, keeping the number of boundaries per work exactly constant. The main effect is $`\Delta_R=R_{\mathrm{NHPYLM}}-R_{\mathrm{random}}`$. The 95% CIs are obtained by 10,000 bootstrap replicates, sampling at the level of melody clusters.
- **Cadence rule.** The comparison with the NHPYLM uses a paired cluster bootstrap with 10,000 replicates across the same 146 clusters. Each replicate pools the two methods' TP, FP and FN counts and recomputes corpus-level micro-F1. The rule was specified before the execution of Phase B. It selects word endings whose final pitches are C, D, F or a—encoded as `c`, `d`, `f`, `h` in Volpiano. These are Mode 1 tonal goals in Helsen's analysis. Accordingly, the rule shares musical criteria with the reference and provides a strong comparator.
- **Internal cuts (RQ3).** Jaccard similarity is computed on internal NHPYLM cuts after dynamic melodic alignment. In the unmatched comparison, same-label occurrence pairs from different melody clusters (alignment distance at most 0.25) are compared with random cuts preserving their number. In the matched comparison, each same-label pair $`(x,x')`$ is paired with an occurrence $`y`$ bearing a different label and belonging to a third melody cluster. The length and number of cuts in $`y`$ differ by at most one from those of $`x'`$. Its distance to $`x`$ differs by at most 0.05 from $`d(x,x')`$; the closest qualifying candidate is selected. An occurrence $`y`$ may be reused in multiple triples. The 95% CI of $`\Delta J`$ comes from 2,000 bootstrap replicates with the analytical label as sampling unit.

### 3.3 Results

**Phase A — *repetenda* boundary (887 responsories, 879 clusters).**

| Measure | Estimate | 95% CI |
|---|---:|---:|
| NHPYLM recall | 0.8929 | 0.8725–0.9126 |
| Length-preserving random reference | 0.4997 | 0.4921–0.5075 |
| **Difference $`\Delta_R`$** | **+0.3932** | **0.3711–0.4146** |
| NHPYLM recall at other word endings | 0.7367 | 0.7278–0.7457 |
| Recall with ±1-note tolerance | 0.9876 | 0.9797–0.9944 |

The model predicts a mean of 64.64 internal boundaries per responsory. Mean segment length is 1.967 notes, and 60.79% of the segments are single notes. In an exploratory analysis, boundary frequency increases with the structural salience of the gap: 0.42 within a neume, 0.44 between neumes, 0.62 at a syllable ending, 0.74 at a word ending and 0.89 at the *repetenda* boundary.

**Phase B — Helsen-element boundaries (148 responsories, 954 boundaries).**

| Measure | Estimate | 95% CI |
|---|---:|---:|
| Exact NHPYLM recall | **0.8994** | 0.8774–0.9206 |
| Length-preserving random reference | 0.5192 | — |
| **Difference $`\Delta_R`$** | **+0.3802** | **0.3528–0.4060** |
| Recall with ±1-note tolerance | 0.9790 | — |
| NHPYLM precision over all gaps | 0.0770 | — |
| NHPYLM F1 over all gaps | 0.1418 | — |

The model recovers nearly 90% of Helsen's boundaries, a recall advantage of 38 percentage points over the random reference. It operates at a much smaller scale, however: it predicts 75.32 boundaries per chant compared with 6.45 for Helsen's reference. An element has a median length of 19 notes, while $`L_{\max}=7`$ requires at least three statistical segments. In the observed output, the median element contains eight internal cuts, or approximately nine statistical segments.

**Boundary selection at word endings.**

| Condition | Boundaries/chant | Recall | Precision | F1 |
|---|---:|---:|---:|---:|
| All word endings | 18.89 | 0.9937 | 0.3392 | 0.5057 |
| Word ending + final pitch C, D, F, a | 13.49 | 0.8742 | 0.4176 | **0.5652** |
| NHPYLM restricted to word endings | 14.86 | 0.8941 | 0.3877 | 0.5409 |
| NHPYLM at all gaps | 75.32 | 0.8994 | 0.0770 | 0.1418 |

A total of 99.37% of Helsen's reference boundaries fall at word endings. Restricting candidates to word endings raises NHPYLM F1 from 0.1418 to 0.5409. The cadence rule remains stronger: paired F1 difference **+0.0243**, 95% CI 0.0085–0.0401. This is consistent with Helsen's definition, whereby each element begins after a cadential figure.

**Internal cuts and analytical labels (exploratory).** In the unmatched comparison (792 pairs, 43 labels), same-label Jaccard similarity is 0.3392 versus 0.1549 for random cuts of the same count ($`\Delta J=+0.1843`$). Since occurrences with the same label are also melodically similar, a matched comparison was conducted:

| Matched comparison | Value |
|---|---:|
| Ordered same-label pairs | 1,584 |
| Matched triples | **418** (26.4%) |
| Labels represented | 28 |
| Mean same-label Jaccard | 0.2783 |
| Mean different-label Jaccard | 0.2254 |
| **Difference $`\Delta J`$** | **+0.0528** |
| 95% CI (label-level bootstrap) | 0.0359–0.1284 |

Matching accounts for much of the original difference, leaving a positive residual associated with the analytical label. This result concerns the 26% of pairs for which a match was available. Helsen labels and Frere symbols have Normalised Mutual Information of 0.7944 across 196 records in the primary sample; across the full database, only 13% of records carry a Frere symbol. The two classifications share analytical assumptions, and both refer to elements delimited by Helsen.

### 3.4 Sensitivity analyses

| Condition | Responsories | Boundaries | NHPYLM recall | $`\Delta_R`$ |
|---|---:|---:|---:|---:|
| Mode 1, distance at most 0.05 (primary) | 148 | 954 | 0.8994 | +0.3802 |
| Mode 1, distance at most 0.15 | 199 | 1,304 | 0.8980 | +0.3698 |
| Preregistered code, before corrections | 113 | 709 | 0.8914 | +0.3830 |
| All modes, distance at most 0.05 (exploratory) | 626 | 3,798 | 0.8605 | +0.3733 |

The recall advantage over the random reference remains positive and of similar magnitude across conditions. Across all modes, NHPYLM restricted to word endings yields F1 of 0.5276, compared with 0.4918 for selecting all word endings. The cadence rule cannot be extended to all modes without separately specified sets of final pitches for each mode.

### 3.5 Scope and limitations

- This evaluation uses the basic unsupervised NHPYLM with a shared segment lexicon. The NHPYLMClasses variant of Lanz and Hajič (2025) trains eight separate models using known mode labels and provides a distinct target for future comparison [1].
- One manuscript and one analyst: Helsen provides the reference boundaries.
- One training seed per fold. A second seed has not yet been run, so between-training variation has not been estimated.
- The primary Phase B analysis concerns Mode 1; the extension to all modes is exploratory.
- Boundaries are projected between two transcriptions of the same manuscript.
- Boundary evaluation uses hard Viterbi decoding; marginal boundary probabilities have not yet been extracted.
- Jaccard is exploratory and uses matching with reuse of different-label occurrences.

### 3.6 Main findings of the Gregorian pilot

1. Statistical-segment transitions systematically align with musicological boundaries and substantially outperform a random reference at the same boundary density.
2. The model operates at a scale of approximately two notes and produces a dense set of candidate boundaries that must be ranked to recover musicological elements.
3. In Gregorian responsories, word endings combined with final pitch predict much of the musicological segmentation more accurately than the model.
4. Analytical labels are associated with a small additional consistency of internal cuts after matching melodic distance, length and cut count.

Two questions remain: the **selection** of musically significant boundaries from dense segmentations, and the **composition of larger units**—how a 19-note element containing about nine subsegments arises from local and long-range relationships.

## 4. Rationale for comparison with Byzantine chant

In Gregorian responsories, almost all Helsen-element boundaries occur at word endings, making textual articulation highly informative for selecting boundaries. In Gregorian antiphons, Lanz and Hajič (2023) found that text boundaries do not yield better segmentation when evaluated through mode classification [8]. Here the target is the annotated boundary of a melodic element, which coincides with a word ending in nearly every case. In papadic and kalophonic chant, several complete melodic positions may unfold within the same syllable. Word endings cannot identify such internal boundaries; melodic and modal information becomes central. The comparison therefore examines which findings of §3.6 depend on text–melody articulation and which reflect more general principles of melodic organisation in chant. The corresponding hypotheses are H-S1–H-S5 (§2).

## 5. Byzantine component: reference sources

No available source provides a complete partition of every work into positions comparable with Helsen's database. The two ByzCorpus sources cover different aspects of the problem:

| | Gheorghiță (2009), Sunday Koinonika [9] | *Papadic Formulae*, St Anthony's Monastery [10] |
|---|---|---|
| Content | 42 eighteenth-century *Ainete* Koinonika, 11 formations, 338 inventory rows recording occurrences across 68 tables ([inventory](../corpus/README.md)) | Positions drawn from 758 compositions, with the title and composer of each source file |
| Coverage | All occurrences of each sign within the repertoire, insofar as they are marked by the relevant sign in the older notation | Cataloguer's selection; not exhaustive |
| Distinctive value | 35 occurrences with separate exegeses by Gregory and Chourmouzios in Koinonika by Daniel | Scale: many families and composers |
| Measures supported | RQ1 (recall at formation boundaries), RQ3 (consistency of internal cuts within a formation), comparison of exegeses | RQ3–RQ4 on a larger scale: family recognition and the vocabulary of positions |
| Data not supplied | A complete partition of the work (hence no full-boundary precision); continuous symbolic scores | Location of each occurrence within a complete work; independent boundary criteria; an explicit reuse licence |
| Preparation required | Encoding the 42 works from printed New Method sources and locating the 338 occurrences | Licence review and matching occurrences to complete works |

**Principal historical reference.** Gheorghiță's study is the main Byzantine source for historically and notationally documented formations. It provides a defined repertoire of one genre and catalogues for 11 signs; its parallel exegeses support the comparison in H-S5. In the current [inventory](../corpus/README.md), 35 of 338 rows have been visually checked and the remaining 303 carry the `OCR_DRAFT` flag. Verification and localisation of occurrences within continuous scores form part of checkpoint P3. St Anthony's catalogue is a complementary source for family recognition at a larger scale (RQ4), after matching occurrences to complete works and reviewing rights.

The [expert-boundary agreement pilot](expert-boundary-pilot.md) will produce a complete musicological partition in selected windows, preferably from the same Koinonika. Precision and F1 for complete positions will be calculated there. Gheorghiță's formations will be evaluated separately as historically documented occurrences with identifiable boundaries. This separation follows directly from the Gregorian pilot's finding on the effect of boundary density upon recall.

**Training data.** The 42 Koinonika constitute an evaluation set. NHPYLM training will use a larger body of unannotated papadic compositions from Neanes files, with splitting by work and composer. The training corpus size will be measured in note events and compared with Phase A before training begins.

## 6. Procedure and checkpoints

Each checkpoint must be satisfied before proceeding to the next stage. Its outcome is dated and entered in §9.

| Checkpoint | Criterion | If the criterion is not met |
|---|---|---|
| **P1 — Boundary probabilities** | Forward–backward agrees with exhaustive enumeration on short sequences, with maximum absolute deviation at most $`10^{-9}`$ | Boundary probabilities are not used; H-S3 remains unresolved |
| **P2 — Training corpus** | Size measured in events; split by work and composer documented before training | Training does not begin |
| **P3 — Localisation of Gheorghiță occurrences** | Every occurrence located in the encoded score by its first and last event; a second check covers at least 30% of cases and all ambiguous cases | Unlocated occurrences are reported and excluded |
| **P4 — Mode-specific reference rules** | The cadence rule for each mode (incomplete, complete and final cadences in New Method theory) is recorded and dated before evaluating the model on the test set | H-S3 is not evaluated |
| **P5 — Repeatability** | Two training seeds per fold, both reported without selection | Results are designated preliminary |

Formations with fewer than ten localised occurrences are reported separately and excluded from pooled H-S4 estimates.

**Work stages.**

1. **Boundary probabilities in the Gregorian component (P1).** Instead of Viterbi, exact marginal boundary probabilities $`p_{\mathrm{bnd}}(t\mid X)`$ are computed with forward–backward while holding the trained NHPYLM parameters fixed. For a bigram model over segments, the state consists of two successive boundaries $`(u,t)`$ and the complexity is $`O(T L_{\max}^2)`$. Evaluation uses threshold-independent AUPRC and ROC-AUC as well as an equal boundary budget relative to the cadence rule, with the prediction budget selected exclusively from development data.
2. **A stricter family test.** Matching in §3.2 is extended to final pitch, cadential-figure type and position within the responsory, without reusing occurrences.
3. **Byzantine infrastructure (P2, P3).** Encode the 42 Koinonika and locate 338 occurrences; assemble a training corpus from Neanes; review rights.
4. **Registration of reference rules (P4).** Define and record mode-specific cadential rules on the symbolic event axis before evaluation.
5. **Execution of the Byzantine component (P5).** Apply the measures of §3.2 and the decision rules of §2.
6. **Compositional models (RQ4).** Compare three architectures using the same statistical subsegments:
   - local sequential composition with variable-order memory;
   - composition with global features of long-range span coherence;
   - composition with family-specific parameters.

   The evaluation separately measures boundary F1, family classification at known boundaries, and joint recognition. This stage precedes any integration with architectures A and C_fac in [M1-X](../m1-x-design.md). There, the marginal boundary decision combines family compatibility scores with `logsumexp`, while full joint MAP decoding maximises the score of the complete analysis.

The full ByzCorpus position evaluation distinguishes four levels: (a) position boundary, (b) membership in an analytical family, (c) its particular written or exegetical realisation and (d) correspondence with a historically named type, where attested.

## 7. Next stages of the pilot study

The comparative study combines the completed Gregorian pilot with the design of the Byzantine application. Its next stages are organised around these deliverables:

1. Complete checkpoints P1–P5.
2. Evaluate hypotheses H-S1–H-S4 in Gheorghiță's Koinonika according to §2.
3. Repeat the Gregorian pilot with a second training seed and marginal boundary probabilities.
4. Release code and aggregate results publicly in accordance with source licences.

The comparative evaluation links unsupervised segmentation with independent musicological reference analyses in two chant traditions using shared measures and controls. The comparison of exegeses (H-S5) and the compositional models (work stage 6) are separate extensions of the pilot.

## 8. Reproducibility and rights

- **Implementation:** `lanzv/nhpylm`, commit `f928c78aa74ce44cd60a2f9b7c987167524c4d45`, published hyperparameters, 200 epochs, seed 1 in each fold.
- **Data:** CantusCorpus v0.2, licensed CC BY-NC-SA 4.0 [7]. Helsen's Microsoft Access database is available as a dissertation appendix through the University of Regensburg repository [5]. The planned public reproduction package will contain extraction, alignment and evaluation code, instructions for obtaining Helsen's database from its original source, and aggregate results, in accordance with the applicable data-use terms.
- **Files:**
  - preprocessing, alignment and evaluation scripts, including `extra_checks.py`;
  - the preregistered Phase A protocol;
  - JSON results for the primary analysis, the original code and sensitivity analyses.
- **Byzantine component:** data publication will follow a rights review for each ByzCorpus source.

## 9. Experimental and design timeline

| Date | Work |
|---|---|
| 10 November 2026 | Registration of the Phase A protocol before training; execution of Phases A and B; Phase B departures as described in §3.1 |
| 11 November 2026 | Finalisation of the comparative pilot design: hypotheses H-S1–H-S5, decision rules and checkpoints P1–P5 |

## References

1. Lanz, V., & Hajič, J., Jr. (2025). Gregorian melody, modality, and memory: Segmenting chant with Bayesian nonparametrics. *Proceedings of the 26th International Society for Music Information Retrieval Conference (ISMIR 2025)*, 638–646. DOI: [10.5281/zenodo.17811449](https://doi.org/10.5281/zenodo.17811449).
2. Mochihashi, D., Yamada, T., & Ueda, N. (2009). Bayesian unsupervised word segmentation with nested Pitman–Yor language modeling. *Proceedings of ACL-IJCNLP 2009*, 100–108. [ACL Anthology](https://aclanthology.org/P09-1012/).
3. Mavromatis, P. (2005). A hidden Markov model of melody production in Greek church chant. *Computing in Musicology*, 14, 93–112.
4. Mavromatis, P. (2005). *The Echoi of Modern Greek Church Chant in Written and Oral Transmission: A Computational Model and Its Cognitive Implications*. Doctoral dissertation, Eastman School of Music, University of Rochester.
5. Helsen, K. E. (2008). *The Great Responsories of the Divine Office: Aspects of Structure and Transmission*. Dissertation, Universität Regensburg. DOI: [10.5283/epub.10769](https://doi.org/10.5283/epub.10769).
6. Helsen, K. (2009). The use of melodic formulas in responsories: Constancy and variability in the manuscript tradition. *Plainsong and Medieval Music*, 18(1), 61–76. DOI: [10.1017/S0961137109000965](https://doi.org/10.1017/S0961137109000965).
7. *CantusCorpus v0.2* (Cantus Database export). [Project repository](https://github.com/bacor/cantuscorpus); [release v0.2](https://github.com/bacor/cantuscorpus/releases/tag/v0.2). Data licence: CC BY-NC-SA 4.0.
8. Lanz, V., & Hajič, J., Jr. (2023). Text boundaries do not provide a better segmentation of Gregorian antiphons. *Proceedings of the 10th International Conference on Digital Libraries for Musicology (DLfM 2023)*, 72–76. DOI: [10.1145/3625135.3625143](https://doi.org/10.1145/3625135.3625143).
9. Gheorghiță, N. (2009). *Chinonicul duminical în perioada post-bizantină (1453–1821). Liturgică și muzică*. București: Sophia. Part VII, pp. 126–253.
10. St. Anthony's Greek Orthodox Monastery. (n.d.). *Papadic Formulae*. <https://stanthonysmonastery.org/pages/papadic-formulae>.
