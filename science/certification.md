# Optimal certification from fresh training probes

The robustness gap has an operational meaning: it determines the optimal high-confidence precision coefficient for certifying a fixed quantum operation from a prescribed catalogue of fresh pure inputs. Quantum storage, collective output measurements, and adaptive classical choice of later probes do not remove the geometry-dependent obstruction.

This page proves the statistical statement, including a finite-sample bound and the confidence qualification needed for an exact coefficient. The cq fidelity step is an elementary specialization of the amortization-collapse machinery in [Wilde, Berta, Hirche, and Kaur](../references/RELATED_WORK.md#wilde-et-al-2020), particularly their Lemma 26 at sandwiched Rényi order $`1/2`$. The contribution established here is the reduction from training geometry to an exact channel adversary, together with the resulting sharp coefficient and support law.

## Certification task and access contract

Fix a finite menu of normalized pure rays $`S=\{P_1,\ldots,P_N\}`$ in dimension $`d\geq2`$. The target is a unitary $`U`$, and the device implements a fixed memoryless channel $`\mathcal V`$. Test

```math
H_0:\mathcal V=\mathcal U,
\qquad
H_1:R_H(\mathcal U^\dagger\circ\mathcal V)\geq\delta,
```

where $`\mathcal U(X)=UXU^\dagger`$ and $`R_H`$ is Haar average infidelity. The verifier must have both type-I and worst-case type-II error at most $`\alpha`$. We use $`0\lt \alpha\leq\alpha_*\lt 1/2`$ and sufficiently small $`\delta>0`$. Haar infidelity is at most $`d/(d+1)`$, so there is no nonempty alternative class beyond that range.

The sample budget $`T`$ is a worst-case cap on the number of device calls. Early stopping is allowed within this cap. The theorem does not assert an optimum for an expected stopping-time budget.

The following resources are allowed.

- Before each device call, a common quantum instrument may act on all retained outputs, classical records, and ancillary memory to choose a classical label $`i`$.
- The input to that call is a fresh copy of $`P_i`$, conditionally independent of the retained memory given that classical label.
- The verifier may keep every output coherently, process outputs and memory jointly, and choose subsequent labels adaptively.
- A final collective measurement may act on the entire retained state.

The model supplies neither coherent control of the input label nor inputs entangled with retained verifier memory. A prescribed ray may itself be entangled among subsystems of the channel input; it is still a permitted pure ray. The restriction is to the prescribed menu and to conditional independence from memory, not to internal product structure. The model supplies no recirculation of an output through later device calls, channel-environment access, exposed noise flag, inverse-device access, or Stinespring oracle. Ancillary quantum memory belongs to the verifier and does not alter the prescribed fresh input. Postselection is allowed only as part of a charged protocol with the stated unconditional error guarantee; no inaccessible environment flag becomes available by postselection.

For the exact upper coefficient, the binary target-output projectors $`UP_iU^\dagger`$ are available. Their preparation and measurement implementation costs are counted separately from $`T`$. This assumption is not a claim that arbitrary target projectors have an efficient circuit. The alternative [paid-reference model](#trusted-pure-target-references) preserves the precision exponents with an explicitly counted factor-two sufficient cost. Neither model uses QRAM. Writing $`\mathcal E=\mathcal U^\dagger\circ\mathcal V`$ below is an algebraic change of coordinates; it does not give the verifier a free target inverse.

If $`\mathcal V`$ is a learned hypothesis, it is fixed before these certification data are collected. An adaptive learner's reused training outcomes do not automatically satisfy the fresh-data premise of this test.

## Geometry and risk identities

For $`P_i=|\psi_i\rangle\langle\psi_i|`$, let

```math
e_i(\mathcal E)=1-\mathrm{Tr}\,\bigl[P_i\mathcal E(P_i)\bigr],
\qquad
\epsilon_S(\mathcal E)=\sum_i p_i e_i(\mathcal E),
```

and define

```math
Q_i(A)=\bigl\|(I-P_i)A|\psi_i\rangle\bigr\|^2,
\qquad
Q_p(A)=\sum_i p_iQ_i(A).
```

For a fixed positive distribution $`p`$, denote its gap by $`\mu_S`$. For the menu with optimized weights, put

```math
\mu_*=
\max_{p\in\Delta_N}
\min_{\substack{\mathrm{Tr}\,A=0\\\|A\|_F=1}}Q_p(A).
```

Zero weights are permitted in this optimization. Positive approximations yield the same supremum if a positive distribution on the whole catalogue is required.

For Kraus operators $`K_a`$ of any CPTP channel, the [robustness identities](robustness.md) are

```math
e_i(\mathcal E)=\sum_aQ_i(K_a),
\qquad
R_H(\mathcal E)
=\frac1{d+1}\sum_a
\left\|K_a-\frac{\mathrm{Tr}\,K_a}{d}I\right\|_F^2.
```

In particular, if $`\mu_*>0`$ and $`p`$ is an optimizing distribution, then

```math
\epsilon_S(\mathcal E)\geq c\,R_H(\mathcal E),
\qquad
c=(d+1)\mu_*\in(0,1].
```

## Adaptive cq fidelity lemma

Use squared Uhlmann fidelity and its square root:

```math
F(\rho,\sigma)=\|\sqrt\rho\sqrt\sigma\|_1^2,
\qquad
f(\rho,\sigma)=\sqrt{F(\rho,\sigma)}.
```

The same root-fidelity formula is used for positive subnormalized blocks.

**Lemma 1.** Suppose that for two possible device channels the output states associated with every allowed input obey

```math
F(\rho_i,\sigma_i)\geq1-b
\qquad\text{for every }i,
\qquad 0\leq b\lt 1.
```

Every allowed protocol with at most $`T`$ device calls has final states satisfying

```math
F(\Omega_0,\Omega_1)\geq(1-b)^T.
```

**Proof.** A common instrument that chooses the next classical label produces block-diagonal memory states with subnormalized blocks $`X_i`$ and $`Y_i`$. Their root fidelity is $`\sum_i f(X_i,Y_i)`$. The label probabilities may differ under the two hypotheses; that possibility is retained inside these subnormalized blocks.

Conditional independence of the fresh input and memory means that appending the next channel output gives blocks $`X_i\otimes\rho_i`$ and $`Y_i\otimes\sigma_i`$. Block additivity and tensor multiplicativity of root fidelity imply

```math
\begin{aligned}
f\left(\bigoplus_iX_i\otimes\rho_i,
       \bigoplus_iY_i\otimes\sigma_i\right)
&=\sum_i f(X_i,Y_i)f(\rho_i,\sigma_i)\\
&\geq\sqrt{1-b}\sum_i f(X_i,Y_i).
\end{aligned}
```

Every common instrument or subsequent quantum processing can only increase fidelity. The initial memory is the same under both hypotheses. Iterating therefore gives root fidelity at least $`(1-b)^{T/2}`$, and squaring proves the claim. A stopped branch can be padded with unused calls whose outputs are discarded, so an at-most-$`T`$ budget obeys the same bound. This proof makes no hypothesis-independent assumption about adaptive label probabilities. ∎

The conditional-independence step is the precise point where the fresh-input restriction is used. Coherent control of the label, or an input entangled with retained memory, does not have the displayed cq product-block form.

**Corollary 2, testing lower bound.** If both errors of a final binary test are at most $`\alpha\lt 1/2`$, then

```math
T\geq
\frac{\log\!\left[1/(4\alpha(1-\alpha))\right]}
     {-\log(1-b)}.
```

Indeed, under the null the acceptance probability is at least $`1-\alpha`$, while under the alternative it is at most $`\alpha`$. The fidelity of these two binary distributions is at most $`4\alpha(1-\alpha)`$. Measurement cannot decrease fidelity, so it is at least the premeasurement lower bound $`(1-b)^T`$. If the null must be accepted with probability one, the binary fidelity is at most $`\alpha`$, strengthening the numerator to $`\log(1/\alpha)`$.

This lemma and converse are standard cq fidelity machinery, in the form needed here; see [Wilde et al.](../references/RELATED_WORK.md#wilde-et-al-2020). They are not an independent novelty claim.

## Fixed-menu minimax duality

Let $`\mathcal H_0`$ be the complex Hilbert space of traceless $`d\times d`$ operators with the Hilbert–Schmidt inner product. Write $`\mathsf Q_i`$ for the positive operator representing $`Q_i`$ on $`\mathcal H_0`$. For any Hermitian operator on this space, its smallest eigenvalue is the minimum expectation over density operators on $`\mathcal H_0`$. Consequently

```math
\begin{aligned}
\mu_*
&=\max_{p\in\Delta_N}
   \min_{\substack{Z\succeq0\\\mathrm{Tr}_{\mathcal H_0}Z=1}}
   \sum_i p_i\mathrm{Tr}_{\mathcal H_0}(\mathsf Q_iZ)\\
&=\min_{\substack{Z\succeq0\\\mathrm{Tr}_{\mathcal H_0}Z=1}}
   \max_i\mathrm{Tr}_{\mathcal H_0}(\mathsf Q_iZ).
\end{aligned}
```

The exchange is finite-dimensional convex minimax: both domains are compact and convex, and the payoff is bilinear. Both optima are attained. This use of a density operator on an operator space is a convex representation of the worst direction, not an additional experimental resource.

Choose a minimizing $`Z`$ and factor it as

```math
Z=\sum_a|L_a\rangle\!\rangle\langle\!\langle L_a|,
\qquad
\mathrm{Tr}\,L_a=0,
\qquad
\sum_a\|L_a\|_F^2=1.
```

The factorization may use at most $`d^2-1`$ terms, obtained from the spectral decomposition of $`Z`$. Minimax gives a simultaneous constraint for every ray:

```math
\sum_aQ_i(L_a)
=\mathrm{Tr}_{\mathcal H_0}(\mathsf Q_iZ)
\leq\mu_*.
```

This simultaneous inequality is stronger than choosing a separate adversary after the verifier's weights have been fixed. It is what makes the next construction valid against adaptive label selection.

## Exact multi-Kraus adversary

Set

```math
B=\sum_aL_a^\dagger L_a,
\qquad
K_a(t)=\sqrt t\,L_a,
\qquad
K_0(t)=\sqrt{I-tB},
\qquad 0\leq t\leq1.
```

The operator $`B`$ is positive with trace one, so $`B\preceq I`$. These Kraus operators define an exact CPTP channel because

```math
K_0(t)^\dagger K_0(t)+\sum_aK_a(t)^\dagger K_a(t)
=I-tB+tB=I.
```

The channel has no accessible Kraus flag. The Kraus representation defines its reduced action only.

Since every $`L_a`$ is traceless, its Haar risk satisfies the exact identity

```math
R_H(\mathcal E_t)
=\frac{t}{d+1}
 +\frac1{d+1}
  \left\|K_0(t)-\frac{\mathrm{Tr}\,K_0(t)}{d}I\right\|_F^2
\geq\frac{t}{d+1}.
```

Each training error obeys

```math
e_i(\mathcal E_t)
=t\sum_aQ_i(L_a)+Q_i(K_0(t))
\leq t\mu_*+Q_i(K_0(t)).
```

The residual is uniformly quadratic. Scalar-shift invariance of $`Q_i`$ and spectral calculus give

```math
\begin{aligned}
Q_i(K_0(t))
&=Q_i(K_0(t)-I)\\
&\leq\|K_0(t)-I\|_F^2\\
&\leq\frac{t^2\mathrm{Tr}\,B^2}
             {(1+\sqrt{1-t})^2}\\
&\leq t^2.
\end{aligned}
```

For the penultimate inequality, diagonalize $`B`$ and use $`1-\sqrt{1-t\lambda}=t\lambda/(1+\sqrt{1-t\lambda})`$ for each $`0\leq\lambda\leq1`$. The final inequality uses $`\mathrm{Tr}\,B^2\leq(\mathrm{Tr}\,B)^2=1`$.

Thus one physical channel simultaneously satisfies

```math
R_H(\mathcal E_t)\geq\frac{t}{d+1},
\qquad
\max_i e_i(\mathcal E_t)\leq t\mu_*+t^2.
```

Under the original target, use the alternative $`\mathcal V_t=\mathcal U\circ\mathcal E_t`$. Fidelity is invariant under the common output unitary, and each null output is pure. Therefore its squared fidelity with the alternative output is exactly $`1-e_i(\mathcal E_t)`$. No target inverse is used in constructing the lower-bound experiment.

## Finite-sample sandwich

Assume $`\mu_*>0`$ and define

```math
c=(d+1)\mu_*,
\qquad
b_\delta=c\delta+(d+1)^2\delta^2.
```

Let $`T_{\rm opt}(\delta,\alpha)`$ be the smallest worst-case call cap among all allowed verifiers. Whenever $`0\lt \delta\leq1/(d+1)`$ and $`b_\delta\lt 1`$,

```math
\boxed{
\frac{\log\!\left[1/(4\alpha(1-\alpha))\right]}
     {-\log(1-b_\delta)}
\ \leq\ T_{\rm opt}(\delta,\alpha)
\ \leq\
\left\lceil
\frac{\log(1/\alpha)}{-\log(1-c\delta)}
\right\rceil.
}
```

For the lower bound, set $`t=(d+1)\delta`$ in the exact adversary. Its risk is at least $`\delta`$, while every allowed output has fidelity at least $`1-b_\delta`$ to its null output. Corollary 2 applies to any adaptive verifier.

For the upper bound, independently choose labels from an optimizing distribution and perform the target-output survival test after each call. The mean rejection probability is $`\epsilon_S(\mathcal E)`$. Under the null it is zero, while every alternative has rejection probability at least $`c\delta`$. Accept only if every test passes. The worst-case false-acceptance probability is at most $`(1-c\delta)^T`$, proving the bound. This verifier has perfect completeness and uses no quantum memory across calls.

The lower bound uses a coarse quadratic residual for a transparent finite formula. Retaining $`t^2/(1+\sqrt{1-t})^2`$ gives a stronger finite bound without changing any coefficient limit.

## Exact optimized sampling coefficient

**Theorem 3.** For fixed $`d`$ and fixed finite menu $`S`$ with $`\mu_*>0`$, and with ideal target-output projectors available,

```math
\boxed{
\lim_{\substack{\delta\to0\\\alpha\to0}}
\frac{\delta\,T_{\rm opt}(\delta,\alpha)}{\log(1/\alpha)}
=\frac1{(d+1)\mu_*}.
}
```

There is no required relation between the rates at which $`\delta`$ and $`\alpha`$ tend to zero. Indeed,

```math
-\log(1-b_\delta)=c\delta+O_{d,S}(\delta^2),
\qquad
-\log(1-c\delta)=c\delta+O_{d,S}(\delta^2),
```

and

```math
\frac{\log[1/(4\alpha(1-\alpha))]}{\log(1/\alpha)}\longrightarrow1.
```

The ceiling contributes at most $`\delta/\log(1/\alpha)`$ after normalization. The two sides of the finite-sample sandwich therefore have the same joint limit.

At fixed $`\alpha\lt 1/2`$, that argument gives the controlled bracket

```math
\frac{\log[1/(4\alpha(1-\alpha))]}{c}
\leq\liminf_{\delta\to0}\delta T_{\rm opt}(\delta,\alpha)
\leq\limsup_{\delta\to0}\delta T_{\rm opt}(\delta,\alpha)
\leq\frac{\log(1/\alpha)}{c}.
```

It does not identify an exact coefficient at fixed confidence for arbitrary two-sided-error protocols. If perfect completeness is imposed, Corollary 2 has numerator $`\log(1/\alpha)`$, so the coefficient becomes exact already at fixed confidence:

```math
\lim_{\delta\to0}
\frac{\delta\,T_{\rm pc}(\delta,\alpha)}{\log(1/\alpha)}
=\frac1c.
```

All these coefficient statements keep $`d`$ and $`S`$ fixed. A sufficient onset condition for the displayed quadratic remainder to be negligible compared with its linear term is $`\delta\ll\mu_* /(d+1)`$. No joint dimension-and-precision uniformity follows from this expansion. The separate [product-channel theorem](product_channels.md) establishes its own dimension-dependent and uniform-in-array-size statements.

Combining Theorem 3 with the [support theorem](optimal_design.md) gives an all-strategy constraint. For a menu with $`\mu_*>0`$ and $`d\lt N\leq d^2`$,

```math
\lim_{\substack{\delta\to0\\\alpha\to0}}
\frac{\delta\,T_{\rm opt}(\delta,\alpha)}{\log(1/\alpha)}
\geq\frac{d(N-1)}{(d+1)(N-d)}.
```

An equiangular-tight-frame menu attains this bound when it exists. The corresponding absolute lower coefficient is $`1`$, attained by weighted projective $`2`$-designs. These are constraints on available rays versus channel repetitions, not a requirement to query every catalogue entry.

## Complete precision trichotomy

The overlap graph of the menu joins rays with nonzero inner product. The [geometry theorem](probe_geometry.md) distinguishes exact identification from a positive gap using the common right-eigenoperator space

```math
\mathcal A_S=
\{L:L|\psi_i\rangle\in\mathbb C|\psi_i\rangle
\text{ for every }i\}.
```

For fixed $`d,S`$ and $`0\lt \alpha\leq\alpha_*\lt 1/2`$, the optimal precision orders are

| Geometry of the available rays | Optimal sample order as $`\delta\to0`$ |
|---|---:|
| Rays span, overlap graph is connected, and $`\mathcal A_S=\mathbb CI`$ | $`\Theta_{d,S}(\delta^{-1}\log(1/\alpha))`$ |
| Rays span, overlap graph is connected, and $`\mathcal A_S\neq\mathbb CI`$ | $`\Theta_{d,S}(\delta^{-2}\log(1/\alpha))`$ |
| Rays do not span, or the overlap graph is disconnected | Impossible below a positive fixed risk threshold |

The first row follows from the finite-sample sandwich. Positivity of the gap is independent of the particular positive weights: it is equivalent to the scalar-kernel condition. Thus optimizing weights does not change which row applies.

For the second row, choose a traceless Frobenius-normalized nonscalar $`L\in\mathcal A_S`$. The exact two-Kraus channel

```math
K_1=\sqrt t\,L,
\qquad K_0=\sqrt{I-tL^\dagger L}
```

has $`R_H\geq t/(d+1)`$, while every ray has $`e_i=Q_i(K_0)=O_{d,S}(t^2)`$. The first-order terms vanish for every ray simultaneously because $`Q_i(L)=0`$. Setting $`t=(d+1)\delta`$ and applying the cq converse proves the $`\Omega(\delta^{-2}\log(1/\alpha))`$ lower bound, including adaptive collective protocols. Connected spanning ensures $`Q_p(L^\dagger L)>0`$, so this family exhibits a genuinely quadratic training signal rather than exact nonidentifiability.

For the matching upper bound, fix any positive weights and define

```math
m_S(\delta)
=\min_{\substack{\mathcal E\ \text{CPTP}\\R_H(\mathcal E)\geq\delta}}
  \epsilon_S(\mathcal E).
```

The minimum exists because the channel set is compact and both losses are continuous. The [imported square-root upper bound](robustness.md#imported-square-root-upper-bound), derived from [Mayer–Knill](../references/RELATED_WORK.md#mayer-knill-2018), gives a finite constant $`B_S`$ such that

```math
R_H(\mathcal E)\leq B_S\sqrt{\epsilon_S(\mathcal E)}.
```

Hence $`m_S(\delta)\geq\delta^2/B_S^2`$. Independently sampled survival tests and all-pass acceptance use

```math
T\leq
\left\lceil
\frac{\log(1/\alpha)}{-\log(1-m_S(\delta))}
\right\rceil
=O_{d,S}\bigl(\delta^{-2}\log(1/\alpha)\bigr).
```

For the third row, there is a nonscalar unitary $`W`$ fixing every available ray as a density operator. If the rays do not span, choose different phases on their span and its orthogonal complement. If the overlap graph is disconnected, its component spans are mutually orthogonal, and different phases can be assigned to those spans. Such a unitary has a strictly positive Haar risk $`r_W`$ and produces exactly the same output as the identity on every allowed input. Every allowed adaptive experiment has identical distributions under these hypotheses. Thus no test with both errors below $`1/2`$ is possible for $`0\lt \delta\leq r_W`$.

The constants in the first two rows can depend on the menu's conditioning, its fixed positive weights, and dimension. This is a classification of precision dependence for a fixed experiment, not a universal dimension bound.

## Trusted pure target references

Suppose the exact binary target-output projectors are unavailable, but each trial supplies one fresh trusted copy of the pure target output $`\tau_i=UP_iU^\dagger`$. A SWAP comparison between $`\sigma_i=\mathcal V(P_i)`$ and $`\tau_i`$ measures the antisymmetric outcome with probability

```math
\mathrm{Tr}\,\left[
\frac{I-\mathbb F}{2}(\sigma_i\otimes\tau_i)
\right]
=\frac{1-\mathrm{Tr}(\sigma_i\tau_i)}2
=\frac{e_i}{2}.
```

This is the standard state-comparison identity of [Barnett, Chefles, and Jex](../references/RELATED_WORK.md#barnett-et-al-2003), extended to the mixed device output by linearity. Exact equality of the two pure outputs under the null gives perfect completeness.

For an optimized linear-regime ensemble, independently sampling labels and rejecting on any antisymmetric outcome gives the sufficient bound

```math
T_{\rm SWAP}\leq
\left\lceil
\frac{\log(1/\alpha)}{-\log(1-c\delta/2)}
\right\rceil.
```

Each trial consumes one device call and one target-output copy. For an $`n`$-qubit output, a conventional SWAP-test implementation uses order $`n`$ local controlled swaps and an ancillary control qubit. All reference copies and their preparation costs remain charged. In the singular regime, replacing $`c\delta`$ by $`m_S(\delta)`$ gives the corresponding order-$`\delta^{-2}`$ bound.

The fidelity lower bounds continue to hold because trusted reference states are the same under the two device hypotheses. They cannot make those hypotheses less faithful when merely appended. Thus this model has the same precision orders, with a factor-two sufficient leading device-copy cost for the stated SWAP protocol. The ideal-projector exact coefficient theorem does not automatically establish an exact coefficient for every paid-reference protocol.

Noisy, untrusted, or correlated reference outputs require a separate calibrated promise. They are not covered by the pure-reference argument.

## Shrinking acceptance tolerance

Perfect completeness is a useful boundary condition, but the precision orders also survive a specified shrinking tolerance. Suppose a randomized survival test has an unknown rejection probability $`q=\epsilon_S`$, and the hypotheses guarantee

```math
H_{\rm good}:q\leq\theta m,
\qquad
H_{\rm bad}:q\geq m,
\qquad 0\leq\theta\lt 1,
\qquad 0\lt m\leq1.
```

Use independent trials and reject when their rejection frequency exceeds $`(1+\theta)m/2`$. A binomial lower-tail bound at $`q=m`$ gives an error at most

```math
\exp\left[-\frac{T(1-\theta)^2m}{8}\right]
```

for the bad class. For the good class, monotonicity reduces the worst case to $`q=\theta m`$. A Bernstein upper-tail bound gives the same sufficient exponent: its variance-plus-range denominator is at most $`2m`$, while the squared separation is $`(1-\theta)^2m^2/4`$. Therefore the choice

```math
T=
\left\lceil
\frac{8}{(1-\theta)^2m}\log\frac1\alpha
\right\rceil
```

controls both errors.

Taking $`m=c\delta`$ in the linear regime, or a justified $`m`$ of order $`\delta^2`$ in the singular regime, preserves the respective sample exponent. The acceptable promise here is explicitly on training loss. It does not assert that every channel within an arbitrary fixed noisy neighbourhood of the target is accepted at this cost.

## Fixed noisy baselines have a different exponent

Consider the depolarizing channel whose survival infidelity on every pure input is $`r`$:

```math
\mathcal D_r(X)
=\left(1-\frac{dr}{d-1}\right)X
 +\frac{r}{d-1}\mathrm{Tr}(X)I,
\qquad 0\leq r\leq\frac{d-1}{d}.
```

Its Haar infidelity is also $`r`$, and

```math
\mathcal D_r(P)
=(1-r)P+\frac{r}{d-1}(I-P).
```

Fix $`0\lt r_0\lt (d-1)/d`$ and compare $`\mathcal D_{r_0}`$ with $`\mathcal D_{r_0+\delta}`$ for sufficiently small positive $`\delta`$. For every pure input their output fidelity is

```math
\begin{aligned}
F
&=\left[
\sqrt{(1-r_0)(1-r_0-\delta)}
+\sqrt{r_0(r_0+\delta)}
\right]^2\\
&=1-\frac{\delta^2}{4r_0(1-r_0)}+O_{r_0}(\delta^3).
\end{aligned}
```

The cq converse therefore imposes

```math
T=\Omega\left(
r_0(1-r_0)\,\delta^{-2}\log\frac1\alpha
\right)
```

for distinguishing these two noisy channels under the same fresh-input access contract. This holds for every menu, including an optimal projective design. An additive risk estimator around the fixed noisy baseline would solve such a two-point testing problem at a comparable separation, so it has the same obstruction.

The linear precision law concerns testing an ideal unitary target, or an explicitly shrinking good region whose training signal remains separated at the required scale. It does not imply a generic $`1/\delta`$ cost for additive estimation around fixed noise, unrestricted learning of an unknown unitary, or certification with uncontrolled state-preparation and measurement errors. Those tasks change the statistical or physical contract specified at the start of this page.
