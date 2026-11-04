# A2 — Synthetic design checks

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](README.md) · **English**
<!-- language-switch:end -->

[A2 research design](../../../../en/docs/research/a2-knowledge-design.md) · [Appendix K — A2 technical protocol](../../../../en/docs/appendices/k.md)

This folder contains the synthetic checks behind this revision's decisions on the statistical procedure, the composition of H, the perturbation generator and head fitting. The data are **synthetic**, with arbitrary noise, prevalence and clustering parameters. The checks show mechanisms and orders of magnitude. They do not estimate performance on the real corpus and do not replace the operating-characteristics study of §K.8, which runs in WP0 with the pilot's sizes and at least 5000 replications per critical scenario.

## Files

| File | Content |
|---|---|
| `a2_ap.py` | Shared synthetic data generator, $`\mathrm{AP}_{\mathrm{fam}}`$ with simultaneous insertion of ties and the two primary estimands. The `symmetrize_fd` option swaps the F and D slots per group, so that null $`H_2`$ holds exactly. `streams` gives independent random streams for the reference and for every dataset. `allocate_h` applies the family-coverage rule for H. |
| `test_ap.py` | Weighted AP with ties matches scikit-learn on duplicated data (200 trials × 3 families). |
| `test_generator.py` | Regression tests of the generator's acceptance rules: a swap inside an alternative group, canonical duplicates, $`\phi=?`$ as a non-witness, rejection of an LP with a large residual, acceptance of a genuine change. |
| `oc_jackknife_t.py`, `run_oc.sh` | Operating characteristics of the primary candidate procedure: jackknife-t with a $`t(G-1)`$ reference and Holm at 0.025, issuance rule, separate denominators and, with `--allocate-h`, allocation of groups to H with family coverage. |
| `oc_bootstrap_t.py` | Sensitivity: per-dataset bootstrap-t with inner jackknife and the strict rule on undefined resamples (small study, $`B=199`$). |
| `generator_feasibility.py` | Perturbation generator: constrained sampler, change of every family's canonical card, canonical and functional uniqueness, a $`\phi=1`$ witness, activation, LP certificates with checked residuals and a conservative dual bound, termination reason. |
| `heads_allocation.py` | Where to fit the heads $`(w,\lambda)`$: on the base's groups, on the internal development set, or by grouped cross-fitting, recording each fold's groups and convergence. |
| `summarize.py` | Produces `results/summary.md`. |
| `run_all.sh` | Full reproduction (about 35–40 minutes on one core). |
| `results/*.jsonl` | One line per scenario or bank, with seed, configuration, software versions and the individual reference values. `oc_jackknife_t.jsonl` also holds the estimates and standard errors of every dataset, at full numerical precision, so that every decision can be reconstructed exactly (§7 of the summary). The intermediate `oc_jackknife_t_a.jsonl` and `_b.jsonl` are created during the run. |
| `results/earlier_batches/` | The two earlier runs, in which the reference and the datasets shared one random stream. Kept for the record and not used in the current results. The subfolder [`pr50-2026-11-03`](results/earlier_batches/pr50-2026-11-03/README.md) also keeps, byte-identical, the first feasibility batch of 3 November. |

## Main results

Full tables: [`results/summary.md`](results/summary.md) (Greek headings).

**Primary candidate procedure.** Nulls are exact by construction: $`H_1`$ through equal V and P laws, $`H_2`$ through a per-group F/D swap. Non-null reference values use $`G=400`$ and 20 replications, on a stream independent of the datasets. FWER and power count all planned datasets, with non-issued ones as non-rejections.

| Scenario | $`G`$ | Bases | Planned / issued | FWER [95% MC] | Power $`H_1`$ / $`H_2`$ | 95% coverage |
|---|---|---|---|---|---|---|
| both nulls | 6 | 1 | 1000 / 980 | 0.019 [0.011, 0.030] | — | 0.957 / 0.976 |
| both nulls | 12 | 1 | 2000 / 2000 | 0.017 [0.012, 0.024] | — | 0.968 / 0.967 |
| both nulls | 20 | 1 | 3000 / 3000 | 0.017 [0.013, 0.022] | — | 0.960 / 0.965 |
| both nulls | 30 | 1 | 1000 / 1000 | 0.018 [0.011, 0.028] | — | 0.959 / 0.967 |
| only $`H_2`$ true | 8 | 1 | 2000 / 1995 | 0.008 [0.005, 0.013] | 0.48 / — | 0.957 / 0.976 |
| only $`H_2`$ true | 12 | 1 | 2000 / 2000 | 0.017 [0.012, 0.024] | 0.79 / — | 0.956 / 0.970 |
| only $`H_2`$ true | 12 | 5 | 1000 / 1000 | 0.017 [0.010, 0.027] | 0.89 / — | 0.960 / 0.962 |
| only $`H_2`$ true, sparse presence, ties | 8 | 1 | 1000 / 498 | 0.000 [0.000, 0.004] | 0.11 / — | 0.974 / 0.994 |
| only $`H_1`$ true | 12 | 1 | 2000 / 2000 | 0.022 [0.016, 0.029] | — / 0.994 | 0.959 / 0.960 |
| only $`H_1`$ true | 20 | 1 | 2000 / 2000 | 0.026 [0.019, 0.033] | — / 1.000 | 0.953 / 0.956 |
| no null ($`\Delta_{\mathrm{know}}\approx0.05`$, $`\Delta_{\mathrm{logic}}\approx0.027`$) | 8 / 12 / 20 | 1 | 1000 per $`G`$ | — | 0.20 / 0.17 · 0.32 / 0.38 · 0.65 / 0.74 | 0.958–0.970 |

With stronger clustering ($`\alpha=10`$, $`G=12`$) power in the no-null scenario was 0.39 / 0.43.

**Allocation of groups to H with family coverage.** Each dataset generates a pool of $`2.5\thinspace G`$ groups. The algorithm covers the rarest families first, so that every family is in at least $`m_H`$ groups of H, and fills the rest at random. The remaining groups form development, whose coverage is recorded.

| Scenario | $`G`$ | $`m_H`$ | Planned / allocated / issued | FWER [95% MC] | Power $`H_1`$ / $`H_2`$ | 95% coverage (nulls) | Development with a family in <2 groups |
|---|---|---|---|---|---|---|---|
| both nulls | 12 | 3 | 2000 / 2000 / 2000 | 0.017 [0.012, 0.024] | — | 0.955 / 0.969 | 0% |
| only $`H_2`$ true | 12 | 3 | 2000 / 2000 / 2000 | 0.014 [0.009, 0.020] | 0.80 / — | — / 0.971 | 0% |
| only $`H_2`$ true, sparse presence, ties | 8 | 2 | 1000 / 992 / 992 | 0.009 [0.004, 0.017] | 0.27 / — | — / 0.977 | 37% |
| only $`H_1`$ true | 20 | 3 | 2000 / 2000 / 2000 | 0.023 [0.017, 0.031] | — / 1.000 | 0.961 / — | 0% |

In the sparse scenario the coverage rule raises the issued datasets from 498 to 992 of 1000, but with $`m_H=2`$ it often leaves development without enough coverage. $`m_H`$ and the minimum coverage of development are therefore set jointly in the pilot.

**Earlier batches.** In the first two runs of the five-base scenario ($`G=12`$, seed 108, 500 datasets) the reference and the datasets came from the same generator. Changing the reference replications from 5 to 20 therefore also changed the datasets. The first batch gave an FWER of 0.028 [0.015, 0.047] and coverage of 0.926 / 0.944, the second 0.018 [0.008, 0.034] and 0.960 / 0.968. In the current run, with independent streams, the same 1000 datasets gave $`\Delta_{\mathrm{know}}`$ coverage of 0.960 with 20 and 0.957 with 5 reference replications, and an FWER of 0.017 in both. The number of reference replications explains a small part of the difference between the two old batches; those batches are different Monte Carlo samples.

**Sensitivity: per-dataset bootstrap-t** ($`G=12`$, $`B=199`$, 150 datasets per scenario). The strict rule suspended 13% of datasets in the all-null scenario and 10% in the scenario where only $`H_2`$ is true. In the all-null scenario the FWER was 0.040 [0.015, 0.085] and coverage 0.939 / 0.893. In the second scenario coverage was 0.926 / 0.933 and power for $`H_1`$ 0.58, against 0.79 for the jackknife-t. With 9999 resamples suspension increases. With about 130 issued datasets, the Monte Carlo error of coverage is about 0.02.

**Generator.** With uniform choice among the compatible images, ten accepted P were found in 10 of the 11 banks without an immovable family (16–191 proposals). The bank that failed exhausted the 100,000 proposals with nine accepted P. The 5 banks with an immovable family were declared infeasible at once. A family is immovable when none of its literals has a compatible alternative image. The most frequent rejection causes were an unchanged canonical card of some family and, in the bank that failed, canonically duplicate proposals. LP residuals and duality gaps were below $`10^{-14}`$ and the smallest conservative dual bound was 0.1. A preference for non-identity images did not help: 8 of 11 banks, with many duplicate proposals and two stops at the time limit in the poor banks.

**Heads.** Fitting on the base's groups underestimates $`\lambda`$, with a median of 1.27–1.36 against 1.70–1.71 on the internal development set. On the internal development set the standard deviation of $`\hat{\lambda}`$ was 0.30, $`\hat{\lambda}`$ reached the upper bound 2 in 12–13% of fits and no estimate was below 0.1. $`\Delta_{\mathrm{logic}}`$ on H was 0.041–0.045 with heads on the base's groups and 0.043–0.048 on the internal development set. Grouped cross-fitting with a consistent temperature gives a similar $`\hat{\lambda}`$ (1.64–1.69) at five times the base training cost. It is a separate sensitivity, because at prediction it combines five models. All bases converged.

## Corrections

### After the second independent check

A second independent check found the following, which are corrected here:

1. **Random streams.** The same generator produced first the reference and then the datasets. Attributing the difference 0.926 against 0.960 only to reference noise was wrong. The reference and every dataset now have independent streams from a common seed, and the individual reference values are stored. The two earlier runs are kept as separate batches.
2. **Composition of H.** The simulation generated $`G`$ random groups directly. It now also runs the prespecified allocation algorithm with family coverage and records allocation failures, prevalences and the coverage of development.
3. **Change per family.** Change was checked on the whole bank; a swap inside an alternative group could leave a family unchanged. A change of every family's canonical card is now required, with a regression test.
4. **LP acceptance.** Acceptance checked only a positive value. It now requires successful termination, residuals and gap up to $`10^{-8}`$ and a conservative dual bound above $`10^{-6}`$, with a fault-injection test.
5. **Termination.** Target reached, proposals exhausted, time limit and infeasibility from an immovable family are recorded separately.
6. **Heads.** The groups of each cross-fitting fold and the convergence of the bases are recorded. The independent check found a deviation of up to about 0.0021 in the cross-fitted $`\Delta_{\mathrm{logic}}`$ with another scikit-learn version; the recorded groups now allow a side-by-side comparison.
7. **Use of the penalty.** The standard deviation of $`\hat{\lambda}`$ and the share $`\hat{\lambda}\lt 0.1`$ are reported.
8. **Storage precision.** Estimates and standard errors were stored with six decimals. Near the Holm threshold, rounding moved a reconstructed $`p`$ from 0.0249972 to 0.0250009 and changed the decision; in the scenario where only $`H_2`$ is true ($`G=12`$) the 34 false rejections were reconstructed as 33. Values are now stored without rounding and the summary verifies every decision.

### After the first independent check

The first independent check of the synthetic studies found the following, which were corrected:

1. Null $`H_2`$ was set to zero while the true value was about $`-0.0025`$. It is now constructed exactly by a per-group F/D swap.
2. Datasets with an undefined resample were dropped from the denominators. Planned, defined and issued datasets are now reported separately.
3. The comparison with $`B=199`$ and one base is presented explicitly as a small sensitivity study.
4. A check for finite, positive standard errors was added.
5. The generator checked uniqueness on the permutation key. The canonical form and the $`(Q,v)`$ function are now checked.
6. The satisfiability check did not distinguish $`\phi=1`$ from $`\phi=?`$. A witness with $`\phi=1`$ is now required.
7. LP residuals and duality gaps are recorded.
8. In head fitting, all splits are by group, the temperature is consistent and an undefined AP counts as undefined.
9. Every result line records seed, configuration and software versions.

The qualitative conclusions of the earlier runs stand: lower coverage and power of the per-dataset bootstrap-t with few groups, the need for a constrained sampler and underestimation of $`\lambda`$ when heads are fitted on the base's groups. The numerical results in this folder replace the earlier ones.

## Reproduction

```bash
cd docs/research/a2/support
./run_all.sh          # or separately: python3 test_generator.py, ./run_oc.sh a, ./run_oc.sh b, ...
```

`run_all.sh` runs both tests, all scenarios and `summarize.py`. Parts `a` and `b` of `run_oc.sh` can run in parallel. Run with Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1 and scikit-learn 1.9.1. Exact versions are recorded in the `env` field of every result line.
