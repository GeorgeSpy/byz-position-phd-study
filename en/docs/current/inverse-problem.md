# ATL-INV: the inverse problem of exegesis

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/current/inverse-problem.md) · **English** · [Translation progress](../translation-status.md)
<!-- language-switch:end -->

[Methodological map](index.md) · [Forward ATL](atl.md) · [Musicological evidence (Greek)](../../../docs/musicology/06-old-notation.md)

The historical direction of exegesis runs from an older written source to an analytical rendering in the New Method. ATL-INV asks the inverse, computationally testable question: **given the exegesis, how well can we recover the particular old notational choice recorded in an independent witness?** The result maps which written distinctions remain predictively accessible beyond metrophonia and beyond already known rules of exegesis.

**The new musicological knowledge** concerns which old notational distinctions are associated with systematic analytical renderings, by which exegetes and in which contexts. Comparison with rules establishes what the particular comparator accounts for and what the actual exegesis adds. The methodology connects this historical question to calibrated prediction from specific, potentially dependent sources. [Research benefit for musicology and machine learning](../review/knowledge-contributions.md).

## The source of ambiguity

Metrophonia describes the course of quantitative movements, but can give different written choices the same intervallic reading. As an introductory example, oligon and petaste can indicate the same ascent; non-intervallic great hypostases do not alter the metrophonic path. The historical test prioritises distinctions that do not reappear unchanged as signs of the New Method, so recovery uses analytical development rather than an obvious copied symbol.

| Symbol | Observation | Role in prediction |
|---|---|---|
| $`H`$ | Old label read in a **specific** witness. Whether it is a sign, relation between signs or complex is declared in advance. | Recovery target; independent historical reference. |
| $`M`$ | Metrophonic equivalence class. | Restricts historically eligible labels with a shared reading. |
| $`Z`$ | Admissible historical, modal and local context. | Controls already predictable differences. |
| $`X_G,X_C`$ | Analytical exegeses of the same verified passage, for example by Gregorios and Chourmouzios. | First and second evidence for recovery. |
| $`\mathcal H(M,Z)`$ | Predefined candidate set of old labels. | Domain of normalisation and evaluation. |

The <code>old_witness_reading</code> relation connects $`H`$ to the witness actually read. The <code>actual_exemplar_of_exegete</code> relation—whether the exegete used precisely that witness—is recorded separately and may remain unknown. This distinction supports the historical interpretation of the result.

### The colour of the cheironomic sign by evidence level

Gheorghiță (2009, pp. 250–251) counts the red or black colour of the cheironomic sign in the older codices among the factors of variation; according to Apostolos Konstas, it indicates a simple or compound, shorter or longer development of the thesis. Because the New Method does not carry the old sign or its colour, colour is **not used** as an input feature in studies fed only by New Method material (M1, M2a, M5-min); its possible effect is examined only as a hypothesis on temporal expansion $`Q_x`$ and internal distribution $`p_x`$. When a passage is linked to a specific older witness, colour is recorded at the **source level**, and only where the reading is certain. It can then be tested whether colour predicts the extent of the exegesis in the forward channel and, conversely, whether the simple or compound function of the great hypostasis can be recovered probabilistically from the analytical notation.

## Probabilistic formulation

A forward historical channel $`q_\phi(X_G\mid H,M,Z)`$ and prior $`p(H\mid M,Z)`$ determine the inverse distribution:

```math
p_\phi(h\mid x_G,m,z)=
\frac{q_\phi(x_G\mid h,m,z)\,p(h\mid m,z)}
{\sum_{h'\in\mathcal H(m,z)}
q_\phi(x_G\mid h',m,z)\,p(h'\mid m,z)}.
```

The denominator sums over all eligible historical choices in the same metrophonic class. Uncertainty is represented as a distribution, allowing calibration and justified abstention. Direct discriminative prediction $`p_\psi(H\mid M,Z,X_G)`$ can serve as a separate baseline on the same data. The channel is estimated from development material and final recovery is tested on held-out works and groups of related sources.

Adding a second exegesis requires a model of **dependence** between the two exegetes. One candidate directed factorisation in the technical plan is:

```math
q_\lambda(x_G,x_C\mid h,z)
=q_G(x_G\mid h,z)
\left[(1-\lambda)q_C(x_C\mid h,z)
+\lambda r(x_C\mid x_G,z)\right],\quad 0\leq\lambda\leq1.
```

With normalised $`q_G,q_C,r`$, the first marginal is $`q_G`$. $`\lambda`$ describes statistical dependence in the model; reversing the direction provides a sensitivity check. If only $`X_C`$ is available, its probability follows through proper marginalisation over $`X_G`$ or a dedicated single-channel model. This mathematical development belongs to the [revision specification](../reference.md#what-each-version-covers) and requires numerical verification at R2.

## Three predictive differences

For an independent set $`D`$ and estimator $`q`$, define:

```math
\widehat{\mathrm{CE}}_D(H\mid V;q)
=-\frac{1}{|D|}\sum_{i\in D}\log_2 q(h_i\mid v_i).
```

Logarithms have base 2 and the unit is bits per historical label. Comparisons concern predictions of **the same** target $`H`$:

```math
\begin{aligned}
\Delta_{\mathrm{rec}}
&=\mathrm{CE}(H\mid M,Z)-\mathrm{CE}(H\mid M,Z,X_G),\\
\Delta_{\mathrm{rec}}^{\mathrm{rule}}
&=\mathrm{CE}(H\mid M,Z,\widehat H_{\mathrm{rule}}(X_G))
 -\mathrm{CE}(H\mid M,Z,X_G),\\
\Delta_{\mathrm{2ex}}
&=\mathrm{CE}(H\mid M,Z,X_G)-\mathrm{CE}(H\mid M,Z,X_G,X_C).
\end{aligned}
```

CE terms denote empirical logarithmic losses of trained predictive models on the same final test. $`\Delta_{\mathrm{rec}}`$ measures the total improvement from the first exegesis. The **comparison with the rule model**, $`\Delta_{\mathrm{rec}}^{\mathrm{rule}}`$, compares the actual analytical rendering with prediction from rules. $`\widehat H_{\mathrm{rule}}`$ is produced either by inverting theoretical rules defined in advance or by an empirical mapping learned only during training. The test thus targets the additional predictive trace of exegesis **beyond the rule**. $`\Delta_{\mathrm{2ex}}`$ is computed on the same passages possessing both exegeses, so the difference reflects the additional observation rather than a change of sample.

### Two co-primary historical comparisons

$`\Delta_{\mathrm{rec}}`$ and $`\Delta_{\mathrm{rec}}^{\mathrm{rule}}`$ are **co-primary**. They support two separate claims: the added value of exegesis over metrophonia and context, and its added value over the rule model.

They form a separate historical family of two one-sided tests with Holm correction at 0.05. Minimum meaningful benefits are set before final testing. Each claim requires rejection of its own null hypothesis; the combined claim that both are supported requires both rejections. Test calibration accounts for groups of works and related sources.

$`\Delta_{\mathrm{2ex}}`$ is evaluated separately on the same doubly attested passages, with its own adequacy assessment. The primary comparison in the historical-supervision study and the family of two human hypotheses retain their own protocols. [Provenance and status of the historical protocol](../reference.md#current-protocol-clarifications).

Agreement among two or more old witnesses of the same passage provides an empirical reference for disagreement in historical labels. Together with reading uncertainty and differences between notational strata, it allows recoverability to be interpreted as a property **of the corpus and the relationships among its sources**.

## From inventory to historical map

| Stage | Task | Output |
|---|---|---|
| R0 | Targeted inventory and blind reading of old witnesses; initial target of 10–20 real passages. | Register of passage, witness, uncertainty, one/two exegeses and provenance. |
| R1 | Grammar of eligible old labels by $`M,Z`$. | Predefined classes, progressing from sign to relation and complex. |
| R2 | Synthetic numerical examples for normalisation, marginals, impossible transitions, $`\lambda`$ and calibration. | Verified model before the real final corpus. |
| R3 | Recovery and comparisons on independent works. | $`\Delta_{\mathrm{rec}}^{\mathrm{rule}}`$, $`\Delta_{\mathrm{rec}}`$, $`\Delta_{\mathrm{2ex}}`$, map by old notational sign and exegete. |
| R4 | Probing of finalised M2 representations. | Map of predictive accessibility of $`H`$. |

The first adequacy assessments occur during inventory and again after encoding independent source groups. This gives the ambitious problem a concrete implementation sequence: from verified passages and a controlled inverse model to a publishable map of historical notation. [Knight–Graehl](../../../docs/bibliography/methodology.md#s053), [Snyder–Barzilay–Knight](../../../docs/bibliography/methodology.md#s076) and [Bouchard-Côté et al.](../../../docs/bibliography/methodology.md#s020) provide methodological precedents in inverse script conversion, decipherment and historical change (reference notes in Greek). Here the label is checked through independent reading of an actual musical source, among metrophonically equivalent historical choices.

## R4: historical probing of representations

R4 is applied after the M2 encoders have been finalised: their parameters are no longer updated. Only the probing classifiers examining their outputs are trained. It asks how well $`H`$ can be predicted from symbolic input, selected representation $`R^\star`$ and learned representations B1, B2 and EISE, using the same historical labels, comparable probes and independent works. The **primary** comparison in this methodological development is EISE against B1 and symbolic input; B2 is reported separately because shared-family supervision tends to smooth differences between passages. Capacity controls, control tasks and minimum-description-length criteria support interpretation ([Hewitt–Liang](../../../docs/bibliography/methodology.md#s045), [Voita–Titov](../../../docs/bibliography/methodology.md#s081); reference notes in Greek).

R4 answers whether a historical distinction is **accessible to a specific predictive test** in the learned representation. M2's $`\Delta_{\mathrm{hist}}`$ measures agreement with independent contemporary performance variation. Together, the two criteria show how productively historical supervision can connect formula identity with information from older notation.

[Methodological source for historical recovery (Greek)](../../../sources/proposal-v878-candidate.tex#L764) · [Methodological bibliography (Greek)](../../../docs/bibliography/methodology.md) · [Visual and schematic examples](../examples/index.md)

## Interpreting historical outcomes

| Research outcome | Knowledge about exegetical practice |
|---|---|
| Meaningful benefit in both total recovery and comparison with rules | In this corpus, analytical rendering is systematically associated with old written distinctions, with additional predictive value beyond the particular rule comparator. The passages show where this relationship lies. |
| Meaningful total recovery and a difference against rules within predeclared equivalence bounds | The particular rule adequately accounts for the predictively useful distinction in these classes and conditions. |
| A small upper bound on additional benefit, with adequate coverage and reliable labels | The maximum practically compatible benefit is established for the models and passages examined. Detailed analysis asks whether the pattern relates to exegetical rendering, source relationships or representation limits. |
| Large uncertainty or inadequate coverage | Identifies the distinctions, source groups and additional data required for a more precise conclusion. |

Total recovery and recovery beyond rules are co-primary comparisons with Holm correction. Benefit from a second exegesis is evaluated separately on the same doubly attested passages. Additional predictive value and genealogical relationships between sources are two objects: the model estimates the former and source criticism establishes the latter. Witness dependence thus participates in interpretation without being inferred solely from a performance difference.
