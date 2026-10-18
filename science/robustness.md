# Robustness from the geometry of pure probes

A finite set of pure probes can determine a unitary channel exactly while giving only a square-root bound on its error under arbitrary channel mismatch. The distinction is controlled by the operators for which every probe is a right eigenvector. A scalar common-eigenoperator space gives a linear bound with an exact coefficient; a larger space supplies a physical channel that attains the square-root exponent.

The dimension, loss functions, and access assumptions are fixed in [the model](model.md). In this page, $`d\geq 2`$ and the finite ensemble $`S=\{(p_i,P_i)\}_{i=1}^N`$ are fixed, each $`p_i>0`$, and $`\sum_i p_i=1`$. The target is unitary, and $`\mathcal E=\mathcal U^\dagger\circ\mathcal V`$ denotes the relative CPTP channel. This change of notation does not supply an inverse query to the target.

## Two exact Kraus identities

Write $`P_i=|\psi_i\rangle\langle\psi_i|`$, with normalized $`\psi_i`$, and define

```math
e_i(\mathcal E)=1-\mathrm{Tr}[P_i\mathcal E(P_i)],
\qquad
\epsilon_S(\mathcal E)=\sum_{i=1}^N p_i e_i(\mathcal E),
\qquad
R(\mathcal E)=1-F_{\mathrm{avg}}(\mathcal E,\mathrm{id}).
```

For an arbitrary complex matrix $`A`$, the probe variance is

```math
\begin{aligned}
Q_S(A)
&=\sum_i p_i\left(\|A\psi_i\|^2-
      |\langle\psi_i|A|\psi_i\rangle|^2\right)\\
&=\sum_i p_i\|(I-P_i)A\psi_i\|^2.
\end{aligned}
```

It is a positive semidefinite quadratic form on the complex Hilbert space of matrices with the Hilbert–Schmidt inner product. In particular, the minimizations below include non-Hermitian and nonnormal matrices. Since $`(I-P_i)I\psi_i=0`$, scalar shifts leave it unchanged:

```math
Q_S(A+zI)=Q_S(A),\qquad z\in\mathbb C.
```

Let $`\{K_a\}`$ be any Kraus representation of $`\mathcal E`$, so that $`\sum_aK_a^\dagger K_a=I`$. Trace preservation gives, for each probe,

```math
e_i(\mathcal E)
=\sum_a\left(\|K_a\psi_i\|^2-
 |\langle\psi_i|K_a|\psi_i\rangle|^2\right).
```

Consequently,

```math
\boxed{\epsilon_S(\mathcal E)=\sum_a Q_S(K_a).}
```

The Haar second moment gives

```math
\int |\langle\psi|A|\psi\rangle|^2\,d\psi
=\frac{\|A\|_F^2+|\mathrm{Tr}\,A|^2}{d(d+1)}.
```

Here $`\|\cdot\|_F`$ is the Frobenius norm. Summing this identity over the Kraus operators and using $`\sum_a\|K_a\|_F^2=d`$ yields

```math
\boxed{
R(\mathcal E)
=\frac{1}{d+1}\sum_a
\left\|K_a-\frac{\mathrm{Tr}\,K_a}{d}I\right\|_F^2.
}
```

Equivalently, if $`F_e`$ is entanglement fidelity with respect to the identity,

```math
F_e(\mathcal E)=\frac{1}{d^2}\sum_a|\mathrm{Tr}\,K_a|^2,
\qquad
R(\mathcal E)=\frac{d}{d+1}[1-F_e(\mathcal E)].
```

The two boxed identities are exact and independent of the chosen Kraus representation.

## The linear robustness theorem

Define the common right-eigenoperator space and its gap by

```math
\mathcal A_S
=\{A:A\psi_i\in\mathbb C\psi_i\ \text{for every }i\},
\qquad
\mu_S
=\min_{\substack{\mathrm{Tr}\,A=0\\\|A\|_F=1}}Q_S(A).
```

Positivity of every weight implies $`\ker Q_S=\mathcal A_S`$. The scalar matrices always belong to this kernel. Compactness of the unit sphere in the traceless subspace therefore gives

```math
\mu_S>0\quad\Longleftrightarrow\quad\mathcal A_S=\mathbb CI.
```

**Theorem 1.** The following conditions are equivalent:

1. There is a finite constant $`C`$ such that $`R(\mathcal E)\leq C\epsilon_S(\mathcal E)`$ for every CPTP channel $`\mathcal E`$.
2. $`\mathcal A_S=\mathbb CI`$.
3. $`\mu_S>0`$.

When they hold, the smallest possible coefficient is

```math
\boxed{C_S=\frac{1}{(d+1)\mu_S}.}
```

This is the optimal coefficient of a global linear inequality. Its sharpness can be witnessed by channels arbitrarily close to the identity.

### Proof of the upper bound

Let $`K_a^0=K_a-\mathrm{Tr}(K_a)I/d`$. Scalar-shift invariance and the definition of the gap give

```math
\epsilon_S(\mathcal E)
=\sum_a Q_S(K_a^0)
\geq\mu_S\sum_a\|K_a^0\|_F^2
=(d+1)\mu_S R(\mathcal E).
```

No small-error approximation is used.

### A physical family that tests necessity and sharpness

For any nonscalar matrix $`L`$, set $`B=L^\dagger L`$ and define

```math
K_1(t)=\sqrt t\,L,
\qquad
K_0(t)=\sqrt{I-tB},
\qquad
0\leq t\leq\|L\|_{\mathrm{op}}^{-2}.
```

These are exact Kraus operators of a CPTP channel $`\mathcal E_t`$, because their squared products sum to the identity. In a neighborhood of $`t=0`$,

```math
K_0(t)=I-\frac t2B-\frac{t^2}{8}B^2+O(t^3).
```

The preceding identities then give

```math
\begin{aligned}
\epsilon_S(\mathcal E_t)
&=tQ_S(L)+\frac{t^2}{4}Q_S(B)+O(t^3),\\
R(\mathcal E_t)
&=\frac{t}{d+1}
 \left\|L-\frac{\mathrm{Tr}\,L}{d}I\right\|_F^2+O(t^2).
\end{aligned}
```

All remainders here concern a fixed finite-dimensional matrix $`L`$. The parameterized family is physical on the displayed finite interval, independently of these expansions.

If $`\mu_S>0`$, take a traceless, Frobenius-normalized minimizer $`L`$. The expansions imply

```math
\lim_{t\downarrow0}
\frac{R(\mathcal E_t)}{\epsilon_S(\mathcal E_t)}
=\frac{1}{(d+1)\mu_S}.
```

Thus no smaller global coefficient is possible. If $`\mathcal A_S`$ contains a nonscalar $`L`$, then $`Q_S(L)=0`$. In that case the training loss is $`O(t^2)`$, whereas the Haar risk has a positive term of order $`t`$. A finite linear coefficient is impossible. This proves every implication in Theorem 1.

### What the optimal coefficient does and does not determine

Define the worst-case curve

```math
W_S(\varepsilon)
=\sup\{R(\mathcal E):\mathcal E\ \text{CPTP},
\epsilon_S(\mathcal E)\leq\varepsilon\}.
```

If $`\mu_S>0`$, the upper bound and the same minimizing family imply

```math
W_S(\varepsilon)=C_S\varepsilon+O(\varepsilon^2)
\qquad(\varepsilon\downarrow0),
\qquad
W_S(\varepsilon)\leq C_S\varepsilon\quad\text{for every }\varepsilon.
```

For the lower statement, $`\epsilon_S(\mathcal E_t)=\mu_St+O(t^2)`$ has a locally invertible dependence on $`t`$. Choosing $`t`$ so that this loss equals $`\varepsilon`$ produces $`R=C_S\varepsilon+O(\varepsilon^2)`$. This determines the leading slope and the best linear inequality. It does not determine the complete finite-error function $`W_S`$.

## Exact identification

Let the **overlap graph** have one vertex for each probe and an edge between distinct $`i,j`$ whenever $`\langle\psi_i|\psi_j\rangle\neq0`$.

**Known identification theorem.** The only CPTP channel with $`\epsilon_S=0`$ is the identity if and only if the probes span $`\mathbb C^d`$ and their overlap graph is connected. This is the exact-identification criterion of [Mayer–Knill, Theorem 1](../references/RELATED_WORK.md#mayer-knill-2018); its minimum-setting consequences are also developed by [Li et al.](../references/RELATED_WORK.md#li-et-al-2021).

A direct Kraus proof makes the role of trace preservation explicit. At zero loss, each Kraus operator satisfies $`K_a\psi_i=\lambda_{ai}\psi_i`$. Trace preservation gives

```math
\sum_a|\lambda_{ai}|^2=1,
\qquad
\langle\psi_i|\psi_j\rangle
=\langle\psi_i|\psi_j\rangle
\sum_a\overline{\lambda_{ai}}\lambda_{aj}.
```

The coefficient vectors $`(\lambda_{ai})_a`$ are unit vectors. Across an overlap edge their inner product equals one, so they coincide. Connectivity makes them independent of $`i`$, and spanning makes every $`K_a`$ scalar. The channel is the identity.

For the converse, if the probes occupy a proper subspace $`V`$, the unitary $`I_V\oplus iI_{V^\perp}`$ fixes every probe projector but gives a nonidentity channel. If the overlap graph is disconnected, the spans of its components are mutually orthogonal. Applying different phases to two such subspaces gives the same obstruction.

Exact identification is therefore weaker than linear robustness. Trace preservation can force a collection of Kraus operators to be scalar at zero loss even when the unrestricted matrix space $`\mathcal A_S`$ contains nonscalar operators. Those matrices generate the nearby channel family above.

## Imported square-root upper bound

The upper bound needed when $`\mu_S=0`$ is an existing result. Here is its precise input and the conversion to the weighted loss used in this repository.

Assume spanning and overlap connectivity. Choose $`d`$ independent probes, relabel them $`1,\ldots,d`$, and let $`G_B`$ be their Gram matrix. Give every overlap edge $`(i,j)`$ length $`|\langle\psi_i|\psi_j\rangle|^{-1/2}`$. Let $`W_{kl}`$ be the shortest-path distance between basis vertices $`k,l`$, allowing paths through all $`N`$ probes. Define

```math
C_{\mathrm{MK}}
=\frac{2}{d}\left[
\frac{2}{d}\sum_{1\leq l\lt k\leq d}W_{kl}^2
+\sum_{k=1}^d\sqrt{(G_B^{-1})_{kk}}
\right].
```

[Mayer–Knill, Theorem 2 and Appendix B](../references/RELATED_WORK.md#mayer-knill-2018), establish, with $`s=\max_i e_i(\mathcal E)`$,

```math
1-F_e(\mathcal E)
\leq C_{\mathrm{MK}}\sqrt s+O_S(s)
\qquad(s\downarrow0).
```

The uniform consequence used here is that finite constants $`A_S,s_0>0`$ exist such that $`1-F_e\leq A_S\sqrt s`$ for every compatible CPTP channel with $`s\leq s_0`$. This assertion does not require the coefficient $`C_{\mathrm{MK}}`$ to be tight.

Set $`p_{\min}=\min_i p_i>0`$. Nonnegativity of individual errors gives $`s\leq\epsilon_S/p_{\min}`$, and hence

```math
R(\mathcal E)
\leq\frac{d A_S}{(d+1)\sqrt{p_{\min}}}
\sqrt{\epsilon_S(\mathcal E)}
```

whenever $`\epsilon_S\leq p_{\min}s_0`$. Enlarging the constant to cover the remaining compact loss interval, using $`R\leq1`$, gives a finite $`B_S`$ with

```math
\boxed{
R(\mathcal E)\leq B_S\sqrt{\epsilon_S(\mathcal E)}
\quad\text{for every CPTP }\mathcal E.
}
```

For example, choose a positive threshold $`\varepsilon_0\leq\min\{p_{\min}s_0,1\}`$ and take $`B_S`$ at least both the local coefficient and $`\varepsilon_0^{-1/2}`$. This global coefficient depends on the fixed ensemble and dimension; no dimension-uniform estimate is asserted here.

## The sharp robustness trichotomy

**Theorem 2.** For a fixed finite pure ensemble with positive weights, the worst-case curve has exactly the following alternatives.

| Probe geometry | Behavior as the loss tends to zero |
|---|---|
| The probes do not span, or the overlap graph is disconnected | $`W_S(0)>0`$ |
| The probes span, the overlap graph is connected, and $`\mathcal A_S\neq\mathbb CI`$ | $`W_S(\varepsilon)=\Theta_S(\sqrt\varepsilon)`$ |
| $`\mathcal A_S=\mathbb CI`$ | $`W_S(\varepsilon)=C_S\varepsilon+O(\varepsilon^2)`$ |

The first and third rows follow from the preceding results. For the middle row, choose a nonscalar $`L\in\mathcal A_S`$. The square-root upper bound is already available. It remains to show that the quadratic coefficient of the physical witness is positive.

Suppose, to the contrary, that $`Q_S(L^\dagger L)=0`$. Every probe would then be an eigenvector of the Hermitian matrix $`L^\dagger L`$. Nonorthogonal eigenvectors of a Hermitian matrix have the same eigenvalue. Overlap connectivity and spanning therefore imply $`L^\dagger L=cI`$. If $`c=0`$, then $`L=0`$. If $`c>0`$, the matrix $`L/\sqrt c`$ is unitary and has every probe as an eigenvector. The same connected-spanning argument for a normal matrix makes it scalar. Both possibilities contradict the choice of $`L`$.

Thus

```math
\beta_L=\frac14Q_S(L^\dagger L)>0,
\qquad
a_L=\frac{1}{d+1}
\left\|L-\frac{\mathrm{Tr}\,L}{d}I\right\|_F^2>0.
```

For the exact family above,

```math
\epsilon_S(\mathcal E_t)=\beta_Lt^2+O(t^3),
\qquad
R(\mathcal E_t)=a_Lt+O(t^2).
```

Choosing the small positive solution of $`\epsilon_S(\mathcal E_t)=\varepsilon`$ gives

```math
W_S(\varepsilon)
\geq\frac{a_L}{\sqrt{\beta_L}}\sqrt\varepsilon+O(\varepsilon).
```

This proves the matching exponent. The displayed witness coefficient need not be the largest square-root coefficient among all channels.

## First-order invisibility is a statement about the loss

Expanding the physical family as a channel gives

```math
\mathcal E_t(X)
=X+t\left(LXL^\dagger-\frac12\{L^\dagger L,X\}\right)+O(t^2).
```

When $`L\psi_i=\lambda_i\psi_i`$, the first derivative of the survival infidelity vanishes. The first derivative of the output density matrix can still be nonzero. In fact, writing $`B=L^\dagger L`$,

```math
\left.\frac{d}{dt}\mathcal E_t(P_i)\right|_{t=0}
=-\frac12\left[(I-P_i)BP_i+P_iB(I-P_i)\right].
```

Its expectation in $`P_i`$ is zero, although the off-diagonal matrix terms can survive. Therefore the probes are not being asserted to be stationary states of a dissipative evolution. Common jump eigenvectors appear in the established theory of pure stationary states, where an additional effective-Hamiltonian condition is required; see [Kraus et al., Theorem 1](../references/RELATED_WORK.md#kraus-et-al-2008).

The channel family is necessarily nonunital in the singular identifying case. [The nonunitality analysis](nonunitality.md) proves this statement and gives the sharp joint dependence on training error and a nonunitality budget. [Probe geometry](probe_geometry.md) supplies computable criteria and exact examples. [Certification](certification.md) turns the loss exponents into optimal experimental sample exponents.
