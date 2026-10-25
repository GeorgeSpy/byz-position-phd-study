# Exploratory and Comparative Research Protocol

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../docs/research/ecsi/03-methods-and-gates.md) · **English**
<!-- language-switch:end -->

[Back to the ECSI overview](README.md)

## P0′ — Source inventory before model training

Signature cards must first be completed from real sources and independently assessed by experts. The seven measurements are:

- **μ1:** independent source/provenance groups, permissions, and dependency closure;
- **μ2:** discrete, ordinal, and continuous diagnostics, with particular attention to continuous core variables;
- **μ3:** admissible and undesirable concept mappings, including non-injective maps; exhaustive enumeration is limited to small finite spaces;
- **μ4:** verified correspondence of specific historical passages;
- **μ5:** blind expert discrimination of difficult negative instances;
- **μ6:** separate assessment of concept identifiability, joint model–assessor identifiability, and precision in variance-component estimation;
- **μ7:** reliability of a fixed signature when applied to new occurrences by independent experts.

Neither the number of families nor a sample size or effect size is treated as empirically established before this inventory. Publishing an individual signature requires precise source identification, a documented evidence trail, and retained disagreements.

## P1′ — Two compiler dossiers

**C_contextual_family:** a context-dependent family rule, its exact compilation into a membership event, comparison with exhaustive enumeration, and independent expert review.

**L_verified_locus:** a specific earlier passage and its exegeses, with independently verified local correspondence. Passage correspondence does **not** automatically create a positive family-membership label. The C dossier can proceed even if L is unavailable.

## P2′ — Matched 2×2 experiment

| Knowledge condition | Structured mechanism | Flat mechanism |
|---|---|---|
| Valid signature | ECSI-D-V | Flat-V |
| Controlled perturbed signature | ECSI-D-P | Flat-P |

All conditions share R★, encoder, observable musical concepts and contexts, occurrence boundaries, the `v` branch, independent data partitions, and training/tuning budgets. Flat conditions receive the **actual valid or perturbed signature content**, but without its enforced logical composition. The strong **B★** comparator uses supervised contrastive learning (SupCon), family prototypes, matched concept supervision, and the same `v` branch.

**Primary identification endpoint:** group-balanced **MacroAP_hard** evaluated over independent provenance groups.

**Compulsory complementary gate:** `Q_real`, preservation of realisation information, assessed both against an absolute threshold and by non-inferiority within a preregistered **intersection–union test (IUT)** framework. Results with gold/expert and predicted boundaries are reported separately. Superiority, non-inferiority and equivalence margins, together with power calculations, are set using development data after P0′—**before the protected final test sets are examined**. A failure to establish superiority does not itself establish equivalence; that requires a separate, preregistered equivalence test.

**GO:** valid new musicological application, no leakage, reliable compiler and calibration checks.

**AMBER:** limited coverage or unresolved ambiguity; narrow the claim and obtain additional independent evidence.

**STOP:** invalid signature, unauditable provenance, an unassessable target, or leakage of the true family label.
