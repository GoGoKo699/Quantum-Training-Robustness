# Relation to established results

This project studies the robustness of a prescribed finite menu of pure input states. The target operation is unitary, the implemented operation may be any completely positive trace-preserving (CPTP) channel, and the observed loss is the average survival infidelity on the menu. The target risk is Haar-average gate infidelity. Its sampling results concern certification with fresh inputs chosen through a classical menu index; quantum storage, adaptive choice of later indices, and collective output measurements are allowed.

The main distinction is between **exact identification**, **stability of that identification**, and **the repetitions needed to certify a prescribed accuracy**. These questions have related but different answers. This page records which ingredients are established results and where the present theorems extend them. Citation keys match [references.bib](references.bib).

## Exact identification and quantitative robustness

<a id="reich-et-al-2013"></a>

[Reich, Gualdi, and Koch (2013)](https://doi.org/10.1103/PhysRevA.88.042309), *Minimum number of input states required for quantum gate characterization*, introduced the orthonormal-basis-plus-superposition construction in this context. Their work also treats mixed probes, for which the counting problem differs. The present project uses pure probes and does not claim the familiar $`d+1`$ construction as a new input design.

<a id="fiurasek-sedlak-2014"></a>

[Fiurášek and Sedlák (2014)](https://doi.org/10.1103/PhysRevA.89.012323), *Bounds on quantum process fidelity from minimum required number of quantum state fidelity measurements*, derive a tight two-qubit process-fidelity bound from the mean fidelity on a basis and the fidelity on its balanced superposition. Their Sections II–III solve that particular finite-error optimization, and Section IV discusses more qubits. Consequently, neither linear robustness of the basis-plus-superposition family nor its possible precision penalty is new here. The present work gives the exact best linear coefficient for that family in arbitrary dimension, including optimized weights, within a general characterization.

<a id="baldwin-et-al-2014"></a>

[Baldwin, Kalev, and Deutsch (2014)](https://doi.org/10.1103/PhysRevA.90.012110), *Quantum process tomography of unitary and near-unitary maps*, study unitarily informationally complete probes and reconstruction under a unitary or near-unitary prior. This is an important antecedent for economical characterization and sensitivity to model assumptions. Their tomography objective and reconstructed information differ from the survival-loss-to-risk coefficient studied here.

<a id="mayer-knill-2018"></a>

[Mayer and Knill (2018)](https://doi.org/10.1103/PhysRevA.98.052326), *Quantum Process Fidelity Bounds from Sets of Input States*, is the closest prior work. Theorem 1 proves that pure rays identify a unitary among all CPTP channels exactly when they span the Hilbert space and their nonorthogonality graph is connected. Theorem 2 gives a square-root upper bound on process infidelity. Theorem 3 proves linear bounds for equiangular tight frames (ETFs), including the simplex. The discussion after Theorem 2 explicitly asks which input geometry makes the square-root term vanish. Their conclusion additionally asks about optimal probe sets at fixed cardinality and finite error.

The present characterization answers the geometric exponent question through common **right eigenoperators**, which may be nonnormal. It gives the exact optimal global linear coefficient whenever that coefficient is finite, and a matching dissipative obstruction otherwise. The cardinality theorem establishes the optimum of this linear coefficient against arbitrary weights and unbalanced ensembles. It does not solve the entire finite-error optimization posed by Mayer and Knill. Their ETF constructions, coefficients, and product preparation of the qubit simplex are credited ingredients.

## Balanced verification and the number of settings

<a id="zhu-zhang-2020"></a>

[Zhu and Zhang (2020)](https://doi.org/10.1103/PhysRevA.101.042316), *Efficient verification of quantum gates with local operations*, provide a general process-verification framework. Section III allows arbitrary weighted input ensembles and formulates the maximum passing probability as an optimization over channels. Section IV specializes the explicit spectral-gap bounds to balanced ensembles, whose average input is maximally mixed. It would therefore be incorrect to describe their entire framework as restricted to balanced ensembles.

For ideal output-projector tests and balanced inputs, the present variance gap is their preparation gap divided by $`d`$. In the notation of this project,

```math
\mu_S=\frac{\nu_{\mathrm P}}{d},
\qquad
C_S=\frac{d}{(d+1)\nu_{\mathrm P}}.
```

The balanced case is thus consistent with their existing verification theory. The extension here is the exact coefficient and necessity criterion for unbalanced menus, together with matching channel adversaries and the resulting optimal precision laws.

<a id="li-et-al-2021"></a>

[Li, Zhang, Li, and Zhu (2021)](https://doi.org/10.1103/PhysRevA.104.062439), *Minimum number of experimental settings required to verify bipartite pure states and unitaries*, distinguish experimental settings from repetitions and study local and entanglement-free verification. Section IV, Lemmas 2–5, characterizes minimal identifying sets as connected bases. Minimal-setting verification generally uses unbalanced inputs. The present result explains the associated precision cost: a connected basis identifies exactly but cannot have finite linear robustness against unrestricted CPTP mismatch. Its optimal near-target certification cost has the square-law precision exponent.

<a id="hofmann-2005"></a>

[Hofmann (2005)](https://doi.org/10.1103/PhysRevLett.94.160504), *Complementary classical fidelities as an efficient criterion for the evaluation of experimentally realized quantum operations*, gives process-fidelity bounds using two mutually unbiased bases. The constant-order robustness obtained from two such bases is an established benchmark. Counting their $`2d`$ available rays does not imply that every ray must be used in every certification experiment: support size and number of repetitions are separate resources.

## Product probes and dimension-independent bounds

<a id="greenaway-et-al-2021"></a>

[Greenaway, Sauvage, Khosla, and Mintert (2021)](https://doi.org/10.1103/PhysRevResearch.3.033031), *Efficient assessment of process fidelity*, introduce a hierarchy of fidelity approximations and develop the $`0`$-fidelity as an objective that reduces the need to change experimental settings during gate optimization. Its construction uses tensor products of single-qubit SIC states. Their operational motivation is relevant here, but that specific objective and its estimator are established work.

<a id="mayer-2021"></a>

[Mayer (2021)](https://arxiv.org/abs/2109.09629), *A short note on the 0-fidelity*, proves in Theorem 1 that, for arbitrary $`n`$-qubit CPTP channels, the product-SIC survival average $`F_0`$ controls process fidelity $`F_{\mathrm e}`$ through

```math
1-\frac32(1-F_0)\le F_{\mathrm e}\le F_0.
```

This is already a dimension-independent linear bound based on product inputs. It uses the full product-SIC ensemble and does not require the channel itself to factor into independent local channels. The note presents numerical evidence for tightness of its lower bound; the stated analytic result is the inequality.

The three-setting result in this project imposes a different promise: the implemented channel and target both factor over the qubits. Under that promise, three **uniform global strings** suffice for a dimension-independent coefficient. Two local directions have a matching $`n/\delta^2`$ certification cost, even if all mixed strings from those directions are allowed; a third gives order $`1/\delta`$. This combines a much smaller global menu with a stronger channel assumption. It does not replace the arbitrary-channel product-SIC guarantee. Each full-array repetition still contains $`n`$ output qubits and uses all $`n`$ local channels.

## Dissipative variance and stationary-state precedent

<a id="kraus-et-al-2008"></a>

[Kraus, Büchler, Diehl, Kantian, Micheli, and Zoller (2008)](https://doi.org/10.1103/PhysRevA.78.042307), *Preparation of Entangled States by Quantum Markov Processes*, characterize pure stationary states of Markovian dynamics in Theorem 1. A pure stationary state must be a common right eigenvector of the jump operators and satisfy an additional condition involving the effective Hamiltonian. Common-eigenvector and dark-state methods are therefore established ingredients.

The relevant project mechanism is weaker than exact stationarity. For a jump direction $`L`$, the first derivative of survival loss is the nonnegative variance

```math
Q_i(L)=\langle\psi_i|L^\dagger L|\psi_i\rangle
-|\langle\psi_i|L|\psi_i\rangle|^2.
```

Its vanishing means that the ray is a right eigenvector of $`L`$; it need not be stationary under the associated dynamics. The exact two-Kraus construction can change an output state at first order while changing its survival infidelity only at second order. The contribution is the use of these directions to prove a complete robustness classification, sharp coefficients, and sampling lower bounds. The project does not claim the common-eigenvector condition itself as new.

## Adaptive discrimination and trusted reference copies

<a id="wilde-et-al-2020"></a>

[Wilde, Berta, Hirche, and Kaur (2020)](https://doi.org/10.1007/s11005-020-01297-7), *Amortized channel divergence for asymptotic quantum channel discrimination*, supply the relevant established converse framework. In particular, Lemma 26 proves amortization collapse for classical-to-quantum channels and sandwiched Rényi divergences for parameters at least $`1/2`$. At parameter $`1/2`$, this is the fidelity statement used by the adaptive converse. Proposition 21 and Corollary 23 connect amortized distinguishability to discrimination error.

The elementary block-fidelity proof in this project is a specialization of that machinery. It is included to make clear that adaptive input probabilities can differ under the two hypotheses and that arbitrary retained quantum memory is permitted. The new content lies in constructing alternatives from the probe geometry, optimizing them through convex minimax, and deriving the exact leading coefficient under the stated confidence limit. This is a converse for fresh classically indexed inputs, not for coherent input superpositions or repeated passage of a quantum output through the channel.

<a id="barnett-et-al-2003"></a>

[Barnett, Chefles, and Jex (2003)](https://doi.org/10.1016/S0375-9601(02)01602-X), *Comparison of two unknown pure quantum states*, develop universal unambiguous state comparison. The antisymmetric test and the swap identity are established tools. With a trusted pure target-output copy $`P`$ and device output $`\rho`$, the rejection probability is

```math
\operatorname{Tr}\!\left[\frac{I-\mathrm{SWAP}}2(\rho\otimes P)\right]
=\frac{1-\operatorname{Tr}(\rho P)}2.
```

The extension to a mixed device output follows by linearity. Each trial consumes one device use and one fresh trusted target copy. Such references preserve the precision exponents with a constant overhead; noisy or untrusted references are a different access model.

## Fidelity convention and the extent of the results

<a id="nielsen-2002"></a>

The relation between average gate fidelity and entanglement fidelity is standard. [Nielsen (2002)](https://doi.org/10.1016/S0375-9601(02)01272-0), *A simple formula for the average gate fidelity of a quantum dynamical operation*, gives a short derivation and credits the earlier Horodecki relation:

```math
F_{\mathrm{avg}}=\frac{dF_{\mathrm e}+1}{d+1}.
```

Here, state fidelity in the statistical converse is **squared** Uhlmann fidelity. This convention must be distinguished from the root fidelity used in some textbooks. All process-fidelity coefficients from prior work are converted to the Haar-risk convention before comparison.

The support bound and its equality characterization concern the best global **linear** coefficient and the corresponding leading near-target sampling coefficient. They leave the complete finite-error curve separate. The certification experiment uses fresh data after the candidate operation is fixed. It establishes neither the minimax cost of learning an unknown unitary nor a generalization guarantee for adaptively reused training data. The inverse target channel is used algebraically to define the relative channel; its experimental implementation is not a free resource.
