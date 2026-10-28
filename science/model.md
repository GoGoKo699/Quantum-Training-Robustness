# Model, losses, and exact claims

A learned quantum operation is tested on a finite menu of pure input states. The question is whether small error on that menu controls its error on a fresh, Haar-distributed pure input, and how many physical examples are needed to certify that control. Exact identification, robust loss transfer, and sample complexity are separate properties of the menu.

The target is a unitary operation. The implemented or learned hypothesis may be any completely positive, trace-preserving (CPTP) map. This model includes dissipative mismatch that would be excluded by assuming that the hypothesis remains unitary.

All logarithms are natural. Vector norms are Euclidean, and the operator norm $`\|A\|_{\mathrm{op}}`$ is the largest singular value of $`A`$. The commutator convention is $`[A,B]=AB-BA`$.

## 1. Training ensemble and test loss

Let the system have dimension $`d\ge2`$. A fixed training ensemble is

```math
S=\{(p_i,P_i):1\le i\le N\},\qquad
P_i=|\psi_i\rangle\langle\psi_i|,\qquad
p_i>0,\quad\sum_i p_i=1.
```

The $`N`$ support rays are distinct and normalized. Let $`U`$ be the target unitary, write $`\mathcal U(X)=UXU^\dagger`$ for its conjugation channel, and let $`\mathcal V`$ be the hypothesis channel. Define the relative channel

```math
\mathcal E(X)=U^\dagger\mathcal V(X)U.
```

This definition changes coordinates in the analysis. It supplies no physical access to $`U^\dagger`$. In the laboratory, the ideal reference for input $`P_i`$ is $`UP_iU^\dagger`$.

The individual and mean training errors are survival infidelities:

```math
e_i(\mathcal E)=1-\mathrm{Tr}[P_i\mathcal E(P_i)],
\qquad
\epsilon_S(\mathcal E)=\sum_i p_i e_i(\mathcal E).
```

The test error is the average infidelity on a normalized Haar-distributed pure state:

```math
R(\mathcal E)
=\int\left(1-\langle\psi|\mathcal E(|\psi\rangle\langle\psi|)|\psi\rangle\right)d\psi.
```

This distribution includes entangled input states when the system is a composite register. It is a mathematical test distribution; the verifier need not prepare Haar-random inputs. The notation $`R_H`$ in the design and certification pages denotes this same risk: $`R_H=R`$.

For Kraus operators $`K_a`$ satisfying $`\sum_aK_a^\dagger K_a=I`$, the standard average-fidelity identity gives

```math
F_e(\mathcal E)=\frac1{d^2}\sum_a|\mathrm{Tr}\,K_a|^2,
\qquad
R(\mathcal E)=\frac d{d+1}[1-F_e(\mathcal E)].
```

Here $`F_e`$ is entanglement fidelity relative to the identity. Its use is algebraic and does not grant an entangled channel input. The normalization and its connection to process verification are discussed in [Mayer–Knill](../references/RELATED_WORK.md#mayer-knill-2018) and [Zhu–Zhang](../references/RELATED_WORK.md#zhu-zhang-2020).

## 2. The operator form that controls robustness

For an arbitrary complex operator $`A`$, define

```math
Q_S(A)=\sum_i p_i\left(\|A\psi_i\|^2-|\langle\psi_i|A|\psi_i\rangle|^2\right)
=\sum_i p_i\|(I-P_i)A\psi_i\|^2.
```

The form measures how strongly an operator moves the probe vectors out of their own rays. Its kernel is

```math
\mathcal A_S=\{A:A\psi_i\in\mathbb C\psi_i\text{ for every }i\}.
```

These are common **right** eigenoperators. They need not be Hermitian or normal. Since adding a scalar multiple of $`I`$ leaves $`Q_S`$ unchanged, its relevant gap is

```math
\mu_S=\min_{\mathrm{Tr}\,A=0,\ \|A\|_F=1}Q_S(A).
```

The full proof in [Robustness](robustness.md) establishes

```math
\epsilon_S(\mathcal E)=\sum_aQ_S(K_a),
\qquad
R(\mathcal E)=\frac1{d+1}\sum_a
\left\|K_a-\frac{\mathrm{Tr}\,K_a}{d}I\right\|_F^2.
```

Consequently, $`R\le C\epsilon_S`$ for every CPTP map if and only if $`\mathcal A_S=\mathbb CI`$. The optimal coefficient is

```math
C_S=\frac1{(d+1)\mu_S}.
```

This coefficient is globally valid in the loss inequality and is approached by physical channels near the identity. It does not specify the entire finite-error boundary of the feasible loss region.

## 3. Three robustness regimes

Join two probe rays when their inner product is nonzero. A menu exactly identifies the target among CPTP hypotheses if and only if its rays span the system and this overlap graph is connected. This identification criterion is established in [Mayer–Knill](../references/RELATED_WORK.md#mayer-knill-2018).

For a fixed ensemble, define $`W_S(\varepsilon)=\sup_{\epsilon_S(\mathcal E)\le\varepsilon}R(\mathcal E)`$. The resulting classification is:

| Probe condition | Worst compatible test error as training error tends to zero |
|---|---|
| Nonspanning rays or disconnected overlap graph | A nonzero error remains possible at zero training error |
| Connected span and a nonscalar member of $`\mathcal A_S`$ | $`W_S(\varepsilon)=\Theta_S(\sqrt\varepsilon)`$ |
| $`\mathcal A_S=\mathbb CI`$ | $`W_S(\varepsilon)=C_S\varepsilon+O_S(\varepsilon^2)`$ |

The constants here may depend on the dimension, rays, and positive weights. [Probe geometry](probe_geometry.md) gives a basis-coordinate criterion, explicit examples, and their dimension dependence. [Nonunitality](nonunitality.md) explains why the square-root obstruction is absent when every hypothesis is unital.

## 4. Certification access

The statistical task distinguishes

```math
H_0:\mathcal E=\mathrm{id}
\qquad\text{from}\qquad
H_1:R(\mathcal E)\ge\delta,
```

with both decision errors at most $`\alpha\in(0,1/2)`$. The device is the same memoryless channel on every use. The resource $`T`$ is a worst-case cap on channel calls, including protocols that stop early. Expected stopping-time complexity is a different quantity.

On each call, a classical index selects one allowed pure input. The input is fresh and conditionally independent of the verifier's memory given that index. The verifier may keep arbitrary quantum memory, measure all collected outputs jointly, and choose future indices using any quantum instrument on its memory. The theorem includes those adaptive strategies.

The input contract supplies prescribed preparations and system outputs. An allowed pure ray may be internally entangled across the system's subsystems. Entanglement between a fresh channel input and retained verifier memory, coherent superpositions of probe choices, arbitrary inputs outside the menu, recycling earlier outputs through the device, and access to its environment are additional resources. The lower bounds do not include those resources.

Two target-reference implementations are distinguished:

1. **Ideal target projectors.** The verifier can test the ideal output ray for each selected input. The exact leading sample coefficient is stated in this model. Preparation, compilation, and measurement costs are accounted for separately.
2. **Paid pure target copies.** Each comparison consumes a fresh trusted ideal output and a hypothesis output. An antisymmetric/SWAP test fails with probability $`e_i/2`$. This preserves the sampling exponents and gives a factor-two sufficient overhead, without asserting the same exact leading coefficient.

The statistical model is described and proved in [Certification](certification.md). It is a certification problem for a fixed hypothesis. A hypothesis selected using training data requires fresh certification data, or a separate treatment of adaptive reuse of the data.

## 5. Optimal design and scalable application

For any $`d\lt N\le d^2`$ pure probes, even with arbitrary weights and imbalance,

```math
C_S\ge\frac{d(N-1)}{(d+1)(N-d)}.
```

Equality requires a uniformly weighted equiangular tight frame and is attained when such a frame exists. [Optimal design](optimal_design.md) proves this bound and its equality conditions. Combining it with the adaptive minimax theorem converts the coefficient into an all-strategy asymptotic sampling bound.

The [product-channel application](product_channels.md) has a stronger structural promise: the relative channel is an exact tensor product of $`n`$ qubit channels and the target is a product unitary. Under this promise, adding a third global product probe changes the optimal sample cost from $`\Theta(n\delta^{-2}\log(1/\alpha))`$ to $`\Theta(\delta^{-1}\log(1/\alpha))`$, uniformly in $`n`$ for sufficiently small global error. Every global example still contains $`n`$ output qubits.

## 6. Reading and verification

The [science map](README.md) organizes the argument. [Interpretation](interpretation.md) connects the results to training and physical resources. [Related work](../references/RELATED_WORK.md) distinguishes imported results from the derived claims. [Finite checks](../verification/README.md) corroborate the explicit matrices and spectra; the universal conclusions rest on the analytical proofs.
