# A2–S3 · Training and evaluating the B_L reference model

**Language / Γλώσσα:** [Ελληνικά](bl-training.md) · **English**

[Reference checks](README.en.md) · [A2–S3 protocol](../protocol.md) · [JSON results](bl_verification.json)

## Research role

The `B_L` comparator supplies a strong learned reference for complete-formula delimitation. It receives the same **fixed base segment scores** used by the compared conditions and trains only additional coefficients for **exact length per candidate family**, articulation and textual boundaries, with L2 regularisation.

For a candidate span `s` and candidate family `f`:

```math
\ell_{B_L}(s,f)=b_r(s,f)/T_r+\theta_{f,|s|}
+\beta_{\mathrm{art}}a(s)+\beta_{\mathrm{text}}t(s),
\qquad
\mathcal L=\frac1{|\mathcal G|}\sum_{g\in\mathcal G}
\frac1{|I_g|}\sum_{i\in I_g}
\log P_\theta(A_i\mid W_i,X_i)
-\frac{\lambda_{\mathrm{L2}}}{2}\|\theta\|_2^2.
```

`A_i` is the event that at least one accepted span of the specified family appears in the shared local window. A two-state semi-Markov dynamic program computes its probability and analytic gradient. All candidate families remain in the scoring space, so family identity enters through training supervision and the S3 diagnostic target, rather than as a test-time scoring feature.

Training, selection of `\lambda_{\mathrm{L2}}` and final evaluation use **disjoint groups of works**. Fixed base scores are supplied as numeric inputs; this interface can accept the properly separated, frozen A2 model outputs when available.

## Executable implementation

- [`bl_train.py`](bl_train.py) implements the reference model, event likelihood, analytic gradient, L2 optimisation, grouped development selection and the two S3 endpoint contrasts.
- [`test_bl_train.py`](test_bl_train.py) contains **17 passing tests**, including finite-difference gradient checks, unchanged base scores, trainable articulation and text coefficients, group separation and multiple accepted extents.
- [`bl_verification.json`](bl_verification.json) records the synthetic results, dataset partition, selected regularisation and SHA-256 checksums.

Requires Python 3.10 or later and only the standard library. From the `support/` directory:

```bash
python -m unittest -v test_bl_train.py
python bl_train.py
```

## Controlled synthetic evaluation

A deterministic generator produces **15 independent groups**, three families, and different family-specific preferred exact lengths. Groups split into nine for training, three for development and three for test. Each occurrence offers candidate spans from **every family**. Articulation and text features are set to zero in this primary length-focused scenario; their trainability is exercised in a separate unit test.

| Comparator | Test group-mean log probability | Mean truncation contrast | Mean extension contrast |
|---|---:|---:|---:|
| **Exact family-specific length** | **−1.1946** | **3.8027** | **3.8104** |
| Coarse length bands | −2.2575 | 0.8876 | 0.8952 |
| Without length features | −2.7729 | −0.0027 | 0.0053 |

The exact-length model selected `\lambda_{\mathrm{L2}}=0.01` on development groups. These results demonstrate the implementation's ability to exploit distinct exact lengths by family in a deliberately controlled synthetic setting.

## Connection to the full experiment

Empirical application requires the frozen per-replication A2 base scores, complete legal candidate sets, independently reviewed accepted extents and source-grouped splits. Feature learning and regularisation selection are performed on development groups, followed by paired truncation and extension comparisons on the shared eligible S3 sample.

The earlier counts of 18 tests, 17,556 variant slots and 488 decisions remain in the separate [historical verification register](verification-manifest.json). Replaying those original results requires their original input files, programs and saved outputs.
