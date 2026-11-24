# Two versus three probes for independent qubit channels

The general support bound concerns arbitrary channels on a $`d`$-dimensional system. A structural promise can reduce the number of input settings dramatically. This page assumes an exact tensor product of qubit channels and shows that one additional global product input changes both the precision exponent and the dependence on register size.

**Manuscript correspondence.** This page proves **Theorem 4 (Certification of independent qubits)** and reproduces its finite call bounds in **Table I**, corresponding to Section VII and Appendix F. The repetition orders are uniform in register size; the exact leading three-probe coefficient takes the joint small-error, high-confidence limit at fixed register size.

## 1. Product promise and operational task

Let $`n\ge1`$, set $`D=2^n`$, and suppose the relative channel is exactly

```math
\mathcal E=\bigotimes_{j=1}^n\mathcal E_j,
```

where each $`\mathcal E_j`$ is an arbitrary qubit CPTP map. The physical target is a product unitary, so the ideal output projectors are also products. The channel factors may differ between sites. They remain fixed across uses.

This is a promise about the whole channel. Specifying its one-qubit marginals, or allowing a correlated mixture of product channels, does not imply this tensor factorization. The proof uses the factorization of output survival probabilities and entanglement fidelity.

One global call sends a fresh $`n`$-qubit product input through all $`n`$ local channels once and returns all $`n`$ output qubits. The device is memoryless across calls. The verifier has the fresh-input access of [Certification](certification.md#certification-task-and-access-contract): the input is conditionally independent of retained memory given its classical label, while arbitrary quantum output memory, adaptive classical label selection, and collective output measurements are allowed. Its task is to distinguish the exact target from $`R(\mathcal E)\ge\delta`$, with both errors at most $`\alpha`$.

For the upper bounds, two or three global inputs suffice:

```math
S_2=\{|0\rangle^{\otimes n},|+\rangle^{\otimes n}\},
\qquad
S_3=S_2\cup\{|1\rangle^{\otimes n}\},
\quad |+\rangle=\frac{|0\rangle+|1\rangle}{\sqrt2}.
```

The two-direction lower bound also permits every mixed tensor string built from local $`|0\rangle`$ and $`|+\rangle`$. It therefore applies to the much larger menu of $`2^n`$ such preparations.

Let $`T_k^\star(\delta,\alpha)`$ be the smallest worst-case cap on whole-register calls for the menu $`S_k`$. This cap includes every branch of a protocol that stops early. Let $`Y_r=e_{r^{\otimes n}}(\mathcal E)`$ be the survival loss on the global input $`|r\rangle^{\otimes n}`$. For the ordered menu $`(0,+,1)`$, define

```math
p=(3/10,2/5,3/10),\qquad
\epsilon_p=\sum_r p_rY_r,\qquad
C_n=\frac{5D}{D+1}.
```

The risk $`R`$ is the Haar-average infidelity on the full register, including entangled test states.

**Theorem 4 — Certification of independent qubits.** Under this exact-product promise and with ideal target-output projectors available:

**(i)** For every fixed $`0\lt\alpha_*\lt1/2`$, constants independent of $`n,\delta,\alpha`$ give

```math
T_2^\star=\Theta\!\left(n\delta^{-2}\log(1/\alpha)\right),\qquad
T_3^\star=\Theta\!\left(\delta^{-1}\log(1/\alpha)\right)
```

for $`n\ge1`$, $`0\lt\delta\le1/8`$, and $`0\lt\alpha\le\alpha_*`$. The two-probe lower bound also holds on the full menu of mixed tensor strings from the two local directions.

**(ii)** Every channel in the product class obeys the global bound

```math
R(\mathcal E)\le C_n\epsilon_p(\mathcal E).
```

The coefficient $`C_n`$ is optimal over all sampling weights on $`S_3`$. For each fixed $`n`$,

```math
\lim_{\substack{\delta\to0\\\alpha\to0}}
\frac{\delta T_3^\star(\delta,\alpha)}{\log(1/\alpha)}=C_n,
```

with no required relation between the rates at which $`\delta`$ and $`\alpha`$ tend to zero.

The sections below prove the two parts and distinguish whole-register repetitions from total local channel uses.

## 2. Product identities

Write

```math
x_j=1-F_e(\mathcal E_j),\qquad
y_{jr}=1-\mathrm{Tr}[P_r\mathcal E_j(P_r)],
\qquad r\in\{0,+,1\}.
```

For a vector with coordinates in $`[0,1]`$, define

```math
F(z)=1-\prod_{j=1}^n(1-z_j).
```

The Kraus trace formula factors over tensor products, and so does survival on a product input. Consequently,

```math
R(\mathcal E)=\frac D{D+1}F(x),
\qquad
Y_r:=e_{r^{\otimes n}}(\mathcal E)=F(y_r).
```

The test loss is the Haar average on the full $`D`$-dimensional register, including entangled test states. The verifier nevertheless uses only the stated product inputs.

Both global probes in $`S_2`$ being preserved exactly forces every local map to preserve $`|0\rangle`$ and $`|+\rangle`$ exactly. These two nonorthogonal qubit rays identify the local identity channel. Thus $`S_2`$ already identifies the product target exactly.

## 3. Matching two-direction law

For any fixed $`0\lt\alpha_*\lt 1/2`$, there are positive constants independent of $`n,\delta,\alpha`$ such that, for $`0\lt \delta\le1/8`$ and $`0\lt \alpha\le\alpha_*`$,

```math
T_2^\star(\delta,\alpha)
=\Theta\!\left(\frac n{\delta^2}\log\frac1\alpha\right).
```

The same order holds if the two-input menu is expanded to all tensor strings from the two local directions.

### Upper bound

The fixed two-ray qubit robustness theorem gives an absolute constant $`C_0`$ such that

```math
x_j\le C_0\sqrt{y_{j0}+y_{j+}}.
```

This follows from the connected-span square-root bound in [Robustness](robustness.md); the local dimension and the two rays are fixed, so its constant is independent of $`n`$.

Let $`\epsilon_2=(Y_0+Y_+)/2`$. If $`\epsilon_2\le1/4`$, then each $`Y_r\le1/2`$ and

```math
\sum_jy_{jr}
\le -\sum_j\log(1-y_{jr})
=-\log(1-Y_r)
\le2Y_r.
```

Cauchy–Schwarz and $`F(x)\le\sum_jx_j`$ imply

```math
R(\mathcal E)
\le C_0\sum_j\sqrt{y_{j0}+y_{j+}}
\le2C_0\sqrt{n\epsilon_2}.
```

For $`\epsilon_2>1/4`$, increase the absolute constant and use $`R\le1`$. There is therefore a universal $`C`$ such that $`R\le C\sqrt{n\epsilon_2}`$ throughout the product class. Every alternative with $`R\ge\delta`$ has $`\epsilon_2\ge\delta^2/(C^2n)`$. Independent random survival tests attain the upper sample bound. They use only the two uniform global inputs, even if a larger menu is available.

### Lower bound and its uniform calibration

Use the same local channel at every site, with

```math
K_0(t)=\begin{pmatrix}1&0\\0&s\end{pmatrix},
\qquad
K_1(t)=\sqrt t\begin{pmatrix}0&1\\0&1\end{pmatrix},
\qquad s=\sqrt{1-2t}.
```

These Kraus operators are exactly trace preserving for $`0\le t\le1/2`$. Direct calculation gives

```math
y_0=0,\qquad
y_+=\frac{(1-s)^2}{4}=\frac{t^2}{(1+s)^2},
\qquad
x(t)=\frac{1-s}{2}+\frac t4.
```

To obtain global risk exactly $`\delta`$, choose $`t`$ so that

```math
x(t)=x_\delta
:=1-\left(1-\frac{D+1}{D}\delta\right)^{1/n}.
```

For $`0\lt \delta\le1/8`$, put $`z=(D+1)\delta/D\le3/16`$. The inequality $`z=1-(1-x_\delta)^n\le nx_\delta`$ gives the lower bound below. The elementary inequalities $`1-e^{-u}\le u`$ and $`-\log(1-z)\le z/(1-z)`$ give its upper bound:

```math
\frac\delta n\le x_\delta\le\frac{2\delta}{n},
\qquad x_\delta\le\frac3{16}.
```

The function $`x(t)`$ is increasing and $`x(1/4)>3/16`$, so the solution has $`t\le1/4`$. In this interval, $`3t/4\le x(t)\le t`$. Hence

```math
\frac\delta n\le t\le\frac{8\delta}{3n}.
```

Every allowed tensor string from local $`\{0,+\}`$ has output infidelity at most

```math
b=1-(1-y_+)^n
\le ny_+
\le\frac{nt^2}{2}
\le\frac{32\delta^2}{9n}.
```

The ideal output is pure. Its squared fidelity with the alternative output is therefore at least $`1-b`$ on every allowed input. Applying the adaptive classical–quantum fidelity lemma in [Certification](certification.md) gives

```math
T\ge
\frac{\log[1/(4\alpha(1-\alpha))]}{-\log(1-b)}
=\Omega\!\left(\frac n{\delta^2}\log\frac1\alpha\right).
```

Here $`b`$ is uniformly bounded away from one; $`-\log(1-b)\le2b`$ is sufficient in the stated range. The confidence comparison is uniform for $`\alpha\le\alpha_*\lt 1/2`$. Quantum memory and collective measurements cannot remove this penalty under the specified input access.

## 4. An exact three-probe inequality

The sharp uniform three-ray qubit coefficient from [Probe geometry](probe_geometry.md) is $`2+\sqrt2`$. Since local average infidelity equals $`2x_j/3`$, it gives

```math
x_j\le\kappa\sum_{r\in\{0,+,1\}}y_{jr},
\qquad \kappa=\frac{2+\sqrt2}{2}\ge1.
```

The following elementary product inequality transfers this local estimate to the entire register.

### Product inequality

If $`x_j\le\sum_r c_r y_{jr}`$ and every $`c_r\ge1`$, then

```math
F(x)\le\sum_r c_r F(y_r).
```

If some $`\sum_r c_r y_{jr}\ge1`$, the right side is at least that sum, because $`F(y_r)\ge y_{jr}`$, and the assertion follows from $`F(x)\le1`$. Otherwise all coordinate sums are below one. Monotonicity, subadditivity, and radial concavity give

```math
F(x)\le F\!\left(\sum_r c_ry_r\right)
\le\sum_r F(c_ry_r)
\le\sum_r c_rF(y_r).
```

For subadditivity, take independent sites whose mutually exclusive categories have the corresponding coordinate probabilities. The event that any category occurs has probability $`F(\sum_r z_r)`$. A union bound over categories gives at most $`\sum_rF(z_r)`$. For radial concavity, $`f(t)=F(tz)`$ has $`f(0)=0`$ and

```math
f''(t)=-\sum_{i\ne j}z_i z_j\prod_{k\ne i,j}(1-tz_k)\le0
```

throughout the permitted coordinate range. Thus $`F(cz)\le cF(z)`$ for $`c\ge1`$ whenever both arguments lie in the cube.

### Global coefficient

With uniform three-probe loss $`\epsilon_3=(Y_0+Y_++Y_1)/3`$, the product inequality proves the exact, global bound

```math
R(\mathcal E)
\le\frac{3(2+\sqrt2)D}{2(D+1)}\epsilon_3.
```

There is no small-error restriction on this loss inequality. Its coefficient is sharp within the product class: leave all but one site noiseless and approach the sharp local ratio.

Weights $`(p_0,p_+,p_1)=(3/10,2/5,3/10)`$ improve the coefficient. The optimal local weighted inequality gives

```math
x_j\le\frac32y_{j0}+2y_{j+}+\frac32y_{j1}.
```

All three coefficients are at least one, so the same argument yields

```math
R(\mathcal E)\le\frac{5D}{D+1}\epsilon_p(\mathcal E).
```

Again a single noisy site attains the limiting ratio. Moreover, any weights on these three global inputs induce the same local weights at one noisy site. The local optimality theorem therefore proves that $`5D/(D+1)`$ is the best linear coefficient for this fixed global menu within the product class.

## 5. Three-direction sample complexity and exact coefficient

The preceding inequality gives a survival-test upper bound of order $`\delta^{-1}\log(1/\alpha)`$, independent of $`n`$. For the matching order lower bound, apply a small depolarizing channel at only one site. Calibrate its local entanglement infidelity so that the global risk is $`\delta`$. All allowed global probes then have output infidelity of order $`\delta`$. The adaptive fidelity lemma applies once more. Thus

```math
T_3^\star(\delta,\alpha)
=\Theta\!\left(\frac1\delta\log\frac1\alpha\right)
```

uniformly in $`n`$ in the same small-error range.

The exact leading coefficient follows from the minimax construction in [Certification](certification.md#exact-multi-kraus-adversary). The optimized qubit menu has $`\mu_*=1/10`$. Its multi-Kraus adversary obeys $`R_{\rm local}\ge t/3`$ and $`e_i\le t/10+t^2`$ on every local probe. Embed it at one site and use

```math
R_{\rm global}=g_D R_{\rm local},\qquad
g_D=\frac{3D}{2(D+1)}.
```

For sufficiently small $`\delta`$, choose $`t=3\delta/g_D=2(D+1)\delta/D`$. The global risk is at least $`\delta`$ and every global probe error is at most

```math
b_{D,\delta}
=\frac{D+1}{5D}\delta
 +\frac{4(D+1)^2}{D^2}\delta^2.
```

The lower-bound denominator $`-\log(1-b_{D,\delta})`$ and the survival-test upper denominator $`-\log(1-\delta/C_n)`$ are both $`\delta/C_n+O(\delta^2)`$ at fixed $`n`$. Their confidence logarithms have ratio tending to one as $`\alpha\to0`$. Together these prove the coefficient in Theorem 4:

```math
\lim_{\delta\downarrow0,\,\alpha\downarrow0}
\frac{\delta T_3^\star(\delta,\alpha)}{\log(1/\alpha)}
=\frac{5D}{D+1}.
```

This limit fixes $`n`$ and permits $`\delta`$ and $`\alpha`$ to tend to zero independently. The repetition orders in part 1 of Theorem 4 hold uniformly in $`n`$.

### Finite call bounds: manuscript Table I

The two-direction necessary count is the ceiling of the fidelity lower bound evaluated at the exact calibration in [Section 3](#3-matching-two-direction-law). The three-probe sufficient count is

```math
\left\lceil\frac{\log(1/\alpha)}{-\log(1-\delta/C_n)}\right\rceil
```

for weights $`(3/10,2/5,3/10)`$. With $`\alpha=0.05`$ and ideal target-output projectors, these are the manuscript's five rows:

| Qubits $`n`$ | Risk threshold $`\delta`$ | Two directions: calls required at least | Three probes: calls sufficient |
|---:|---:|---:|---:|
| 8 | 5% | 11,312 | 297 |
| **32** | **5%** | **45,489** | **299** |
| 128 | 5% | 181,831 | 299 |
| 32 | 10% | 10,792 | 149 |
| 32 | 2.5% | 186,626 | 598 |

Each whole-register call uses all $`n`$ local channels. The `finite_bounds` routine in [generate_plots.py](../verification/Graph/generate_plots.py) evaluates these necessary and sufficient bounds directly.

## 6. A local physical realization of the hard channel

The two Kraus operators can be written as

```math
K_0=|0\rangle\langle0|+\sqrt{1-2t}|1\rangle\langle1|,
\qquad
K_1=\sqrt{2t}|+\rangle\langle1|.
```

Start with ordinary amplitude damping of probability $`2t`$. Apply a Hadamard to the system conditional on the environment's damping flag, then discard the environment. Equivalently, a one-qubit environment realizes the isometry

```math
|0\rangle\longmapsto|0\rangle|0_e\rangle,
\qquad
|1\rangle\longmapsto
\sqrt{1-2t}|1\rangle|0_e\rangle
+\sqrt{2t}|+\rangle|1_e\rangle.
```

The two images are orthonormal, and tracing out the environment produces exactly the stated channel. It uses a constant number of local gates and one reset environment qubit per local call; the sites can operate in parallel.

The environment flag is inaccessible under the channel-only model. Measuring it would reveal a first-order jump probability and would change the lower-bound access contract. The construction describes an allowed dissipative mismatch, not a statement that unmodified amplitude damping has the same cancellation.

## 7. Physical resources and scope

At fixed small $`\delta`$ and fixed confidence, two directions require order $`n`$ global repetitions and three directions require order one. Each repetition uses $`n`$ local channel applications and returns $`n`$ output qubits. Therefore total local uses scale as

```math
\Theta\!\left(n^2\delta^{-2}\log(1/\alpha)\right)
\quad\text{and}\quad
\Theta\!\left(n\delta^{-1}\log(1/\alpha)\right),
```

respectively. The upper protocols use product preparations and local survival measurements with $`O(n)`$ elementary one-qubit operations per global example in the ideal primitive model. Gate synthesis and preparation calibration at a specified tolerance are separate implementation costs. Paid pure target copies add one full reference register per SWAP comparison and preserve the two exponents.

The general necessity $`N>D`$ for linear robustness applies to arbitrary $`D`$-dimensional CPTP mismatch, whereas this application restricts the alternatives to independent qubit channels. Three global probes are sufficient because of that structural promise. [Interpretation](interpretation.md) explains the resulting distinction between support, samples, and learning cost.
