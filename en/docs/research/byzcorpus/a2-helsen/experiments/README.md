# A2–Helsen — Experimental and Evidence Register

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../docs/research/byzcorpus/a2-helsen/experiments/README.md) · **English**
<!-- language-switch:end -->

[A2–Helsen](../README.md) · [ByzCorpus](../../README.md) · [A2 research design](../../../a2-knowledge-design.md) · [Appendix K](../../../../../docs/appendices/k.md) · [Provenance and rights](provenance-and-rights.md)

## Purpose and research scope

This register documents the executed **exploratory A2–Helsen study**, from the initial corpus inventory to melodic-order and family-diagnostic experiments. Every quantitative entry specifies its condition, evaluation unit, metric, estimand, evidence level, and the identity of the underlying private research source.

The study comprises **136 Gregorian mode-1 responsories**, **134 independent melodic groups**, **1,037 complete annotated melodic elements**, and **19,838 pitch events**. Four target families are evaluated: \`D01x\` (43 occurrences), \`D02x\` (31), \`H01i\` (40), and \`c01\` (25). The main factorial experiment employs three group-disjoint folds and five neural training repetitions.

The [study overview](../README.md) presents the central scientific results. This register provides **experiment-level traceability**, including the sequence of computational corrections and the separation of exploratory from prospective confirmatory evaluation.

## Experimental sequence

| Stage | Main method | Recorded finding |
|---|---|---|
| **A — Corpus** | Sources, labels, melodic groups, and fold coverage | 136 works, 134 groups, 1,037 elements |
| **B — Families** | Source-grounded descriptions and diagnostic relationships | 139 occurrences across four target families; \`V_source\` |
| **C — Factorial comparison** | \`Valid/Perturbed × Flat/Structured\`; ten original \`P\` specifications | Knowledge validity \`Δ_know = +0.0332\` macro AP; 95% CI [+0.0147, +0.0516] |
| **D — Full decoding** | Semi-CRF, ten perturbations, LP tests, rule-violation register | Target-family \`DV−FV = +0.0264\` F1; 95% CI [+0.0083, +0.0444] |
| **E — Matched information** | Same visible prefix for encoder and knowledge features | \`PREFIX/PREFIX\`, learned prefix specification: \`Δ_know = +0.0474\` |
| **F0 — Diagnostic decomposition** | Fixed specifications, head re-fitting, melodic-region experiments | Separate access and specification effects; middle-register ROC-AUC 0.9194 |
| **F1 — Order and gap controls** | Gap-aware masking, capacity matching, OOF recomputation | Four-family order effect \`+0.310322\` macro AP; 95% CI [+0.240601, +0.380043] |

### Three distinct empirical results

**Musicological knowledge validity.** With annotated element boundaries, the main comparison estimates

\`\`\`math
\Delta_{\mathrm{know}}=\tfrac12\big[(DV-DP)+(FV-FP)\big].
\`\`\`

Stage C uses its original set of ten controlled perturbations. Later experiments use additional, separately generated perturbation specifications and therefore retain their own experiment identifiers.

**Structured logical integration.** On annotated boundaries, \`DV−FV\` equals \`+0.0093\` macro AP, with a 95% interval of [−0.0030, +0.0216]. In **full-work semi-CRF decoding**, the target-family exact span-and-family F1 difference is \`+0.0264\`. Overall joint F1 across all families changes from \`0.2282\` to \`0.2290\`.

**Melodic sequence and register.** Stage F1 independently recomputes the four-family sequence-order contrast from stored OOF probabilities (\`+0.310322\` macro AP). On the \`D01x–D02x\` pair the same contrast equals \`+0.007168\`, 95% CI [−0.036120, +0.050455]. The descriptive middle-third mean-register index attains ROC-AUC \`0.9194\`.

## Metric definitions

- **\`macro_ap\`:** macro Average Precision for the four target families on annotated element spans, using all other annotated elements as negatives. Test-fold predictions are pooled per seed, followed by averaging across five seeds. The result generally differs from a mean of fold-level AP values.
- **\`target_joint_f1\`:** exact span and family match for the four target types when decoding complete works.
- **\`overall_joint_f1\`:** joint span-and-family F1 across the full label inventory.
- **\`binary_ap\` / \`roc_auc\`:** distinct pair-specific outcomes for \`D01x–D02x\`.
- **95% intervals:** principal paired contrasts use grouped jackknife-*t* at the independent melodic-group level. Stage F1 also reports direct OOF-based recalculation.

The **134 melodic groups** define group-disjoint splitting and statistical sampling units. They are distinct from the four **target melodic-element families**. Each CSV record defines its outcome and target population to preserve this distinction.

## Computational revisions documented by the register

An early stage-D \`p[:-4]\` comparison restricted the neural encoder to a melodic prefix while knowledge descriptors retained access to the full element. Stage E introduced matched \`PREFIX/PREFIX\` access. Stage F0 separated the effect of information visibility from head re-fitting and the selection of a different prefix-specific specification.

Initial middle-region deletion directly joined pitches across the removed interval. Stage F1 added explicit \`MASK_GAP\` and \`TWO_STREAM\` representations. F1 order controls are parameter matched, while the four-family and \`D01x–D02x\` outcomes remain separately reported.

The source-derived \`V_source\` rules flag **19 violations among 139 genuine target-family elements**: nine \`D02x\`, seven \`D01x\`, and three \`H01i\`. These are **rule-based diagnostics awaiting independent musicological review**. Candidate rule revisions are kept separate from previously reported model results.

## Public machine-readable files

| File | Content |
|---|---|
| [\`experiments.csv\`](../../../../../docs/research/byzcorpus/a2-helsen/experiments/manifests/experiments.csv) | 50 experiment records: condition, outcome, estimate, interval, groups, evidence level and provenance |
| [\`claims.csv\`](../../../../../docs/research/byzcorpus/a2-helsen/experiments/manifests/claims.csv) | 11 scientific statements mapped to individual experiment records |
| [\`sources.csv\`](../../../../../docs/research/byzcorpus/a2-helsen/experiments/manifests/sources.csv) | Seven private source snapshots, content descriptions and SHA-256 identifiers |
| [Provenance, rights and verification](provenance-and-rights.md) | Source restrictions, reproduction procedure and release decisions |

Evidence flags such as \`internal-pooled-oof\`, \`aggregate-checked\`, \`interval-reported\`, \`oof-recomputed\`, \`rule-screen-pending-expert\`, and \`source-inventory\` specify the **available evidence level**. The public release contains aggregate results and provenance metadata.

## Remaining research milestones

The next steps are independent review of the 19 rule exceptions, finalization of the source-grounded family specification, the strong \`B★\` comparator, and a new independent confirmatory corpus \`H\`. At the time of the F1 inventory, **zero locally verified eligible external groups** were available. The principal doctoral A2 study will evaluate the same design on independently annotated Byzantine melodic positions in ByzCorpus.

All stages A–F1 currently constitute **exploratory evidence** from the internally evaluated Gregorian sample.
