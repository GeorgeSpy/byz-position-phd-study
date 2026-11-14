# 6. Mathematical and computational verification

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/06-mathematical-verification.md) · **English**
<!-- language-switch:end -->

[Overview](README.md) · [Models](01-research-questions-and-models.md) · [Boundary information](03-multiscale-boundary-information.md)

This section verifies numerical agreement between algorithms, exhaustive enumeration and analytically computable values on small examples. Empirical model performance is documented separately in Sections 2–5.

## Two test suites

| Suite | Tests | Scope |
|---|---:|---|
| Semi-Markov models and multigram base | 13 | Partition functions, MAP and marginals by dynamic programming against enumeration; internal C_comp composition; two-level normalisation; degeneration at zero family tilt; LASM identity for a zero-order base; exact multigram calculations |
| Boundary events and family terms | 25 | Exact contextual $`Q_0`$, comparison with local A1, nonadjacent boundaries, uncovered spans, certification, duration-weighted family contributions, numerical stability, fold and capacity checks |

Both suites passed (13/13 and 25/25).

## Main verification results

**Exhaustive enumeration.** For sequence lengths $`T=1,\ldots,8`$, maximum sub-segment length 3 and random bigram matrices, all 255 boundary subsets were evaluated. Dynamic programming and transfer-matrix calculations agree with enumeration to a maximum log-scale error of $`5.3\times10^{-15}`$.

**Predictive table from trained NHPYLM.** `lanzv/nhpylm` (commit `f928c78`) was trained for three epochs on eight artificial strings. Its predictive-probability table for `abababac`, with maximum sub-segment length 3, was extracted. All 128 boundary subsets were checked against 81 internal partitions; maximum log-scale error $`7.1\times10^{-15}`$. The predictive-probability table and its extraction script are scheduled for joint release in the code-reproducibility package.

**Exact $`Q_0`$ versus local A1.** The two methods agree for a single internal boundary. For cuts $`\{2,5\}`$ in the same example, exact $`Q_0=0.0537661756`$ whereas A1 gives 0.0142543692. A1 overestimates in some other boundary sets. Joint events of multiple cuts require history-aware global $`Q_0`$.

**Joint event versus marginals.** In a constructed example of separated cuts, the joint probability (0.4) differs from the product of marginals (0.36). Summed boundary marginals therefore measure a different quantity from $`Q_0`$.

**Mixtures.** For a mixture of base models, $`Q_0`$ is a ratio of mixtures rather than an average of component $`Q_0`$ values (0.18 versus 0.5 in the example).

**Upstream decoding implementation.** The NHPYLM segmentation function combines forward summation and backward maximisation. A constructed counterexample shows that it can miss the globally highest-probability segmentation. On the extracted NHPYLM table, 80 queries showed no discrepancy.

## Certified re-ranking

For $`S(y)=A(y)+\lambda_b\log Q_0(B(y)\mid X)`$ with $`\lambda_b\ge0`$, the bound $`S(y)\le A(y)`$ follows from $`\log Q_0\le0`$. When candidate analyses are generated in descending $`A`$ order, the best rescored candidate is certified globally optimal **only if** its $`S`$ score exceeds the upper bound $`A`$ for the next unexamined analysis, or the legal search space has been exhausted.

An initial implementation defaulted the bound for the next candidate to $`-\infty`$, causing false certification when lists were truncated. The corrected implementation requires an explicit bound and nonnegative weight, and returns an optimality gap whenever certification remains unresolved. Practical evaluations will report the fraction of certified works, mean gap and candidate count.

## Family terms and data checks

The DBC checks ([Section 4](04-family-compositional-learning.md)) confirm: duration-term invariance for constant family scores; a counterexample for variable scores; Jensen's inequality between linear and exponential forms; a common nonlinear term remaining after family centring; and changes in predicted formula count induced by a constant family offset.

Data checks cover: constructing label vocabularies from training folds only, with separate unknown and non-standardised categories; excluding group overlap across training, development, testing and base-model data; rejecting reference units longer than the maximum span; and calculating likelihood numerators when family labels are known for only some units.

## Pending checks

- Training an architecture with NHPYLM as its unsupervised base.
- Rebuilding NHPYLM and extracting the predictive table in a clean environment.
- Measuring certification costs and coverage on real works.
