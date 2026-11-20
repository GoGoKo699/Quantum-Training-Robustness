# From Watrous to quantum training robustness

[Repository](../README.md) · [30 milestones](MILESTONES.md) · [Scientific map](../science/README.md)

## The single educational anchor

**John Watrous, *The Theory of Quantum Information*, Cambridge University Press, 2018.** Use the [author's book page](https://cs.uwaterloo.ca/~watrous/TQI/) and its standard-layout chapters. Section numbers below refer to the author's 2018 pre-publication version, whose preface is dated January 2018, not to an independently paginated edition. The [errata](https://cs.uwaterloo.ca/~watrous/TQI/TQI.errata.pdf) remain available from that page. The book files are for personal use and are not redistributed here.

The book supplies the mathematical language. The research-specific steps are developed in this repository and attributed in [Related work](../references/RELATED_WORK.md). In particular, the common right-eigenoperator criterion, optimal weighted coefficient, support bound, and restricted-input certification theorem are not assigned to Watrous. The established identification and square-root upper bounds retain their Mayer–Knill attribution.

Use the source sections when their concepts enter the project; reading the entire book is not a prerequisite. The [milestone map](MILESTONES.md) follows the project's argument rather than the book's chapter order.

<a id="source-map"></a>
## Source-to-project map

| Anchor sections | Foundation to extract | Project connection |
|---|---|---|
| [1.1.1–1.1.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf) | Vectors, operators, decompositions, norms | [Operator variance and traceless directions](../science/robustness.md) |
| [1.2.1 and 1.2.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf) | Compact convex sets and semidefinite optimization | [Weight optimization and the project-supplied minimax argument](../science/certification.md) |
| [2.1.2–2.1.3 and 2.2.1–2.2.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | States, reductions, channels, Kraus and isometric representations | [Loss model](../science/model.md) and [physical noise witness](../science/probe_geometry.md) |
| [2.3.1–2.3.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | Outcome probabilities and measurements | [Survival tests and paid reference copies](../science/certification.md) |
| [3.1.1 and 3.2.1–3.2.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Discrimination, fidelity, and its monotonicity | [Adaptive lower bound](../science/certification.md) |
| [3.3.1–3.3.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Channel discrimination and channel distance | [Why the input-access restriction matters](../science/interpretation.md) |
| [4.1 and 4.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.4.pdf) | Unital channels and fixed points | [Commutator identity and nonunitality budget](../science/nonunitality.md) |
| [7.1.1 and 7.2.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.7.pdf) | Symmetric tensors and invariant measures | [Haar second moment](../science/robustness.md) and [design endpoint](../science/optimal_design.md) |

The source's general channel-discrimination setting is not the project's fresh-menu experiment. It provides a comparison, not permission to import entangled inputs or inverse queries into the resource model.

<a id="notation"></a>
## Translate the conventions before importing a formula

Watrous writes a pure state as $`uu^*`$; here it is $`P=|\psi\rangle\langle\psi|`$. His adjoint $`A^*`$ is $`A^\dagger`$ here. His Hilbert–Schmidt norm $`\|A\|_2`$ is the Frobenius norm $`\|A\|_F`$. A channel is a completely positive, trace-preserving linear map on operators, not generally a unitary matrix acting on state vectors.

**Fidelity requires an explicit conversion.** Watrous's Definition 3.11 uses root fidelity. The certification page denotes this by $`f`$ and its square by $`F`$:

```math
f(\rho,\sigma)=\|\sqrt\rho\sqrt\sigma\|_1,
\qquad F(\rho,\sigma)=f(\rho,\sigma)^2.
```

Thus for a pure projector, $`F(P,\rho)=\mathrm{Tr}(P\rho)`$, whereas $`f(P,\rho)=\sqrt{\mathrm{Tr}(P\rho)}`$. Watrous's fidelity monotonicity theorem, Theorem 3.27, applies to $`f`$; squaring preserves the inequality for nonnegative values. Losing this square changes a statistical coefficient.

Haar infidelity $`R=R_H`$, entanglement infidelity $`1-F_e`$, training loss $`\epsilon_S`$, and state trace distance are different quantities. In this project,

```math
R=\frac{d}{d+1}(1-F_e).
```

A small Haar-average error is not automatically a dimension-independent worst-input or diamond-distance guarantee.

For vectorized operators, [Optimal design](../science/optimal_design.md) uses the explicit input-first order

```math
|A\rangle\!\rangle=\sum_{j,k}A_{jk}|k\rangle\otimes|j\rangle.
```

Check this order before translating a vectorization, Choi, or partial-transpose identity. The scalar direction is $`|I\rangle\!\rangle/\sqrt d`$; removing it leaves a complex space of dimension $`d^2-1`$.

<a id="loss-to-gap"></a>
## Bridge 1: from a measured loss to an operator gap

Suppose the desired operation is $`U`$ and the device implements $`\mathcal V`$. Preparing $`P_i`$ and testing its ideal output $`UP_iU^\dagger`$ gives rejection probability $`e_i`$. Writing $`\mathcal E=\mathcal U^\dagger\circ\mathcal V`$ simplifies the proof but supplies no laboratory inverse of $`U`$.

The part of $`A\psi_i`$ perpendicular to $`\psi_i`$ is the part detected by a survival test. Define

```math
Q_S(A)=\sum_i p_i\|(I-P_i)A\psi_i\|^2.
```

For a physical channel, trace preservation converts the sum of squared output amplitudes into total probability one. The [two exact Kraus identities](../science/robustness.md) consequently express both losses on the same operator space:

```math
\epsilon_S=\sum_a Q_S(K_a),
\qquad
R=\frac1{d+1}\sum_a\|K_a^0\|_F^2,
\qquad K_a^0=K_a-\frac{\mathrm{Tr}\,K_a}{d}I.
```

The second identity follows by contracting the pure-state second moment

```math
\int P^{\otimes2}\,dP=\frac{I+\mathbb F}{d(d+1)}
```

with the Kraus operators; $`\mathbb F`$ exchanges the two factors. Here Haar averaging defines the performance metric, not a required input-preparation procedure.

Scalar shifts do not change $`Q_S`$. Its minimum $`\mu_S`$ on unit-norm traceless **complex** operators therefore gives $`\epsilon_S\ge(d+1)\mu_S R`$. If the only common right-eigenoperators of the training rays are scalar, compactness makes this gap positive. The missing physical step is sharpness: a bad operator direction must be realized by a channel, not merely found by diagonalization.

<a id="hidden-noise"></a>
## Bridge 2: turn a bad operator direction into a physical channel

Given an operator $`L`$, the pair

```math
K_1(t)=\sqrt t\,L,
\qquad K_0(t)=\sqrt{I-tL^\dagger L}
```

is exactly trace preserving for $`0\le t\le\|L\|_{\mathrm{op}}^{-2}`$. If every probe is a right eigenvector of a nonscalar $`L`$, the jump contributes no survival loss. The compensating no-jump operator can still contribute quadratically in $`t`$, while Haar error is linear in $`t`$. This is the physical reason exact identification does not ensure linear robustness.

For $`|0\rangle,|+\rangle`$ on one qubit, take

```math
L=\begin{pmatrix}0&1\\0&1\end{pmatrix},
\qquad K_0=\mathrm{diag}(1,\sqrt{1-2t}).
```

Both inputs identify the identity channel at zero error, but this family has

```math
e_0=0,\qquad e_+=\frac{(1-\sqrt{1-2t})^2}{4},\qquad e_1=t.
```

At equal two-ray weights, $`R=\sqrt{2\epsilon_S}-2\epsilon_S/3`$. Adding $`|1\rangle`$ exposes the first-order error and gives the uniform three-ray bound $`R\le(2+\sqrt2)\epsilon_S`$ for every CPTP alternative. [Probe geometry](../science/probe_geometry.md) supplies the spectra and the better weights $`(3/10,2/5,3/10)`$, whose optimal coefficient is $`10/3`$.

This is not ordinary amplitude damping alone: its dilation includes a conditional rotation after a jump. The verifier receives the system, not the environment flag. Restricting the operator calculation to Hermitian matrices, or exposing that flag, removes an essential part of the example.

<a id="geometry-and-noise"></a>
## Bridge 3: distinguish three kinds of structure

The **overlap graph** joins training rays with nonzero inner product. With spanning, its connectivity gives the established exact-identification criterion. The **coordinate-support graph** instead starts from a basis extracted from the menu and asks which coordinates extra rays connect. Its connectivity detects a scalar common right-eigenoperator space and hence linear robustness. The two graphs answer different questions.

A positive gap need not be large. The basis-plus-uniform-ray menu repairs the exponent but still has an optimized coefficient growing with dimension. [Optimal design](../science/optimal_design.md) proves that every weighted ensemble with $`d\lt N\le d^2`$ obeys

```math
C_S\ge\frac{d(N-1)}{(d+1)(N-d)}.
```

Balance is a consequence of equality, not an assumed resource. The equality frames are established constructions and exist only at permitted dimension/cardinality pairs. A weighted projective 2-design attains the absolute coefficient one.

The physical hypothesis class is another independent choice. For unital alternatives, $`\mathcal E(I)=I`$, a commutator form replaces the one-sided variance and gives linear control on every connected spanning menu. The [nonunitality frontier](../science/nonunitality.md) quantifies the crossover using a separately supplied physical promise on $`\mathcal E(I/d)`$. Unital does not mean noiseless; independence across sites is a different promise again.

<a id="statistics"></a>
## Bridge 4: why collective output measurements do not remove the penalty

An all-pass verifier samples a probe, measures its ideal-output projector, and rejects after any failure. If every bad channel has average rejection probability at least $`q`$, then $`T`$ fresh trials have false acceptance at most $`(1-q)^T`$. A linear or quadratic relation between signal and target risk therefore suggests a $`\delta^{-1}`$ or $`\delta^{-2}`$ cost. This is an upper bound only until every permitted verifier is addressed.

The [certification proof](../science/certification.md) optimizes the gap over sampling weights and uses a convex minimax argument to build **one channel that is hard on every allowed ray simultaneously**. This avoids selecting a new adversary after each adaptive choice.

The next label is classical. Conditional on it, the fresh input is independent of retained memory. Root fidelity of classical blocks adds, tensor-product fidelity multiplies, and common quantum processing cannot decrease fidelity. If each null/alternative output pair has squared fidelity at least $`1-b`$, the final states have fidelity at least $`(1-b)^T`$, even with collective readout and arbitrary quantum output storage.

Both testing errors at most $`\alpha`$ then imply

```math
T\ge\frac{\log[1/(4\alpha(1-\alpha))]}{-\log(1-b)}.
```

Combining this with the physical minimax adversary and the survival protocol gives the exact leading coefficient $`1/[(d+1)\mu_*]`$ as $`\delta,\alpha\to0`$, with the menu and dimension fixed. At fixed confidence, unrestricted two-sided testing has a bracket; perfect completeness gives a sharper statement. These limits must not be replaced by an unproved uniform-in-dimension claim.

Fresh trusted pure reference copies permit a SWAP comparison with rejection probability $`e_i/2`$. Each comparison consumes the reference as well as a device output. Fixed noisy baselines are different: their output fidelity can change only quadratically in an additive risk difference, restoring a quadratic sampling cost even for a good menu.

<a id="array"></a>
## Bridge 5: from local noise to a whole-register consequence

Under the exact promise $`\mathcal E=\bigotimes_{j=1}^n\mathcal E_j`$ and a product-unitary target, put $`D=2^n`$ and $`x_j=1-F_e(\mathcal E_j)`$. The product identities are

```math
R=\frac D{D+1}\left[1-\prod_j(1-x_j)\right],
\qquad
Y_r=1-\prod_j(1-y_{jr}),
```

where $`y_{jr}`$ is site $`j`$'s survival loss on local ray $`r`$. Haar risk still concerns the whole register, including entangled test inputs.

Spreading the hidden qubit noise across the sites makes the global risk of order $`nt`$ while the two-direction survival loss is of order $`nt^2`$. Calibrating $`t`$ to $`\delta/n`$ produces the lower-bound signal of order $`\delta^2/n`$. The full proof controls constants uniformly for $`0\lt \delta\le1/8`$; it does not infer a uniform theorem from this heuristic expansion.

Adding the third global input transfers the local linear inequality through the product formula. The [exact array theorem](../science/product_channels.md) yields optimal repetition orders

```math
T_2^\star=\Theta\!\left(n\delta^{-2}\log(1/\alpha)\right),
\qquad
T_3^\star=\Theta\!\left(\delta^{-1}\log(1/\alpha)\right).
```

A repetition still uses all $`n`$ local channels and returns $`n`$ qubits. Correlated channels, correlated mixtures of product channels, and uncontrolled preparation/readout noise are not covered by the independence promise. The support bound for arbitrary $`D`$-dimensional channels and the three-probe product theorem concern different hypothesis classes, so they do not conflict.

## Reconstruct the complete story

Follow [M01–M13](MILESTONES.md#background) to assemble the model, then [M14–M30](MILESTONES.md#narrative) to connect the mechanisms to the bounds. The science pages remain the authoritative proofs; the bridge explains their dependencies and operational meaning.

Use [Verification](../verification/README.md) for the explicit matrices and [Interpretation](../science/interpretation.md) for the distinction between loss transfer, optimization, and fresh-data certification. Finite numerical checks support the constructions but do not establish universal converses or research priority.
