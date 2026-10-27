# Scientific map

The central question is whether a finite pure-state training menu controls the error of a quantum operation on a new input. The argument proceeds from an exact operator identity to geometry, optimal design, and an operational certification theorem.

## Read the argument

For a continuous introduction with worked examples, start with the [explanatory report](../learning/report/Quantum_Training_Robustness_Report.pdf). The topic pages below give the canonical statements, proofs, and source attribution.

| Page | Question answered | Main dependencies |
|---|---|---|
| [Model](model.md) | What is observed, what is the test risk, and which physical resources are supplied? | Finite-dimensional channels, pure states, and average fidelity. |
| [Robustness](robustness.md) | When is loss transfer linear, what is its best coefficient, and when is the square-root exponent unavoidable? | The model and the Kraus representation. |
| [Probe geometry](probe_geometry.md) | How can the criterion be checked, and what happens for minimal and slightly enlarged probe sets? | The variance form and its common right-eigenoperator kernel. |
| [Optimal design](optimal_design.md) | What can any weighted ensemble achieve at a prescribed support size? | The variance gap, positive operators, and finite-dimensional spectral inequalities. |
| [Nonunitality](nonunitality.md) | Which part of the obstruction is dissipative, and what does a bound on nonunitality buy? | The Kraus identities and a commutator gap. |
| [Certification](certification.md) | How many fresh examples are necessary and sufficient, even with adaptive choice and quantum output memory? | Robustness, squared fidelity, and convex minimax. |
| [Product channels](product_channels.md) | How does one extra global probe change the cost for independent qubit channels? | The qubit construction, the certification converse, and exact tensor factorization. |
| [Interpretation](interpretation.md) | What do the theorems imply for quantum training and for an actual resource count? | The conclusions above; detailed proofs can be followed through the links. |

For a conceptual first pass, read the model and interpretation, then the two-probe qubit example in probe geometry. For a proof-oriented pass, follow the table from robustness through certification. The product-channel application can then be read as a complete worked consequence.

## The chain of claims

For a fixed weighted ensemble of rays, the exact Kraus identities relate training error and Haar risk to quadratic forms on operators. Their quotient yields the optimal coefficient. For a connected spanning menu with vanishing variance gap, a nonscalar, nonnormal kernel direction supplies a physical alternative with an unusually weak training signal.

The geometry page makes this criterion explicit in basis coordinates. The design page then bounds the best coefficient over all ensembles with a given support size and characterizes equality, including unbalanced ensembles and unequal weights.

The certification page constructs one hard channel that defeats every permitted adaptive choice of probes. A fidelity converse makes that construction a lower bound for arbitrary collective output measurements. Random survival tests supply the matching upper bound. These steps turn a geometric coefficient into an optimal operational coefficient.

Unitality and tensor factorization enter as additional physical assumptions. Their pages show exactly which conclusions change under each assumption and why.

## Notation and conventions

| Symbol | Meaning |
|---|---|
| $`d`$ | General system dimension. |
| $`N`$ | Number of distinct pure rays in a menu; repetitions are counted separately. |
| $`p_i`$ | Probability assigned to probe $`i`$. Fixed-ensemble results use positive weights. |
| $`\mathcal E`$ | The hypothesis composed algebraically with the inverse target unitary. |
| $`e_i,\epsilon_S`$ | Individual and weighted mean survival infidelity. |
| $`R`$ or $`R_H`$ | Haar-average gate infidelity; these are the same quantity. |
| $`Q_S,\mu_S`$ | The operator variance form and its minimum on unit-norm traceless complex operators. |
| $`C_S`$ | Best global linear coefficient, with $`C_S=+\infty`$ when no finite coefficient exists. |
| $`\mu_*`$ | The variance gap optimized over sampling probabilities on a fixed menu. |
| $`\delta,\alpha,T`$ | Required test-risk separation, maximum decision error, and worst-case device-call cap. |
| $`D=2^n`$ | The full register dimension in the product-channel application. |

State fidelity in the statistical proof is **squared Uhlmann fidelity**. A textbook using root fidelity must be converted before importing a fidelity inequality. Process and Haar infidelities differ by the factor $`d/(d+1)`$.

## Sources and checks

[Related work](../references/RELATED_WORK.md) records the provenance of the identification criterion, the imported square-root upper bound, established frame and verification constructions, and the discrimination converse framework. It also states the boundary of the extensions proved here.

[Finite numerical checks](../verification/README.md) corroborate explicit examples and constants. The analytical proofs establish the statements for all dimensions, channels, ensembles, and permitted adaptive strategies within their stated assumptions.
