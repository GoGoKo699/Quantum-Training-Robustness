# Thirty milestones for quantum training robustness

[Repository](../README.md) · [Watrous bridge](WATROUS_BRIDGE.md) · [Scientific map](../science/README.md)

This is a project-defined understanding map, independent of a particular reader's background or progress. Its single educational anchor is **Watrous, *The Theory of Quantum Information* (2018)**, using the author's standard-layout pre-publication version. The [source map and notation translation](WATROUS_BRIDGE.md#source-map) identify the relevant sections. Research-level attributions remain in [Related work](../references/RELATED_WORK.md).

The allocation is **13 background/preliminaries milestones and 17 narrative/innovation milestones**. The background connects states, channels, losses, probability, and access assumptions into one well-defined experiment. The narrative starts with an operator identity and builds through probe geometry and noise to optimal certification and the whole-register consequence. The final milestone of each phase combines its components. This route conveys the complete scientific story without claiming to cover every technical lemma or neighboring problem.

Dependencies name earlier milestones only. They organize concepts rather than prescribing a reader's pace or an assessment procedure. Each milestone's source pointers distinguish textbook foundations from the repository's scientific statements.

<a id="background"></a>
## Phase I: background and preliminaries, M01–M13

<a id="m01"></a>
### M01. A pure input is a ray

**Central question:** What is supplied when an experiment prepares a pure input?

**Understanding target:** Explain a normalized vector, its rank-one projector, and why multiplying the vector by a global phase does not change the physical input. Distinguish a ray from a classical label naming its preparation.

**Dependencies and story role:** None. Establish the local object on which every probe constraint acts.

**Conceptual connection:** The projector specifies both the input state and the ideal yes/no survival event.

**Sources:** Watrous §§1.1.1, 2.1.2; [Model](../science/model.md).

<a id="m02"></a>
### M02. The geometry of operators

**Central question:** What does it mean to remove a scalar direction from a matrix?

**Understanding target:** Interpret trace, adjoint, Frobenius norm, and the orthogonal decomposition into scalar and traceless parts. Distinguish arbitrary complex, Hermitian, and normal matrices.

**Dependencies and story role:** M01. Move from state vectors to the operator directions that describe errors.

**Conceptual connection:** A scalar matrix preserves every ray; a nonscalar matrix can also preserve selected rays without being Hermitian.

**Sources:** Watrous §§1.1.2–1.1.3; [Robustness](../science/robustness.md).

<a id="m03"></a>
### M03. A noisy operation is a channel

**Central question:** How can one mathematical operation include both unitary evolution and dissipation?

**Understanding target:** Explain complete positivity, trace preservation, and a Kraus representation. Use the condition that the sum of the squared Kraus operators is the identity to recognize a physical channel.

**Dependencies and story role:** M01, M02. Define the admissible hypothesis class.

**Conceptual connection:** A unitary target does not force the learned or implemented hypothesis to remain unitary.

**Sources:** Watrous §§2.2.1–2.2.3; [Model](../science/model.md).

<a id="m04"></a>
### M04. A dilation is not free environment access

**Central question:** What information is lost when the environment is discarded?

**Understanding target:** Relate an isometry and partial trace to Kraus operators. Distinguish a physical realization of a noisy channel from a verifier that can inspect a jump flag.

**Dependencies and story role:** M03. Specify what the experiment receives, not merely how the device could be built.

**Conceptual connection:** An inaccessible first-order noise flag can coexist with a weak observable survival signal.

**Sources:** Watrous §§2.1.3, 2.2.2; [Nonunitality](../science/nonunitality.md), [Certification](../science/certification.md).

<a id="m05"></a>
### M05. Survival probability and measured loss

**Central question:** What does one ideal-output measurement report?

**Understanding target:** Interpret the measurement with the ideal-output projector and its complement. Distinguish a rejection probability from a single observed failure or a finite-sample estimate.

**Dependencies and story role:** M01, M03. Connect the channel model to an experimental outcome.

**Conceptual connection:** The training loss is an expectation of a physical binary test, not a full reconstruction of the output state.

**Sources:** Watrous §§2.3.1–2.3.2; [Model](../science/model.md).

<a id="m06"></a>
### M06. A weighted menu and its span

**Central question:** How do available rays, sampling weights, and repeated examples differ?

**Understanding target:** Separate the number of distinct preparations from the number of channel calls. Interpret a positive weighted ensemble, its mean state, linear span, and overlap graph.

**Dependencies and story role:** M01, M02, M05. Assemble individual probes into a finite experiment.

**Conceptual connection:** Coverage of a vector space and the frequency of sampling its rays are distinct design choices.

**Sources:** Watrous §§1.1.1, 1.2.2, 2.3.3; [Model](../science/model.md), [Probe geometry](../science/probe_geometry.md).

<a id="m07"></a>
### M07. Training loss is not Haar test risk

**Central question:** What does performance on an unseen input mean here?

**Understanding target:** Distinguish weighted survival loss from Haar-average gate infidelity and entanglement infidelity. Explain the factor relating the latter two and why the mathematical test distribution need not be prepared experimentally.

**Dependencies and story role:** M03, M05, M06. Define the quantity that training performance is meant to control.

**Conceptual connection:** The invariant pure-state second moment converts the global average into a Kraus trace identity.

**Sources:** Watrous §§7.1.1, 7.2.1; [Model](../science/model.md), [Robustness](../science/robustness.md).

<a id="m08"></a>
### M08. State distinguishability and the fidelity convention

**Central question:** How can two different output states remain hard to distinguish?

**Understanding target:** Translate Watrous's root fidelity into the squared fidelity used here. Explain trace distance and monotonicity of fidelity under common processing without identifying them with Haar infidelity.

**Dependencies and story role:** M01, M03, M05. Introduce the comparison tool for an all-measurement lower bound.

**Conceptual connection:** For a pure ideal output, squared fidelity is exactly the survival probability.

**Sources:** Watrous §§3.1.1, 3.2.1–3.2.3; [Notation bridge](WATROUS_BRIDGE.md#notation), [Certification](../science/certification.md).

<a id="m09"></a>
### M09. A certification decision and its confidence

**Central question:** What must a verifier accept and reject?

**Understanding target:** Specify the exact-target null, alternatives separated by a risk threshold, two decision errors, and a worst-case call cap. Explain why all-pass acceptance has false-acceptance probability bounded by a product of pass probabilities.

**Dependencies and story role:** M05, M07, M08. Convert an accuracy requirement into a statistical task.

**Conceptual connection:** A rare rejection signal controls repetitions; catalogue size alone does not.

**Sources:** Watrous §§1.2.2, 3.1.1; [Certification](../science/certification.md).

<a id="m10"></a>
### M10. Fresh classical choices with quantum output memory

**Central question:** Which adaptive strategies are actually allowed?

**Understanding target:** Explain a classical label selected by an instrument on retained memory, followed by a conditionally independent fresh input. Distinguish arbitrary collective output processing from coherent input choice, input-memory entanglement, and recycling outputs.

**Dependencies and story role:** M04, M08, M09. Complete the experiment's information-access model.

**Conceptual connection:** The classical block structure is the exact point used by the adaptive fidelity proof.

**Sources:** Watrous §§2.2–2.3, 3.3.1; [Certification](../science/certification.md).

<a id="m11"></a>
### M11. Positive forms, gaps, and design optimization

**Central question:** Why does a minimum eigenvalue quantify the weakest observed direction?

**Understanding target:** Relate a positive quadratic form to a matrix, its kernel, and a spectral gap. Interpret optimization over sampling probabilities and over positive trace-one operators on an operator space.

**Dependencies and story role:** M02, M06. Supply the mathematical framework for the geometric and minimax results.

**Conceptual connection:** These positive operators encode an optimization variable, not an extra experimentally supplied quantum state.

**Sources:** Watrous §§1.1.2–1.1.3, 1.2.1, 1.2.3; [Optimal design](../science/optimal_design.md), [Certification](../science/certification.md).

<a id="m12"></a>
### M12. Physical promises change the alternatives

**Central question:** What is added by assuming unitality or independence across sites?

**Understanding target:** Explain preservation of the maximally mixed state and exact tensor factorization. Distinguish these promises from each other, from noiselessness, and from knowledge of one-site marginals.

**Dependencies and story role:** M03, M04, M07. Establish how restricted physical classes alter a theorem's scope.

**Conceptual connection:** An identity involving a whole channel may fail for a correlated mixture even when each component looks local.

**Sources:** Watrous §§2.2.2, 4.1, 4.2.2; [Nonunitality](../science/nonunitality.md), [Product channels](../science/product_channels.md).

<a id="m13"></a>
### M13. Assemble the complete certification experiment

**Central question:** What must be fixed before a robustness claim becomes meaningful?

**Understanding target:** Connect the target, physical hypothesis class, menu, loss, test distribution, confidence, and supplied measurements into one model. Explain why a coordinate change does not provide a free target inverse and why a selected hypothesis needs fresh certification data.

**Dependencies and story role:** M01–M12. Synthesize the background into the exact problem solved by the project.

**Conceptual connection:** Preparation, reference outputs, device calls, and readout are separate resources; a bound must keep their roles visible.

**Sources:** Watrous §§2.2–2.3, 3.1; [Model](../science/model.md), [Interpretation](../science/interpretation.md).

<a id="narrative"></a>
## Phase II: narrative and innovation, M14–M30

<a id="m14"></a>
### M14. Express both losses on one operator space

**Central question:** Which identity turns channel robustness into geometry?

**Understanding target:** Explain why training loss is the sum of probe variances of Kraus operators, while Haar risk is their total squared traceless norm divided by the dimension factor. Recognize scalar-shift invariance.

**Dependencies and story role:** M02, M03, M05, M07, M11, M13. Start the contribution with its local algebraic mechanism.

**Conceptual connection:** Measured rejection and unseen-input risk become two quadratic forms on the same channel representation.

**Sources:** Watrous §§2.2.2, 7.2.1; [Robustness](../science/robustness.md), [Bridge 1](WATROUS_BRIDGE.md#loss-to-gap).

<a id="m15"></a>
### M15. The scalar-kernel criterion and optimal coefficient

**Central question:** When can training loss control test risk linearly for every channel?

**Understanding target:** Relate a scalar common right-eigenoperator space to a positive gap and the coefficient $`C_S=1/[(d+1)\mu_S]`$. Distinguish a best global linear inequality from the complete finite-error frontier.

**Dependencies and story role:** M11, M14. Identify the precise property that a training set must satisfy.

**Conceptual connection:** The kernel determines the qualitative regime; the smallest positive eigenvalue determines conditioning. Physical sharpness is developed in M18.

**Sources:** Watrous §§1.1.3, 1.2.1; [Robustness](../science/robustness.md).

<a id="m16"></a>
### M16. Exact identification versus robust identification

**Central question:** Why can zero training error identify a target while small error gives a weak guarantee?

**Understanding target:** Explain the known connected-span identification condition and distinguish the three loss regimes: nonidentifiability, square-root robustness, and linear robustness. Retain the fixed-ensemble qualification on asymptotic constants.

**Dependencies and story role:** M06, M13, M15. Separate an established zero-error fact from the finite-error question.

**Conceptual connection:** Trace preservation constrains a whole set of Kraus operators at zero error more strongly than it constrains a single nearby operator direction.

**Sources:** Watrous §2.2.2 as foundation; [Robustness](../science/robustness.md), [Mayer–Knill attribution](../references/RELATED_WORK.md#mayer-knill-2018).

<a id="m17"></a>
### M17. Coordinate supports diagnose the kernel

**Central question:** How can a finite list of vectors reveal linear robustness?

**Understanding target:** Build the coordinate-support graph from a basis selected from the menu and the supports of additional rays. Explain its relation to common eigenvalues and distinguish it from the overlap graph.

**Dependencies and story role:** M02, M06, M15, M16. Make the abstract criterion directly checkable.

**Conceptual connection:** A nonorthogonal direct-sum decomposition can preserve all selected rays, even when overlap connects them. One extra ray with all basis coordinates nonzero removes this decomposition.

**Sources:** Watrous §1.1; [Probe geometry](../science/probe_geometry.md).

<a id="m18"></a>
### M18. Realize the weak direction as physical noise

**Central question:** Can an operator-space obstruction actually be produced by a device?

**Understanding target:** Explain the exact two-Kraus construction using $`\sqrt t L`$ and $`\sqrt{I-tL^\dagger L}`$. Connect its first-order risk and second-order training signal in a singular identifying menu, and its limiting ratio in a positive-gap menu.

**Dependencies and story role:** M03, M04, M14–M16. Supply physical necessity and sharpness, not just a formal spectral bound.

**Conceptual connection:** Nonnormal common right-eigenoperators describe noise directions excluded by a Hamiltonian-only search.

**Sources:** Watrous §2.2.2; [Robustness](../science/robustness.md), [Bridge 2](WATROUS_BRIDGE.md#hidden-noise).

<a id="m19"></a>
### M19. The qubit example and the extra probe

**Central question:** What changes when $`|1\rangle`$ is added to $`|0\rangle,|+\rangle`$?

**Understanding target:** Relate the exact qubit loss curve to its inaccessible jump flag. Explain why the added probe sees first-order noise, why its uniform coefficient is $`2+\sqrt2`$, and why optimized weights improve it to $`10/3`$.

**Dependencies and story role:** M05, M17, M18. Make the criterion and its physical meaning concrete.

**Conceptual connection:** The new information is a geometric constraint, not an increase in the added state's superposition.

**Sources:** Watrous §§1.1.3, 2.2.2; [Probe geometry](../science/probe_geometry.md), [Nonunitality](../science/nonunitality.md).

<a id="m20"></a>
### M20. An exponent repair can remain poorly conditioned

**Central question:** Does one extra ray give a useful coefficient as dimension grows?

**Understanding target:** Explain the minimal identifying family and the basis-plus-uniform-ray repair. Separate positivity of the gap from its dimension dependence and interpret the improvement from optimized sampling weights.

**Dependencies and story role:** M11, M17–M19. Move from a qubit illustration to dimension-sensitive design.

**Conceptual connection:** The finite range of a fixed-dimensional witness cannot be extrapolated into a uniform fixed-risk many-qubit theorem.

**Sources:** Watrous §§1.1.3, 1.2.1; [Probe geometry](../science/probe_geometry.md).

<a id="m21"></a>
### M21. The support bound and its equality cases

**Central question:** What can any ensemble achieve with a prescribed number of rays?

**Understanding target:** Explain the universal support bound without assuming equal weights or balance. Interpret why equality forces a uniform equiangular tight frame, conditional on its existence, and why a weighted projective 2-design attains coefficient one.

**Dependencies and story role:** M07, M11, M15, M20. Replace examples with an all-ensemble optimal-design statement.

**Conceptual connection:** A rank constraint on the projector moment operator limits how well a finite menu can cover traceless error directions. Balance follows from equality rather than being silently assumed.

**Sources:** Watrous §§1.1.2–1.1.3, 7.2.1 as foundations; [Optimal design](../science/optimal_design.md), [Related work](../references/RELATED_WORK.md).

<a id="m22"></a>
### M22. Unitality removes the singular noise direction

**Central question:** Which physical promise restores linear control without adding a ray?

**Understanding target:** Explain the commutator gap and its exact nonunital correction. Interpret the sharp crossover between training loss, a supplied nonunitality budget, and square-root risk.

**Dependencies and story role:** M12, M14, M16, M18, M21. Separate geometric design from a change in the allowed noise class.

**Conceptual connection:** A balanced ensemble cancels the correction for every channel. A bound on nonunitality is a physical promise, not an observable supplied at no cost.

**Sources:** Watrous §§4.1, 4.2.2; [Nonunitality](../science/nonunitality.md).

<a id="m23"></a>
### M23. One adversary for every sampling strategy

**Central question:** How can a lower bound survive adaptive choice of probes?

**Understanding target:** Interpret the optimized gap and its convex minimax dual. Explain how a positive operator on traceless operator space yields multiple Kraus directions whose losses are simultaneously small on every available ray.

**Dependencies and story role:** M10, M11, M15, M18, M21. Connect geometric optimality to a physically realizable statistical adversary.

**Conceptual connection:** Choosing one bad direction for each fixed distribution is not enough; a simultaneous per-ray bound is needed before adaptation begins.

**Sources:** Watrous §§1.2.1, 1.2.3 as convex foundations; [Certification](../science/certification.md) for the minimax step and exact multi-Kraus construction.

<a id="m24"></a>
### M24. The adaptive fidelity converse

**Central question:** Why does arbitrary quantum output storage not defeat that adversary?

**Understanding target:** Explain root-fidelity addition over classical blocks, multiplication for a fresh output, and monotonicity under common processing. Derive the role of a worst-case call cap and the final binary decision constraint.

**Dependencies and story role:** M08–M10, M23. Turn indistinguishable per-ray outputs into an all-strategy lower bound.

**Conceptual connection:** Adaptive label probabilities can differ under the two hypotheses; subnormalized memory blocks retain that difference. Conditional independence, not an assumption of identical label probabilities, drives the argument.

**Sources:** Watrous §§3.1.1, 3.2; [Certification](../science/certification.md), including its attribution of the classical–quantum fidelity machinery.

<a id="m25"></a>
### M25. The optimal certification law and its limits

**Central question:** When do the upper and lower costs have the same coefficient?

**Understanding target:** Connect survival testing to the minimax adversary and the finite-sample sandwich. Distinguish joint small-error/high-confidence limits, fixed-confidence two-sided brackets, and perfect completeness; recover the precision trichotomy.

**Dependencies and story role:** M09, M16, M21, M23, M24. Complete the general operational theorem.

**Conceptual connection:** Geometry controls optimal repetitions even with collective readout, but the exact general coefficient keeps dimension and menu fixed.

**Sources:** Watrous §§1.2.2, 3.2 as foundations; [Certification](../science/certification.md), [Bridge 4](WATROUS_BRIDGE.md#statistics).

<a id="m26"></a>
### M26. Reference costs and noisy baselines

**Central question:** Which experimental changes preserve the precision exponent?

**Understanding target:** Explain the paid pure-reference SWAP protocol, its half-sized rejection signal, and its separately counted reference copies. Distinguish a shrinking training-loss tolerance from additive estimation around a fixed noisy baseline.

**Dependencies and story role:** M04, M05, M08, M13, M25. Define where the certification theorem can be used without changing its statistical problem.

**Conceptual connection:** A factor-two sufficient overhead does not prove an optimal paid-reference coefficient. A nonzero noise floor changes rare-event testing into a different estimation regime.

**Sources:** Watrous §§2.3, 3.2; [Certification](../science/certification.md), [Interpretation](../science/interpretation.md).

<a id="m27"></a>
### M27. Factor local errors across a register

**Central question:** What connects local survival losses to global Haar risk?

**Understanding target:** Explain the product formulas for entanglement fidelity and probe survival under exact tensor factorization. Distinguish global Haar averaging from a product test distribution.

**Dependencies and story role:** M07, M12, M19, M25. Introduce the stronger promise for a separately uniform many-qubit result.

**Conceptual connection:** Three global product probes need not satisfy the support requirement for unrestricted channels on dimension $`2^n`$ because the alternative class is smaller.

**Sources:** Watrous §§2.2.2, 7.2.1 as foundations; [Product channels](../science/product_channels.md).

<a id="m28"></a>
### M28. Spread hidden dissipation over independent sites

**Central question:** Why do two local directions require more global repetitions as the array grows?

**Understanding target:** Explain the calibrated product of weak qubit witnesses and the matching two-probe upper bound. Retain uniformity in array size and the lower bound even for every tensor string built from the two local directions.

**Dependencies and story role:** M18, M19, M24, M27. Establish the many-site consequence of the local cancellation.

**Conceptual connection:** First-order risks add while local quadratic survival signals remain weak, producing order $`n\delta^{-2}\log(1/\alpha)`$ full-array examples.

**Sources:** Watrous §§2.2.2, 3.2 as foundations; [Product channels](../science/product_channels.md).

<a id="m29"></a>
### M29. Transfer the third-probe repair to the full array

**Central question:** How can one more global preparation remove the array-size repetition penalty?

**Understanding target:** Explain the product inequality transferring local linear bounds to a full register. Interpret the optimized coefficient $`5D/(D+1)`$ and the matching order $`\delta^{-1}\log(1/\alpha)`$ for $`D=2^n`$.

**Dependencies and story role:** M19, M23–M25, M27, M28. Complete the scalable separation and its optimality.

**Conceptual connection:** A single noisy site witnesses the optimal linear coefficient, while noise spread over all sites witnesses the two-direction penalty. These are different roles for hard channels.

**Sources:** Watrous §§1.2.2, 2.2.2 as foundations; [Product channels](../science/product_channels.md), [Bridge 5](WATROUS_BRIDGE.md#array).

<a id="m30"></a>
### M30. Synthesize geometry, physics, and resources

**Central question:** What has the project established, and what does it not imply about learning?

**Understanding target:** Connect menu geometry, permitted noise, loss-transfer exponent, and optimal certification cost into one account. Separate the training optimizer's work from fresh verification, count local uses and references per global example, and distinguish analytical proofs from finite checks and literature comparisons.

**Dependencies and story role:** M13–M29. Synthesize the full contribution and its boundaries rather than append another isolated result.

**Conceptual connection:** Exact identification can coexist with poor robustness; a geometric repair or a stronger physical promise can restore it. Neither supplies a free inverse, an accessible environment, a general learning speedup, or robustness to uncontrolled experimental errors.

**Sources:** Watrous §§2.2–2.3, 3.2–3.3 as foundations; [Interpretation](../science/interpretation.md), [Scientific map](../science/README.md), [Related work](../references/RELATED_WORK.md), [Verification](../verification/README.md).
