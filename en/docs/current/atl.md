# ATL: learning historical transformations

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/current/atl.md) · **English** · [Translation progress](../translation-status.md)
<!-- language-switch:end -->

[Methodological map](index.md) · [Inverse recovery](inverse-problem.md) · [Musicology of exegesis (Greek)](../../../docs/musicology/06-old-notation.md)

ATL (Attested Transformation Learning) develops a **probabilistic model of the morphology of exegesis**: it learns how one written realisation is expanded, contracted or modified into another. Parallel exegeses of the same historical passage provide pairs with known provenance, while internal alignment and transformations are estimated by the model.

The contribution is knowledge of **where and how the same chant changes between exegeses**. The model will identify which internal regions expand or contract, which relations persist, and which practices vary by exegete and context. Prediction on new families tests the reach of these regularities. [Musicological question and computational contribution](../review/knowledge-contributions.md).

## The observed object

Let $X_G=(g_1,\ldots,g_m)$ and $X_C=(c_1,\ldots,c_n)$ be two analytical notations of a demonstrably shared passage, $F$ its formula family and $Z$ its modal, prosodic and historical context. The identity of the passage is established through the relationship between sources. An alignment $A$ links subsequences that may differ in length, such as $g_{i:j}\leftrightarrow c_{k:\ell}$, allowing expansion, contraction and substitution.

A general probabilistic formulation for the analytical description of ATL is:

$$q_\theta(X_C\vert X_G,F,Z) =\sum_{A\in\mathcal A(X_G,X_C)} q_\theta(A,X_C\vert X_G,F,Z).$$

Summing over admissible alignments avoids arbitrarily choosing a single correspondence. Permitted transitions are constrained by formula encoding and alignment rules recorded before final testing. Training can maximise the log-likelihood of historical pairs, while interpretation returns to actual passages and individual aligned regions. The specific factorisation, constraints and parameter estimation belong to the technical protocol to be developed; the equation defines the research object.

| Comparison model | What it isolates |
|---|---|
| Specified rules of exegesis | Predictability from already documented theoretical knowledge. |
| Simple sequence alignment/distance | Formal resemblance without learning specifically from historical pairs. |
| Variable-length probabilistic transducer | Distributions of expansion, contraction and substitution in relation to $F,Z$. |
| Held-out families | Predictive transfer of learned transformations. |

The analysis retains successful and unresolved alignments together. ATL thereby offers a measurable morphology of exegesis: which internal zones expand, which relations persist, and where differences between exegetes accumulate. Profiles concern the observed written exegeses and connect to musicological analysis of the corresponding sources.

## Relation to B2–EISE, ATL-INV and the operator

The controlled M2 study uses the **existence** of an attested pair as a source of positive relations for the EISE encoder. ATL uses the **internal content** of both exegeses and models their transformation. Shared sources support complementary tasks, each with a defined output and independent criterion.

[ATL-INV](inverse-problem.md) turns to an older, independently read witness: it attempts to recover the old written label $H$ from an analytical exegesis. Bayesian inversion uses the dedicated historical channel $H\rightarrow X_G$, with an independent reading of the old label. ATL's $X_G\rightarrow X_C$ transducer estimates the relation between two analytical exegeses. [ $M_{\mathrm{θέσις}}$ ](m-thesis.md) studies more generally the distribution of a realisation $X$ given family $F$ and context $C$. The three formulations share alignment and context tools; their predictions are evaluated separately.

**Scientific contribution:** an interpretable, historically supervised model of variation that moves from descriptions of individual cases to tests of transfer to unseen families. The [historical transformation source (Greek)](../../../sources/proposal-v878-candidate.tex#L764) defines ATL's current programmatic role; the [analytical reader section (Greek)](../../../docs/full/06-eise.md#r049) is an earlier technical starting point.
