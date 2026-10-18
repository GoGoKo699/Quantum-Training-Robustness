# Finite numerical checks

[check_math.py](check_math.py) evaluates the explicit matrices, spectra, and scalar product formulas used in the analytical argument. It provides reproducible checks of normalization, coefficients, and concrete examples. The universal robustness classification, support bound, and statistical lower bounds are established by the proofs in [science](../science/README.md).

## Run the checks

From the repository root, install the dependency and run:

```bash
python3 -m pip install -r verification/requirements.txt
python3 verification/check_math.py
```

The script requires NumPy; [requirements.txt](requirements.txt) specifies `numpy>=1.24,<3`. It was executed successfully with **Python 3.12.14 and NumPy 2.3.5**. It uses `numpy.random.default_rng(20261018)`, so the sampled configurations are fixed for the recorded environment.

The program prints a result for each named group and finishes with:

```text
PASS 234 finite checks in 26 groups
```

A failed comparison raises an `AssertionError` identifying its group. The script does not download data or require quantum hardware.

## Scientific coverage

| Part of the argument | What is evaluated |
|---|---|
| Two-ray and three-ray qubit menus | Direct diagonalization of the two-ray variance spectrum and the three-ray gap at weights $`(3/10,2/5,3/10)`$. |
| Dissipative obstruction | At $`t\in\{0.2,0.05,0.01,0.001\}`$: trace preservation, individual survival losses, the exact square-root loss curve, and the nonunital commutator identity. The environment isometry is checked for orthonormal columns and for the stated Kraus operators obtained from its two environment components. |
| Dimension-dependent probe geometry | For $`d\in\{2,3,4,8\}`$: orthonormality of the traceless operator basis, the full restricted variance spectrum of the basis-plus-superposition family at uniform and optimized weights, and the closed optimized-gap formula. The known simplex is checked for tightness and its gap $`1/d^2`$. |
| A concrete minimax mixture | The qubit trine adversary is evaluated at $`t\in\{0.01,0.1,0.4\}`$. Its Kraus operators are trace preserving, all three probe errors equal $`t/4`$, and its Haar risk equals $`t/3`$. |
| Unbalanced ensembles | Eight sampled configurations in each of dimensions $`2,3,4`$, with $`d+2`$ rays and unequal positive weights. The script checks their gaps against the support bound, evaluates the linear inequality on sampled CPTP maps, and compares the Kraus expression for Haar risk with the direct trace formula. |
| Approach to a sharp coefficient | A channel built from a minimum-gap eigenoperator at $`t=10^{-5}`$ approaches the local weighted coefficient $`10/3`$. Embedding its scalar loss data at one noisy site approaches the product coefficient $`5D/(D+1)`$. |
| Uniform product calibration | For $`n\in\{1,2,8,32,128\}`$ and $`\delta\in\{0.1,0.01,0.001\}`$: the hard channel is calibrated to the target global risk, and the stated parameter and global probe-error bounds are evaluated. |
| Nonidentical local channels | Twelve sampled arrays for each $`n\in\{1,2,4,8\}`$, with site-dependent channels and mixing strengths, are used to evaluate the exact optimized three-probe product inequality. |

## Operator space and numerical tolerances

The variance matrix is represented in a Hilbert–Schmidt orthonormal **Hermitian traceless basis**, but its coefficient vectors are complex. A complex linear combination of that basis represents an arbitrary traceless complex operator. The calculation therefore includes non-Hermitian and nonnormal witnesses; it does not restrict the optimization to Hamiltonian perturbations. This distinction is essential to the dissipative obstruction in [Robustness](../science/robustness.md).

Most equality comparisons use `numpy.allclose` with **both absolute and relative tolerance $`2\times10^{-10}`$**. Sampled inequality comparisons use an additive allowance of the same size. The two ratio checks approaching sharp coefficients have finite-$`t`$ corrections, so their absolute and relative tolerances are respectively $`5\times10^{-4}`$ for the local coefficient and $`8\times10^{-4}`$ for the product coefficient. These looser tolerances concern the approach to a limit, rather than identities claimed exact at nonzero $`t`$.

The large-register calculations use scalar local fidelities and the identity

```math
F(z)=1-\prod_j(1-z_j).
```

The script evaluates small probabilities using `log1p` and `expm1` to reduce cancellation. In particular, the $`n=128`$ cases **do not construct $`2^{128}`$-dimensional matrices or state vectors**. They check the scalar consequences of the product-channel identities. The sampled nonidentical arrays likewise use local qubit matrices and their scalar product formulas.

## What establishes the general conclusions

Finite diagonalizations corroborate the written eigenvalue formulas at the listed dimensions. They cannot establish those formulas for every dimension, prove optimality over all weights or ensembles, or rule out an untested counterexample. The simplex checks evaluate an explicit known construction; they are not a search over ETF existence.

Similarly, the product examples evaluate selected points within the proved range. The entire interval $`0<\delta\le1/8`$, the lower bound for every mixed tensor string, and the validity of the product inequality for all permitted coordinates follow from the analytical arguments in [Product channels](../science/product_channels.md). The script does not simulate adaptive quantum verifiers or establish their optimality by enumeration. Those statements use the fidelity converse and minimax proof in [Certification](../science/certification.md).

The checks are numerical corroboration of the explicit mathematical constructions. They do not measure hardware performance, characterize unknown preparation or readout errors, or establish a literature-priority claim.
