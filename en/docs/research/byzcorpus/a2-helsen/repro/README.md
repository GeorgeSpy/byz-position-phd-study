# A2–Helsen — Executable Musicological-Knowledge Core

[A2–Helsen study](../README.md) · [A–F1 experiment register](../experiments/README.md) · [A2 technical protocol](../../../../../../docs/appendices/k.md) · [Existing A2 statistical simulations](../../../../../../docs/research/a2/support/README.en.md) · [Ελληνικά](../../../../../../docs/research/byzcorpus/a2-helsen/repro/README.md)

This directory provides executable numerical operators for musical-family specifications, constrained perturbations, linear-programming certificates and core A2 estimators. Inputs are symbolic cue matrices with externally specified families. The accompanying tests and example use entirely synthetic values.

## Installation and execution

Python 3.10 or later is required. From this directory:

~~~bash
python -m venv .venv
# Activate the environment using the command for your operating system.
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m examples.synthetic_example
~~~

NumPy and SciPy are the required numerical dependencies. scikit-learn is optional: one test cross-checks tied-score average precision against its reference implementation, and is skipped when scikit-learn is unavailable.

The local test run completed **14 tests successfully**. The example evaluates two invented family specifications over 16 binary cue states and obtains certified $d_F=d_D=0.4$.

## Files

| File | Purpose |
|---|---|
| [a2_core.py](../../../../../../docs/research/byzcorpus/a2-helsen/repro/a2_core.py) | Three-valued R/A/E logic, $Q$, logical penalties, flat/structured scores, LP certificates, perturbations and estimators |
| [tests/test_core.py](../../../../../../docs/research/byzcorpus/a2-helsen/repro/tests/test_core.py) | Deterministic numerical and logical checks |
| [examples/synthetic_example.py](../../../../../../docs/research/byzcorpus/a2-helsen/repro/examples/synthetic_example.py) | Executable demonstration with invented observations |
| [requirements.txt](../../../../../../docs/research/byzcorpus/a2-helsen/repro/requirements.txt) | Minimal numerical dependencies |

## Knowledge representation

Each family is represented by three roles: **R**, a conjunction of required cues; **A**, a conjunction of disjunctive alternative groups; and **E**, excluded cues negated before conjunction.

The function `evaluate(values, observed, concepts, spec)` accepts two matching `(N, C)` arrays, one with binary observations and the other with observability indicators. A masked cue is unknown. Outputs include `Q_R,Q_A,Q_E`, a strong-Kleene truth state `1/0/-1` and a penalty activated only by an observed logical violation.

Flat and structured scoring follow $\ell_F=b+Qw$ and $\ell_D=b+Qw-\lambda v$, with $\sum_j w_j=1$, $w_j\in[0.1,0.8]$ and $\lambda\in[0,2]$.

The core handles knowledge contributions for the supplied family columns. Full-class score alignment, neural training, temperature calibration and work-level decoding remain part of the larger empirical training pipeline.

## Perturbations and certificates

The `propose_perturbations` function builds a globally injective mapping of cues within compatible descriptor classes, balancing prevalence and observability on **unlabeled development states**. Each accepted proposal changes every family's canonical specification, has observed satisfying and violating witnesses, is functionally distinct and passes both $d_F$ and $d_D$ LP certificates.

HiGHS provides the solutions. The certificate records primal residuals, dual-stationarity residuals, duality gap and a conservative dual lower bound. Its scope is the declared state set and parameter domain. Independent musicological review determines whether a proposed mapping changes the intended musical meaning.

## Estimators

`ap_with_ties` computes uninterpolated average precision with simultaneous insertion of tied scores. `macro_ap` evaluates one family against all other annotated elements. `pooled_seed_ap` computes AP from pooled fold predictions **separately for each seed**, then averages over the seeds.

`factorial_contrasts` reports knowledge validity, the valid-specification logical contrast, the mean structural effect and their interaction. `jackknife_t` recomputes the complete estimator with one independent melodic group left out each time.

## Research context and data access

The empirical study uses Helsen/CantusCorpus data, trained neural models and individual out-of-fold predictions retained in a private research archive. These files are managed according to the [provenance and rights documentation](../experiments/provenance-and-rights.md).

This public subpackage supplies an **executable reference for the numerical operators and their tests**. Replicating the empirical study additionally requires authorized source materials, training code and the original experimental configuration. The established [A2 synthetic simulation suite](../../../../../../docs/research/a2/support/README.en.md) remains the reference for design calibration and operating characteristics.

**Code license:** [MIT](../../../../../../LICENSE-CODE), as specified in the [repository licensing policy](../../../../../../LICENSING.md).
