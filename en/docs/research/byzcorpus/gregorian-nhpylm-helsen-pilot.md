# Statistical Segmentation and Musicological Boundaries in Gregorian and Byzantine Chant

*ByzCorpus comparative pilot study*

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../docs/research/byzcorpus/gregorian-nhpylm-helsen-pilot.md) · **English**
<!-- language-switch:end -->

[ByzCorpus](README.md) · [Expert-boundary agreement pilot](expert-boundary-pilot.md) · [Byzantine NHPYLM protocol (Greek)](../../../../docs/research/byzcorpus/segmentation-pilot.md) · [Roadmap (Greek)](../../../../docs/research/byzcorpus/roadmap.md) · [M1-X](../m1-x-design.md) · [Gheorghiță inventory](../corpus/README.md)

## 1. Purpose

This pilot study investigates how melodic segments derived from unsupervised statistical segmentation relate to musicological boundaries and to the internal organisation of larger melodic units. Our point of departure is the Nested Hierarchical Pitman–Yor Language Model (NHPYLM) [2], a Bayesian nonparametric model originally designed for word segmentation in unsegmented natural languages, which induces recurrent variable-length melodic segments ("words") directly from continuous symbolic sequences by jointly modelling note transitions within each segment and transitions between consecutive segments. Applying this approach recently to Gregorian chant, Lanz and Hajič (2025) evaluated its performance in terms of memorisation efficiency (*perplexity*) and modal classification [1]. However, when they visually compared the induced segments of a sample chant against Kenneth Levy's classic musicological analysis (Figure 2 in [1]), they observed that the model fragments the melody into much smaller units than those associated with *centonisation*—the compositional practice of constructing melodies by piecing together pre-existing melodic formulae. Prompted by this discrepancy in scale, the authors highlighted the need for comparative studies across other modal traditions possessing documented melodic formulae, including Byzantine chant, while noting the lack of suitably annotated datasets [1]. A parallel question arises within Byzantine musicology itself: although probabilistic models of melodic generation have been proposed for the *echoi* (modes) of Byzantine chant by P. Mavromatis [3, 4], historical and morphological musicological analysis operates on broader, functionally self-contained units such as structural elements, melodic types and complete musical *theseis*.

To bridge this gap in analytical scale systematically, the present work develops and evaluates a **unified comparative framework** that confronts statistical segmentation with musicologically documented boundaries and analytical categories. Through dedicated experimental controls, our methodology isolates the structural information genuinely contributed by the model from the confounding effects of high boundary density on the one hand and surface melodic similarity on the other. The empirical investigation is structured into two complementary components. In the Gregorian component, which has already been completed, the framework is applied to the Great Responsories (*responsoria prolixa*, extensive melismatic chants of the Western Night Office), using as its reference the systematic morphological analysis of musicologist Kate Helsen, who segmented the repertoire into recurring melodic formulae [5, 6]. In the Byzantine component, the same methodology is transferred to papadic Koinonika (Communion chants) in the New Method of analytical notation, drawing its principal historical reference from the comparative study of Nicolae Gheorghiță—who catalogued the occurrences and exegeses of eleven historical signs across eighteenth-century Koinonika [9]—combined with independent expert annotation of complete musical-*thesis* boundaries.

### 1.1 Terminology

- **Statistical segment:** a contiguous subsequence of note events automatically induced by the NHPYLM.
- **Helsen element:** a musicologically delimited melodic unit (formula) of a responsory in Helsen's database [5]. Each element begins immediately after the preceding element's cadential figure [5, p. 57]. It receives a standard label if it occurs at least five times in at least three responsories; otherwise it receives a provisional label.
- **Analytical family:** a category of occurrences sharing structural and modal criteria. In the Gregorian component, standard Helsen labels serve as a proxy; in the Byzantine component, the relevant categories are the analytical families of ByzCorpus, with Gheorghiță's historically and notationally documented formations treated as distinct evidence categories.
- **Complete melodic *thesis* (pl. *theseis*; Greek: θέσις):** the central structural unit studied in ByzCorpus (a recognisable variable-length melodic formation in Byzantine chant). Comparison with a Helsen element concerns the analytical scale of the two traditions and does not presume musicological equivalence between their units.
- **Occurrence / realisation / historically named type:** distinct levels of documentation. Helsen's labels, as well as the classic alphanumeric theme symbols introduced by musicologist W. H. Frere (1894) for the Great Responsories, are modern analytical categories, whereas Gheorghiță's formations bear historical names associated with the *great hypostases* (signs of melodic action in the older Byzantine notation).

## 2. Research questions and hypotheses

- **RQ1 — Boundary alignment.** To what extent do NHPYLM boundaries in held-out works coincide with musicological boundaries, compared with random segmentation preserving both segment count and segment-length distribution?
- **RQ2 — Boundary selection.** How effectively can musicological boundaries be recovered from the dense set of statistical cuts, and how does the model compare with simple rules specified in advance?
- **RQ3 — Internal organisation.** Are internal cuts more consistent among occurrences of the same family than among occurrences of different families matched for surface melodic similarity?
- **RQ4 — Larger-scale units.** Do shared internal coherence and family-specific structural relationships provide additional predictive power for recognising complete melodic units?
- **RQ5 — Cross-tradition comparison.** Which findings from RQ1–RQ4 persist in papadic chant, where multiple consecutive *theseis* can unfold within a single syllable?

The Gregorian pilot provides empirical evidence for RQ1–RQ3 (§3). The following hypotheses are preregistered for the Byzantine component. Each confirmatory hypothesis has three possible outcomes: **supported** when the entire 95% confidence interval (CI) falls on the predicted side of its reference value, **rejected** when it falls entirely on the opposite side, and **unresolved** when it includes the reference value. The bootstrap sampling unit for the Byzantine component is the work, with composer-level sensitivity analysis.

| Hypothesis | Prediction | Measure and reference value |
|---|---|---|
| **H-S1** | A substantially smaller proportion of reference boundaries in Koinonika coincides with word endings than in responsories | Share of reference boundaries at word endings; Gregorian reference 0.9937 |
| **H-S2** | NHPYLM boundaries align with reference boundaries in both traditions | $`\Delta_R`$ versus a length-preserving random reference; reference 0 |
| **H-S3** | Given the same number of predicted boundaries in Koinonika, NHPYLM boundary probabilities outperform an *echos*-specific cadence rule | Paired $`F_1`$ difference in expert-annotated windows with complete boundary annotation; reference 0. Supplementary recall at identified Gheorghiță-formation boundaries |
| **H-S4** | Occurrences of the same historically documented formation—and separately of the same musicologically validated analytical family—exhibit more consistent internal cuts than matched occurrences from another category | Matched $`\Delta J`$ at each category level; reference 0 |
| **H-S5** (exploratory) | The two co-exegeses of the same historical passage (by Gregory and Chourmouzios) yield more consistent segmentation than different passages of the same formation | Paired Jaccard difference across 35 parallel cases; reference 0 |

For H-S1, a "word ending" is defined as the inter-event transition immediately following the last note event of the final syllable of a word. H-S1–H-S4 are confirmatory, whereas H-S5 remains exploratory because the 35 co-exegeses (parallel analytical transcriptions of the same older passage into the New Method) come from eight Koinonika by Daniel Protopsaltes. No direction is predicted for the between-tradition difference in H-S4.

## 3. Gregorian chant pilot: methods and results

### 3.1 Material

**Phase A (CantusCorpus).** From the digital corpus CantusCorpus v0.2 [7], 995 complete responsories from codex Paris, BnF, lat. 12044 (an early twelfth-century antiphoner from the Abbey of Saint-Maur-des-Fossés, which also serves as the manuscript source of Helsen's analysis) were selected. The melodies are encoded in Volpiano (an alphanumeric representation mapping each pitch and notational symbol to a distinct ASCII character). We used the `full_melodies` representation from the code of Lanz and Hajič [1], in which a flat replaces the note symbol it modifies. Textual and notational boundaries (neume, syllable, word and division) were removed from model input and retained solely for evaluation.

Duplicate entries and closely related melodic versions were grouped into 935 melody clusters, defined by identical Cantus IDs or a Jaccard similarity of at least 0.5 between note eight-grams. The two-fold cross-validation split was performed at the cluster level. The NHPYLM was trained for 200 epochs in each fold using the published hyperparameters, a maximum segment length of $`L_{\max}=7`$ and Viterbi decoding. Each work was therefore segmented by a model that had not encountered its melodic cluster during training.

The *repetenda* boundary—marking the concluding portion of the main respond that is repeated as a refrain after the psalmody of the verse—was evaluated in 887 responsories containing a single internal division. In 883 of 900 cases possessing both an internal division and a verse-end text cue, the cue agreed with the text following the division. The Phase A protocol was registered prior to training.

**Phase B (Helsen database).** All 1,668 Mode 1 records from Helsen's relational database [5] were extracted: 214 responsories, comprising 1,056 records with standard labels and 612 with provisional labels. Each responsory was reconstructed from consecutive phrases ordered by the `Position` field. Works were matched to CantusCorpus via their standard CAO (*Corpus Antiphonalium Officii*) catalogue number and textual *incipit*; notably, the database's `Source` field denotes the biblical source of the text rather than the musical manuscript witness. Phase B reuses the out-of-fold segmentations from Phase A.

Comparison between the two transcriptions of the same codex (Helsen and CantusCorpus) yielded 19 exact matches, 129 melodies at normalised edit distance up to 0.05, 51 at distances between 0.05 and 0.15, four above 0.15 and 11 with no match. The **primary analysis** comprises the **148 melodies** at distance at most 0.05, distributed across 146 melody clusters. Sequence alignment projected **954 internal Helsen-element boundaries** onto the Cantus melodies; 28 boundaries were excluded owing to local alignment ambiguity. As a validation check, Helsen's *repetenda* boundary coincided-exactly with the Cantus division in 134 of 137 evaluable instances.

**Departures from the preregistered protocol.** The originally registered Phase B code was executed first. Three technical errors were subsequently identified and corrected:

1. The work-matching key erroneously included the `Source` field (biblical origin).
2. Sequence alignment distinguished upper- and lower-case characters, thereby treating liquescent neumes (semi-vocalised articulations on consonant clusters or diphthongs, which Volpiano encodes using uppercase letters) as pitch mismatches.
3. The *incipit* matching procedure was overly strict with respect to orthographic variants.

Results from the original unamended code are reported separately in the sensitivity analyses (§3.4).

### 3.2 Measures

Let $`E`$ denote the set of reference boundaries and $`B`$ the set of boundaries predicted by the model. We define $`\mathrm{Recall}=|E\cap B|/|E|`$, $`\mathrm{Precision}=|E\cap B|/|B|`$, and $`F_1`$ as their harmonic mean. These definitions are retained unchanged for the Byzantine component: precision and $`F_1`$ for complete *theseis* are computed within jointly annotated windows providing a complete boundary partition, whereas recall of identified boundaries is computed for Gheorghiță's documented formations.

- **Recall against a random reference.** High boundary density increases expected recall even in the absence of informative placement. The principal baseline therefore randomly permutes the exact same statistical-segment lengths within each chant, keeping the number of boundaries per work strictly constant. The primary effect size is the difference $`\Delta_R=R_{\mathrm{NHPYLM}}-R_{\mathrm{random}}`$. The 95% CIs are obtained via 10,000 bootstrap replicates, sampling at the level of melody clusters.
- **Cadence rule.** The comparison with the NHPYLM uses a paired cluster bootstrap with 10,000 replicates across the same 146 clusters. Each replicate pools the two methods' TP, FP and FN counts and recomputes corpus-level micro-$`F_1`$. The rule was specified prior to executing Phase B: it selects word endings whose final pitches are C, D, F or a (encoded as `c`, `d`, `f`, `h` in Volpiano). These represent the primary tonal goals (cadential degrees) of Mode 1 in Helsen's analysis; accordingly, the rule is not independent of the reference, but serves as a strong, musicologically informed comparator.
- **Internal cuts (RQ3).** Jaccard similarity is computed on internal NHPYLM cuts following dynamic melodic alignment. In the unmatched comparison, same-label occurrence pairs from different melody clusters (with alignment distance at most 0.25) are compared against random cuts preserving their count. In the matched comparison, each same-label pair $`(x,x')`$ is paired with an occurrence $`y`$ bearing a different label and belonging to a third melody cluster. The length and number of internal cuts in $`y`$ differ by at most one unit from those of $`x'`$, while its melodic distance to $`x`$ differs by at most 0.05 from $`d(x,x')`$; among qualifying candidates, the closest is selected. An occurrence $`y`$ may be reused across multiple triples. The 95% CI of $`\Delta J`$ is derived from 2,000 bootstrap replicates using the analytical label as the sampling unit.

### 3.3 Results

**Phase A — *repetenda* boundary (887 responsories, 879 clusters).**

| Measure | Estimate | 95% CI |
|---|---:|---:|
| NHPYLM recall | 0.8929 | 0.8725–0.9126 |
| Length-preserving random reference | 0.4997 | 0.4921–0.5075 |
| **Difference $`\Delta_R`$** | **+0.3932** | **0.3711–0.4146** |
| NHPYLM recall at other word endings | 0.7367 | 0.7278–0.7457 |
| Recall with ±1-note tolerance | 0.9876 | 0.9797–0.9944 |

The model places a mean of 64.64 internal boundaries per responsory. Mean segment length is 1.967 notes, and 60.79% of segments consist of a single note. In an exploratory breakdown, boundary probability increases monotonically with the structural salience of the inter-event transition: 0.42 within a neume, 0.44 between neumes of the same syllable, 0.62 at a syllable ending, 0.74 at a word ending and 0.89 at the *repetenda* boundary.

**Phase B — Helsen-element boundaries (148 responsories, 954 boundaries).**

| Measure | Estimate | 95% CI |
|---|---:|---:|
| Exact NHPYLM recall | **0.8994** | 0.8774–0.9206 |
| Length-preserving random reference | 0.5192 | — |
| **Difference $`\Delta_R`$** | **+0.3802** | **0.3528–0.4060** |
| Recall with ±1-note tolerance | 0.9790 | — |
| NHPYLM precision across all transitions | 0.0770 | — |
| NHPYLM $`F_1`$ across all transitions | 0.1418 | — |

The model recovers nearly 90% of Helsen's boundaries, exceeding the random reference by 38 percentage points. It operates at a much finer scale, however, predicting a mean of 75.32 boundaries per chant compared with 6.45 in Helsen's analysis. A Helsen element has a median length of 19 notes, whereas the constraint $`L_{\max}=7`$ enforces its division into at least three segments. In practice, the median element contains eight internal cuts, corresponding to approximately nine statistical segments.

**Boundary selection at word endings.**

| Condition | Boundaries/chant | Recall | Precision | $`F_1`$ |
|---|---:|---:|---:|---:|
| All word endings | 18.89 | 0.9937 | 0.3392 | 0.5057 |
| Word ending + final pitch C, D, F, a | 13.49 | 0.8742 | 0.4176 | **0.5652** |
| NHPYLM restricted to word endings | 14.86 | 0.8941 | 0.3877 | 0.5409 |
| NHPYLM across all transitions | 75.32 | 0.8994 | 0.0770 | 0.1418 |

A total of 99.37% of Helsen's reference boundaries coincide with word endings. Restricting candidate boundary positions to word endings raises NHPYLM $`F_1`$ from 0.1418 to 0.5409. The deterministic cadence rule nonetheless retains an advantage: paired $`F_1`$ difference **+0.0243** (95% CI: 0.0085–0.0401). This finding follows directly from Helsen's analytical definition, whereby each element begins immediately after a cadential figure.

**Internal cuts and analytical labels (exploratory analysis).** In the unmatched comparison (792 pairs, 43 labels), same-label Jaccard similarity is 0.3392 versus 0.1549 for random cuts of equal count ($`\Delta J=+0.1843`$). Because occurrences sharing a label are also melodically similar by definition, a matched comparison was conducted:

| Matched comparison | Value |
|---|---:|
| Ordered same-label pairs | 1,584 |
| Matched triples | **418** (26.4%) |
| Labels represented | 28 |
| Mean same-label Jaccard | 0.2783 |
| Mean different-label Jaccard | 0.2254 |
| **Difference $`\Delta J`$** | **+0.0528** |
| 95% CI (label-level bootstrap) | 0.0359–0.1284 |

Matching on melodic distance accounts for the majority of the unadjusted difference, yet leaves a statistically distinct positive residual associated with the analytical label itself. This finding applies to the 26.4% of pairs for which a valid match was available. Helsen's labels and Frere's historical theme symbols exhibit a Normalised Mutual Information (NMI) of 0.7944 across 196 records in the primary sample (across the entire database, only 13% of records carry a Frere symbol, as Helsen cross-referenced both systems where applicable). The two classifications share underlying analytical assumptions and evaluate elements on the boundaries defined by Helsen.

### 3.4 Sensitivity analyses

| Condition | Responsories | Boundaries | NHPYLM recall | $`\Delta_R`$ |
|---|---:|---:|---:|---:|
| Mode 1, distance at most 0.05 (primary analysis) | 148 | 954 | 0.8994 | +0.3802 |
| Mode 1, distance at most 0.15 | 199 | 1,304 | 0.8980 | +0.3698 |
| Originally registered code (before corrections) | 113 | 709 | 0.8914 | +0.3830 |
| All modes, distance at most 0.05 (exploratory) | 626 | 3,798 | 0.8605 | +0.3733 |

The recall advantage over the random reference remains stable across all conditions. Across all eight modes, NHPYLM restricted to word endings achieves $`F_1=0.5276`$, compared with $`0.4918`$ when selecting all word endings indiscriminately. By contrast, the cadence rule cannot be generalised across modes without specifying mode-specific final pitches in advance.

### 3.5 Scope and limitations

- This evaluation uses the basic unsupervised NHPYLM with a shared segment lexicon. The `NHPYLMClasses` variant of Lanz and Hajič (2025) trains eight separate models using known mode labels and provides a distinct target for future comparison [1].
- One source and one expert: reference boundaries come exclusively from K. Helsen's analysis of codex Paris, BnF, lat. 12044.
- One training initialisation (*seed*) per fold. A second seed has not yet been run, so between-training variation has not been estimated.
- The primary Phase B analysis concerns Mode 1; the extension to all modes is exploratory.
- Boundaries are projected between two independent transcriptions of the same source (Helsen's database and CantusCorpus).
- Boundary evaluation relies on discrete (*hard*) Viterbi decoding; marginal boundary probabilities have not yet been extracted.
- The Jaccard analysis is exploratory and relies on matching with reuse of different-label occurrences.

### 3.6 Main findings of the Gregorian pilot

1. Statistical-segment transitions systematically align with musicological boundaries and substantially outperform a random reference of equal boundary density.
2. The model operates at a micro-scale of approximately two notes, generating a dense set of candidate boundaries that requires ranking and selection to recover musicological elements.
3. In Gregorian responsories, word endings combined with final pitch predict a large share of the musicological segmentation more accurately than the unsupervised model.
4. Analytical labels are associated with a small but positive additional consistency of internal cuts, even after matching for melodic distance, length and cut count.

Two open methodological problems emerge: the **selection** of structurally significant boundaries from dense statistical segmentations, and the **composition of scale**—how a 19-note musicological unit (comprising roughly nine statistical subsegments) arises from local and longer-range relationships.

## 4. Rationale for comparison with Byzantine chant

In Gregorian responsories, analytical boundaries coincide almost universally with word endings, allowing textual articulation to bear the primary burden of boundary discrimination. In Gregorian antiphons (shorter, predominantly syllabic or oligotonic chants), Lanz and Hajič (2023) showed that text boundaries do not yield better segmentation with respect to mode classification [8]; in the present study, however, the target is the analytical boundary of extensive melodic elements, where coincidence with word endings is nearly complete. By contrast, in Byzantine papadic and kalophonic chant, multiple complete *theseis* frequently unfold within a single syllable (extended melismata). There, word endings cannot suffice to select boundaries, and diagnostic weight shifts to melodic, rhythmic and modal information. The comparative study therefore investigates which findings of §3.6 depend on text–melody articulation and which reflect broader principles of melodic organisation in chant. The corresponding hypotheses are formalised as H-S1–H-S5 (§2).

## 5. Byzantine component: reference sources

Unlike Helsen's database, no published source in Byzantine musicology provides an exhaustive partition of complete papadic works into consecutive *theseis*. The two primary reference sources of ByzCorpus address complementary aspects of the problem:

| Feature | Gheorghiță (2009), Sunday Koinonika [9] | *Papadic Formulae*, St Anthony's Monastery [10] |
|---|---|---|
| **Content** | 42 eighteenth-century *Ainete* Koinonika, 11 formations, 338 inventory entries recording occurrences across 68 tables ([inventory](../corpus/README.md)) | *Theseis* drawn from 758 compositions, recording the title and composer of each source file |
| **Coverage** | All occurrences of each sign within the studied repertoire, insofar as they are marked by the corresponding *great hypostasis* in the older notation | Cataloguer's selection; non-exhaustive |
| **Distinctive value** | 35 passages with parallel co-exegeses by Gregory and Chourmouzios in Koinonika by Daniel | Scale: large number of families and composers |
| **What it measures** | RQ1 (recall at formation boundaries), RQ3 (consistency of internal cuts per formation), comparison of co-exegeses | RQ3–RQ4 at scale: family recognition and the lexicon of *theseis* |
| **What it does not supply** | Complete partition of the work (hence no direct computation of full-boundary precision); continuous digital scores | Exact location of each occurrence within a complete work; independent boundary criteria; an explicit reuse licence |
| **Prerequisites** | Encoding the 42 works from printed New Method sources and localising the 338 occurrences | Licence review and matching occurrences to complete works |

**Selection of the principal historical reference.** **Gheorghiță's** study serves as the primary Byzantine source for historically and notationally documented formations. It provides a closed repertoire of a single liturgical genre and systematic catalogues for 11 *great hypostases*/signs, while its parallel co-exegeses enable testing H-S5. In the current [inventory](../corpus/README.md), 35 of the 338 entries have been visually verified, while the remaining 303 carry the `OCR_DRAFT` status. Full verification and localisation of occurrences within continuous scores form part of checkpoint P3. The online *Papadic Formulae* catalogue of **St Anthony's Monastery** is used complementarily to scale up family recognition (RQ4), following alignment with complete works and rights clearance.

The [expert-boundary agreement pilot](expert-boundary-pilot.md) will provide a complete musicological partition within selected windows, preferably drawn from the same Koinonika, enabling the calculation of Precision and $`F_1`$ for complete *theseis*. Gheorghiță's documented formations will be evaluated separately as historically attested occurrences with known boundaries. This methodological distinction directly addresses the Gregorian pilot's central finding regarding the effect of boundary density on recall.

**Training data.** The 42 Koinonika serve exclusively as an evaluation set. The NHPYLM will be trained on a broader corpus of unannotated papadic works encoded in the open-source Byzantine music scorewriter *Neanes*, with strict splitting by work and composer. Training corpus size will be measured in elementary note events and compared against Phase A prior to training.

## 6. Procedure and checkpoints

Each checkpoint must be satisfied before advancing to the next stage. The outcome of each check is dated and logged in §9.

| Checkpoint | Adequacy criterion | Decision if criterion is not met |
|---|---|---|
| **P1 — Boundary probabilities** | The *forward–backward* implementation matches exhaustive enumeration on short sequences, with maximum absolute deviation at most $`10^{-9}`$ | Marginal boundary probabilities are not used; H-S3 remains unresolved |
| **P2 — Training corpus** | Size measured in events; split by work and composer documented prior to training | Training does not commence |
| **P3 — Localisation of Gheorghiță occurrences** | Every occurrence localised in the digital score by its initial and final event; independent second check on at least 30% of the material and all ambiguous cases | Unlocalised occurrences are documented and excluded |
| **P4 — *Echos*-specific reference rules** | The cadence rule for each *echos* (imperfect, perfect and final cadences in New Method theory) is preregistered and dated before running the model on the evaluation set | H-S3 is not evaluated confirmatorily |
| **P5 — Repeatability** | Two training initialisations (*seeds*) per fold, both reported without selective filtering | Results are designated preliminary |

Formations with fewer than 10 localised occurrences are reported separately and excluded from pooled H-S4 estimates.

**Work stages.**

1. **Marginal boundary probabilities in the Gregorian component (P1).** In place of discrete Viterbi decoding, exact marginal boundary probabilities $`p_{\mathrm{bnd}}(t\mid X)`$ are computed via the *forward–backward* dynamic-programming algorithm while holding the trained NHPYLM parameters fixed. For a segment-bigram model, the state is defined by the pair of consecutive boundaries $`(u,t)`$ with computational complexity $`O(T L_{\max}^2)`$. Evaluation is conducted both threshold-independently (AUPRC, ROC-AUC) and at an equal boundary budget against the cadence rule, with the prediction budget selected exclusively on the development set.
2. **Stricter test of family consistency.** The matching procedure of §3.2 is extended to control for final pitch, cadential-figure type and relative position within the responsory, without reusing occurrences.
3. **Byzantine data infrastructure (P2, P3).** Digitally encode the 42 Koinonika and localise the 338 occurrences; assemble the training corpus from *Neanes* files; review usage rights.
4. **Preregistration of rules (P4).** Define and log *echos*-specific cadential rules on the symbolic representation prior to evaluation.
5. **Execution of the Byzantine component (P5)** using the measures of §3.2 and the decision rules of §2.
6. **Compositional models of larger units (RQ4).** Compare three architectures over the same statistical subsegments:
   - local sequential composition with variable-order memory;
   - composition incorporating global span-coherence features;
   - composition with family-specific parameters.

   Evaluation separately measures boundary $`F_1`$, family classification at known boundaries, and joint segmentation and recognition. This stage precedes any integration into the segmental architectures `A` (joint semi-CRF for boundary segmentation and family recognition) and `C_fac` (factorised segmentation semi-CRF without family feedback) of study [M1-X](../m1-x-design.md), where the marginal boundary decision aggregates family compatibilities via `logsumexp`, while full joint MAP estimation maximises the overall analysis score.

Full evaluation of *theseis* in ByzCorpus distinguishes four levels: (a) occurrence boundaries, (b) membership in an analytical family, (c) the specific notational or exegetical realisation, and (d) correspondence with a historically named type, where attested.

## 7. Next stages of the pilot study

This study links the completed Gregorian pilot application with the design of the Byzantine component. Immediate next steps are organised around the following deliverables:

1. completion of checkpoints P1–P5;
2. evaluation of hypotheses H-S1–H-S4 in Gheorghiță's Koinonika according to the prespecified decision rules of §2;
3. replication of the Gregorian pilot with a second training initialisation (*seed*) and extraction of marginal boundary probabilities;
4. public release of code and aggregate results in accordance with source licensing terms.

This comparative evaluation bridges unsupervised statistical segmentation with independent musicological reference analyses across two related modal chant traditions, applying shared metrics and rigorous methodological controls. The comparison of co-exegeses (H-S5) and the hierarchical compositional models (stage 6) constitute distinct extensions of the pilot study.

## 8. Reproducibility and rights

- **Implementation:** `lanzv/nhpylm`, commit `f928c78aa74ce44cd60a2f9b7c987167524c4d45`, published hyperparameters, 200 epochs, initialisation `seed = 1` in each fold.
- **Data:** CantusCorpus v0.2, under a CC BY-NC-SA 4.0 licence [7]. Helsen's database (in Microsoft Access format) is available as a doctoral dissertation appendix through the University of Regensburg repository [5]. The planned public reproducibility package will include extraction, alignment and evaluation scripts, detailed instructions for retrieving Helsen's database from its primary source, and aggregate results, in full compliance with data-distribution terms.
- **Evaluation files:**
  - preprocessing, alignment and diagnostic scripts (including `extra_checks.py`);
  - the preregistered Phase A protocol;
  - JSON result files for the primary analysis, the originally registered code and sensitivity analyses.
- **Byzantine component:** data publication will follow rights clearance for each constituent source of ByzCorpus.

## 9. Experimental and design timeline

| Date | Work |
|---|---|
| 10 November 2026 | Registration of the Phase A protocol prior to training; execution of Phases A and B; documentation and correction of Phase B departures (§3.1) |
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
