# Quantum Training Robustness

## When does a small training loss certify a quantum operation?

A finite set of pure inputs can identify a target unitary exactly while giving a weak guarantee when its measured training loss is merely small. This repository characterizes that gap for learned or implemented operations that may be arbitrary completely positive, trace-preserving (CPTP) channels.

The decisive object is the variance of an operator on the training rays. Linear control of Haar-average test infidelity holds exactly when the only operators that preserve every training ray as a right eigenvector are scalar multiples of the identity. The corresponding variance gap gives the **optimal global linear coefficient**. A nonscalar, nonnormal direction can instead hide first-order dissipative error behind second-order training loss.

[Read the scientific argument](science/README.md) · [Learn through Watrous](learning/WATROUS_BRIDGE.md) · [Follow the 30 milestones](learning/MILESTONES.md) · [Understand the training and resource implications](science/interpretation.md) · [Compare with prior work](references/RELATED_WORK.md) · [Run the finite checks](verification/README.md)

## Main results

| Question | Result |
|---|---|
| What does exact identification guarantee at small nonzero loss? | A sharp classification: nonidentifiability, square-root robustness, or linear robustness. The distinction is proved through the common right-eigenoperator algebra. |
| What is the best linear coefficient for a fixed weighted ensemble? | $`C_S=1/[(d+1)\mu_S]`$, where $`\mu_S`$ is the variance gap on traceless complex operators. The bound is attained asymptotically by physical CPTP perturbations. |
| How many pure probes are needed for a good coefficient? | For arbitrary weights and imbalance, $`C_S\ge d(N-1)/[(d+1)(N-d)]`$ when $`d\lt N\le d^2`$. Equality requires a uniform equiangular tight frame and is attained when one exists. |
| Can adaptive choice and collective readout remove the precision penalty? | Under fresh inputs selected by a classical menu index, the variance gap optimized over sampling weights, $`\mu_*`$, determines the exact leading certification coefficient in the joint small-error, high-confidence limit. Arbitrary retained quantum output memory is allowed. |
| What changes for unital hypotheses? | Every connected spanning menu has a sharp linear bound. A quantitative nonunitality budget gives the crossover to square-root robustness. |
| Is there a scalable illustration? | For an exact product of $`n`$ qubit channels, two global product probes need order $`n\delta^{-2}\log(1/\alpha)`$ examples; a third gives order $`\delta^{-1}\log(1/\alpha)`$. Each example still uses all $`n`$ qubits. |

Definitions, constants, hypotheses, and full proofs are in the [science pages](science/README.md). The complete finite-error frontier is a separate optimization problem from the best global linear coefficient.

## Learn the project

[Explanatory report](learning/report/Quantum_Training_Robustness_Report.pdf) — a self-contained route from the experiment and qubit example to the proofs, certification recipes, and independent-register result.

The single educational anchor is **John Watrous, *The Theory of Quantum Information* (2018)**. The [Watrous bridge](learning/WATROUS_BRIDGE.md) identifies relevant sections of the author's standard-layout pre-publication version, translates the notation, and connects the textbook foundations to the operator gap, physical noise witness, certification converse, and product-channel application. Root versus squared fidelity and the restricted input-access model are kept explicit.

The [30-milestone map](learning/MILESTONES.md) contains **13 background/preliminaries milestones** and **17 narrative/innovation milestones**. It moves from individual states and channels to the complete experiment, then from the operator mechanism to optimal resource laws. Each milestone includes a central question, an understanding target, earlier dependencies, a conceptual connection, and scientific source pointers.

The map is common to all readers and independent of personal assessment records. Use it with the bridge for self-directed study, or follow the [scientific map](science/README.md) directly for the proofs. [llms.txt](llms.txt) provides question-to-file routes for automated readers.

## Scope

The target is unitary; the hypothesis may dissipate. Test risk is Haar-average gate infidelity on the full system. Certification compares the exact target with a fixed alternative of risk at least $`\delta`$, using fresh data and a worst-case cap on device calls. The exact sampling coefficient assumes ideal target-output projectors. Fresh trusted pure target copies preserve the exponents with a constant comparison overhead.

These are loss-transfer and certification results. Their relation to training, preparation cost, noisy baselines, and the stronger assumptions of the product-channel application is developed in [Interpretation](science/interpretation.md).

## Reproducible checks and sources

The analytical proofs are accompanied by a [NumPy verification script](verification/check_math.py). It checks the explicit Kraus channels, spectra, sharp-coefficient limits, and product formulas. The recorded run passed **234 finite checks in 26 groups**; its environment, seed, tolerances, and coverage are documented in [Verification](verification/README.md).

From the repository root:

```bash
python3 -m pip install -r verification/requirements.txt
python3 verification/check_math.py
```

Finite checks corroborate explicit constructions; universal and adaptive optimality statements rely on the written proofs.

[Related work](references/RELATED_WORK.md) separates established ingredients from the results developed here. [BibTeX references](references/references.bib) provide the cited primary sources. [llms.txt](llms.txt) maps the repository for automated readers.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).

## License

[MIT](LICENSE)
