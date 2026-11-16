# A2–S3 · Evidence, status and next steps

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../docs/research/byzcorpus/a2-s3-delimitation/evidence-and-next-steps.md) · **English**
<!-- language-switch:end -->

[Overview](README.md) · [Technical protocol](protocol.md) · [Byzantine protocol](../segmentation-and-family-recognition/07-byzantine-protocol.md)

## Evidence categories

| Study | Recorded finding | Evidence and status |
|---|---|---|
| [NHPYLM–Helsen pilot](../gregorian-nhpylm-helsen-pilot.md) | 148 responsories; boundary recall 0.8994, precision 0.0770, F1 0.1418 | Actual Gregorian chant; completed separate pilot |
| [Supervised Helsen comparison](../segmentation-and-family-recognition/05-gregorian-benchmark.md) | 123 responsories; complete-element F1 0.684 for F with text; LASM−F +0.044 without text and −0.021 with text | Actual Gregorian chant; exploratory, two initialisations |
| A2–S3 synthetic tests | Variant eligibility, exact-length B_L, log-space union, common sample and jackknife | Synthetic and numerical validation; locally verified outputs |
| A2–S3 Byzantine application | Documented cards, reviewed gaps, connective material and estimated knowledge effects | Planned WP0, M3a and subsequent computational evaluation |

The two Gregorian studies have **different samples, protocols and outcomes**. S3 results come from constructed musical settings; the contribution of knowledge in Byzantine chant remains to be measured.

## Synthetic and numerical checks

Local verification established:

- **Eligibility:** 18 targeted tests passed; 17,556 stored variant slots had unchanged endpoints after the eligibility rule was aligned with the protocol.
- **Length control:** one- and two-event endpoint movements with matched articulation. The $B_L$ reference using **exact length per family** separated the synthetic complete-formula setting from the setting in which the card only encoded length. Three-event bins and the particular tested smoothing failed the same decision rule.
- **Numerical stability:** log-space recursion matched exhaustive enumeration to approximately $5.3\cdot10^{-15}$ maximum error; a case with $\log P=-50$ was evaluated accurately in log space.
- **Sample and intervals:** fixed family composition, explicit reasons for withholding intervals and a near-zero standard error check.
- **Additional guards:** the numerator uses accepted extents with the common start; the window contains all accepted extents and candidate variants; the jackknife uses a numerical tolerance. Reanalysis of 20 stored result files and 488 decision comparisons preserved the previous aggregate estimates.

Full scripts, reproducible environment versions and machine-checkable outputs are planned for a **separate technical release**. These numbers document synthetic behaviour and checks of stored outputs.

## WP0 — Musicological card and feasibility screening

Initial families are *parakletike*, *kylisma* and *piasma*, subject to primary-source verification and sufficient eligible occurrences.

1. Specify R/A/E family cards and connect their diagnostic criteria to onset, internal development and cadence.
2. Record accepted boundary pairs, preferred start, gap-level judgements, abstentions, technical masks and connective regions.
3. Build truncations and extensions independently of model predictions, retaining eligibility decisions and reasons.
4. Inventory coverage by family, **exact length** and independent work group; check text-channel features and rare lengths.
5. Finalise common windows and report the proportion of occurrences admitting both variants.

Actual WP0 counts will determine the feasibility of comparative estimation.

## M3a — Independent musicological validation

**M3a uses separate material** to evaluate finalised cards and instructions. Two independent experts may judge family membership and acceptable boundary pairs separately. The assessment includes genuinely accepted longer realisations alongside plausible but rejected extensions into connective material.

The evaluation measures agreement, abstention, card applicability and candidate quality before the principal computational experiments.

## Separate segmentability comparison

NHPYLM cuts act as an **independent comparison variable**. Eligible cut and non-cut locations are compared with control for articulation, textual boundaries, distance from the accepted full endpoint and exact length through $B_L$.

This connects the study of smaller statistical units with the recognition of complete melodic formulas, preserving distinct musicological references for each chant tradition.

## Reproducibility and release policy

This release contains **research documentation**. Code, stored results and tests are scheduled for a subsequent `support/` release after reviewing rights, input data, dependencies, reproduction commands and file integrity. The [core A2](../../a2-knowledge-design.md) documentation remains separate.
