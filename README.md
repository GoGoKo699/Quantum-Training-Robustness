# Quantum Training Robustness

Companion repository for **Probe Geometry and the Cost of Quantum Gate Certification**. This project is an ongoing collaboration.

## When does a small probe loss certify a quantum gate?

A set of pure probes can identify a target unitary exactly and give a square-root guarantee at small nonzero loss. Mayer and Knill asked which identifying menus give a linear guarantee. The criterion is that every operator having all probe rays as right eigenvectors must be scalar. The operator variance gap gives the **sharp global linear coefficient** when the criterion holds. A dissipative channel attains the square-root order in the other identifying menus.

[Read the scientific argument](science/README.md) · [Learn through Watrous](learning/WATROUS_BRIDGE.md) · [Follow the 30 milestones](learning/MILESTONES.md) · [Understand the training and resource implications](science/interpretation.md) · [Compare with prior work](references/RELATED_WORK.md) · [Run the finite checks](verification/README.md) · [Reproduce the numerical figures](verification/Graph/README.md)

## Main results

| Question | Result |
|---|---|
| What does exact identification guarantee at small nonzero loss? | A sharp classification: nonidentifiability, square-root robustness, or linear robustness. The distinction is proved through the common right-eigenoperator algebra. |
| What is the best linear coefficient for a fixed weighted ensemble? | $`C_S=1/[(d+1)\mu_S]`$, where $`\mu_S`$ is the variance gap on traceless complex operators. The bound is attained asymptotically by physical CPTP perturbations. |
| How many pure probes are needed for a good coefficient? | For arbitrary weights and imbalance, $`C_S\ge d(N-1)/[(d+1)(N-d)]`$ when $`d\lt N\le d^2`$. Equality requires a uniform equiangular tight frame and is attained when one exists. |
| What determines the optimal call count? | For fixed dimension and menu, a positive optimized variance gap $`\mu_*`$ gives the exact leading coefficient $`1/[(d+1)\mu_*]`$ as the infidelity threshold and decision error jointly vanish. The upper bound uses ideal target-output projectors. The converse covers adaptive classical selection of fresh probes and collective measurement of retained outputs. |
| What changes for unital hypotheses? | Every connected spanning menu has a sharp linear bound. A quantitative nonunitality budget gives the crossover to square-root robustness. |
| What does a third global probe buy? | For an exact product of $`n`$ qubit channels, two global product probes need order $`n\delta^{-2}\log(1/\alpha)`$ whole-register calls. A third reduces the order to $`\delta^{-1}\log(1/\alpha)`$. Each call applies all $`n`$ local channels once. |

Definitions, constants, and proofs are in the [science pages](science/README.md). The [related-work notes](references/RELATED_WORK.md) explain the distinction between the sharp global linear coefficient and the full finite-error frontier.

## Learn the project

The single educational anchor is **John Watrous, *The Theory of Quantum Information* (2018)**. The [Watrous bridge](learning/WATROUS_BRIDGE.md) identifies relevant sections of the author's standard-layout pre-publication version, translates the notation, and connects the textbook foundations to the operator gap, physical noise witness, certification converse, and product-channel application. Root versus squared fidelity and the restricted input-access model are kept explicit.

The [30-milestone map](learning/MILESTONES.md) contains **13 background/preliminaries milestones** and **17 narrative/innovation milestones**. It moves from individual states and channels to the complete experiment, then from the operator mechanism to optimal resource laws. Each milestone includes a central question, an understanding target, earlier dependencies, a conceptual connection, and scientific source pointers.

The map is common to all readers and independent of personal assessment records. Use it with the bridge for self-directed study, or follow the [scientific map](science/README.md) directly for the proofs.

## Scope

The target is unitary, and the implementation may be any completely positive, trace-preserving (CPTP) channel. Certification compares the exact target with a fixed alternative whose Haar-average infidelity on the full system is at least $`\delta`$. Each call uses a fresh probe from the prescribed menu. The call count is a worst-case cap. With one fresh trusted pure target copy per call, SWAP comparison preserves the precision exponents.

These are loss-transfer and certification results. Their relation to training, preparation cost, noisy baselines, and the stronger assumptions of the product-channel application is developed in [Interpretation](science/interpretation.md).

## Reproducible checks and sources

The analytical proofs are accompanied by a [NumPy verification script](verification/check_math.py). It checks the explicit Kraus channels, spectra, sharp-coefficient limits, and product formulas. The recorded run passed **234 finite checks in 26 groups**; its environment, seed, tolerances, and coverage are documented in [Verification](verification/README.md).

From the repository root:

```bash
python3 -m pip install -r verification/requirements.txt
python3 verification/check_math.py
```

Finite checks corroborate explicit constructions; universal and adaptive optimality statements rely on the written proofs.

The manuscript cites [release v1.1.0](https://github.com/GoGoKo699/Quantum-Training-Robustness/releases/tag/v1.1.0), at revision `3287066`, for proofs and numerical verification. The [table reproduction recipe](verification/Graph/README.md#reproduce-the-manuscript-table) evaluates all five rows of the manuscript's call-count table with the same generator used for the [companion plots](verification/Graph/README.md).

[Related work](references/RELATED_WORK.md) separates established ingredients from the results developed here. [BibTeX references](references/references.bib) provide the cited primary sources.

## Contact

For questions about the repository, contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).

## License

[MIT](LICENSE)
