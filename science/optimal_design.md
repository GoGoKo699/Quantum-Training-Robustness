# Optimal training-state design

The number of available training rays limits the best robustness coefficient, even when their sampling weights are optimized and their average state is unbalanced. This page proves the sharp bound and characterizes equality. The constructions that attain it, when they exist, are the symmetric frames already used by [Mayer and Knill](../references/RELATED_WORK.md#mayer-knill-2018). The result here establishes optimality against all weighted pure-state ensembles for the global linear coefficient. It does not determine the full finite-error worst-case fidelity curve.

The [model](model.md) fixes the operational meaning of a training ray and distinguishes its catalogue size from the number of channel calls. The [robustness theorem](robustness.md) supplies the exact relation between the spectral gap below and channel infidelity. The [certification theorem](certification.md#exact-optimized-sampling-coefficient) shows that the same optimum controls adaptive certification with quantum output memory.

## Notation and statement

Let $`S=\{P_i=|\psi_i\rangle\langle\psi_i|:1\leq i\leq N\}`$ consist of distinct normalized pure rays in dimension $`d\geq2`$. Let $`p_i>0`$ and $`\sum_i p_i=1`$. Define

```math
\rho_S=\sum_i p_iP_i,
\qquad
Q_S(A)=\sum_i p_i\bigl\|(I-P_i)A|\psi_i\rangle\bigr\|^2,
```

and the gap on the complex traceless operator space by

```math
\mu_S=
\min_{\substack{\mathrm{Tr}\,A=0\\\|A\|_F=1}}Q_S(A).
```

When $`\mu_S>0`$, the smallest constant in the global channel inequality is

```math
R_H(\mathcal E)\leq C_S\epsilon_S(\mathcal E),
\qquad
C_S=\frac{1}{(d+1)\mu_S}.
```

Here $`\epsilon_S`$ is the weighted survival infidelity and $`R_H`$ is Haar average infidelity relative to the unitary target. Set $`C_S=+\infty`$ when no finite linear coefficient exists. The relative-channel notation is an algebraic reduction and supplies no inverse-target oracle.

**Theorem 1, support bound.** Every weighted pure-state ensemble satisfies the following statements.

1. If $`N\leq d`$, then $`\mu_S=0`$.
2. If $`d\lt N\leq d^2`$, then

   ```math
   \mu_S\leq\frac{N-d}{d(N-1)},
   \qquad
   C_S\geq\frac{d(N-1)}{(d+1)(N-d)}.
   ```

   Equality holds exactly when the rays form an equiangular tight frame and all weights are $`1/N`$.
3. For every $`N`$,

   ```math
   \mu_S\leq\frac{1}{d+1}.
   ```

   Equality holds exactly for a weighted complex projective $`2`$-design. Consequently the optimal possible linear coefficient is $`C_S=1`$, and it requires at least $`d^2`$ support rays.

An equiangular tight frame in this statement means

```math
\frac1N\sum_iP_i=\frac{I}{d},
\qquad
\mathrm{Tr}(P_iP_j)=\frac{N-d}{d(N-1)}
\quad(i\neq j).
```

The equality characterization is conditional on existence in the specified dimension and cardinality. It does not assert that an equiangular tight frame exists for every $`d\lt N\leq d^2`$. At $`N=d^2`$, the frame and projective-design characterizations agree.

## Operator representation

Use column vectorization, with the input factor first:

```math
|A\rangle\!\rangle
=\sum_{j,k}A_{jk}|k\rangle\otimes|j\rangle,
\qquad
\langle\!\langle A|B\rangle\!\rangle
=\mathrm{Tr}(A^\dagger B).
```

Define operators on this $`d^2`$-dimensional Hilbert space by

```math
M=\sum_i p_i|P_i\rangle\!\rangle\langle\!\langle P_i|,
\qquad
\Pi_0=\frac{|I\rangle\!\rangle\langle\!\langle I|}{d},
\qquad
\mathsf Q=\rho_S^{\mathsf T}\otimes I-M.
```

Then $`Q_S(A)=\langle\!\langle A|\mathsf Q|A\rangle\!\rangle`$. Each summand of $`Q_S`$ is nonnegative and vanishes on the identity, so

```math
\mathsf Q\succeq0,
\qquad
\mathsf Q|I\rangle\!\rangle=0,
\qquad
\mathsf Q\succeq\mu_S(I-\Pi_0).
```

Also

```math
\mathrm{Tr}\,M=1,
\qquad
\mathrm{rank}\,M\leq N,
\qquad
\mathrm{Tr}\,\mathsf Q=d-1.
```

These are operator traces on the vectorized space, except for the ordinary trace in the vectorization inner product.

The minimum eigenvalue of $`\rho_S`$ bounds the gap from above. To see this, choose a unit eigenvector $`v`$ for $`\lambda_{\min}(\rho_S)`$ and a unit vector $`u\perp v`$. The operator $`A=|u\rangle\langle v|`$ is traceless and has Frobenius norm one, while

```math
Q_S(A)
=\langle v|\rho_S|v\rangle
-\sum_i p_i|\langle\psi_i|u\rangle|^2
                  |\langle v|\psi_i\rangle|^2
\leq\lambda_{\min}(\rho_S).
```

Thus $`\mu_S\leq\lambda_{\min}(\rho_S)`$. This also handles ensembles that do not span the ambient space: their gap is zero.

## Bound without a balance assumption

Assume $`\mu_S>0`$ and temporarily choose $`0\lt \mu\lt \mu_S`$. Set

```math
B=\rho_S-\mu I\succ0,
\qquad
H=B^{\mathsf T}\otimes I+\mu\Pi_0.
```

The gap inequality implies $`M\preceq H`$. Therefore the eigenvalues of $`H^{-1/2}MH^{-1/2}`$ lie in $`[0,1]`$, and its rank is at most $`N`$. It follows that

```math
N\geq\mathrm{Tr}(H^{-1}M).
```

Write

```math
s=\mathrm{Tr}\,B^{-1},
\qquad s_2=\mathrm{Tr}\,B^{-2},
\qquad
a=\mathrm{Tr}(\rho_SB^{-1})=d+\mu s,
\qquad
b=\mathrm{Tr}(\rho_SB^{-2})=s+\mu s_2.
```

The rank-one inverse formula gives

```math
\mathrm{Tr}(H^{-1}M)
=a-\frac{\mu}{a}
     \sum_i p_i\langle\psi_i|B^{-1}|\psi_i\rangle^2.
```

For each unit vector, the variance of the Hermitian operator $`B^{-1}`$ is nonnegative. Hence

```math
\sum_i p_i\langle\psi_i|B^{-1}|\psi_i\rangle^2
\leq\sum_i p_i\langle\psi_i|B^{-2}|\psi_i\rangle
=b,
```

and consequently

```math
N\geq F:=a-\frac{\mu b}{a}.
```

It remains to bound this expression using only the trace of $`\rho_S`$. Let $`x_j=\lambda_j(\rho_S)-\mu>0`$ and put $`\tau=\sum_jx_j=1-d\mu`$. Then

```math
\tau s\geq d^2,
\qquad
\tau(s^2-s_2)\geq d(d-1)s.
```

The first inequality is Cauchy–Schwarz. For completeness, the second has an elementary proof. Expanding by pairs and triples gives

```math
\begin{aligned}
\tau(s^2-s_2)
&=2(d-1)s
 +2\sum_{i\lt j\lt k}
   \frac{x_i^2+x_j^2+x_k^2}{x_ix_jx_k}\\
&\geq2(d-1)s
 +2\sum_{i\lt j\lt k}
   \left(\frac1{x_i}+\frac1{x_j}+\frac1{x_k}\right)\\
&=d(d-1)s.
\end{aligned}
```

For $`d=2`$, the triple sums are empty and the second inequality is an identity. For larger $`d`$, the inequality in each triple follows from the sum of the three squared pairwise differences.

A direct rearrangement now yields

```math
\begin{aligned}
a\tau\left(F-\frac{d(1-\mu)}{1-d\mu}\right)
&=(d-1)\mu\bigl[-d^2+(1-2d\mu)s\bigr]
  +\tau\mu^2(s^2-s_2)\\
&\geq(d-1)\mu(\tau s-d^2)\\
&\geq0.
\end{aligned}
```

Therefore

```math
N\geq\frac{d(1-\mu)}{1-d\mu}.
```

The right-hand side is strictly larger than $`d`$ for $`\mu>0`$. Thus $`N\leq d`$ is incompatible with a positive gap. For $`N>d`$, rearranging and then taking $`\mu\uparrow\mu_S`$ gives

```math
\mu_S\leq\frac{N-d}{d(N-1)}.
```

No balance, equal-weight, or general-position hypothesis entered this proof.

## Equality and the potentially singular endpoint

Suppose $`d\lt N\leq d^2`$ and the cardinality bound is saturated. Define

```math
q=\frac{N-d}{d(N-1)}=\mu_S>0.
```

One must justify passing to $`\mu=q`$, since $`B`$ was made invertible by using $`\mu\lt \mu_S`$. The proof retained the explicit slack

```math
F-\frac{d(1-\mu)}{1-d\mu}
\geq
\frac{(d-1)\mu(\tau s-d^2)}{(d+\mu s)\tau}.
```

If $`\lambda_{\min}(\rho_S)=q`$, then $`s\to\infty`$ as $`\mu\uparrow q`$. Since $`1-dq>0`$, the displayed right-hand side tends to $`d-1`$. Meanwhile $`d(1-q)/(1-dq)=N`$. This contradicts $`N\geq F`$. Hence equality requires $`\lambda_{\min}(\rho_S)>q`$, and all matrices in the proof remain invertible at the endpoint.

At that endpoint every inequality between $`N`$ and $`d(1-q)/(1-dq)`$ must be an equality. In particular, the explicit slack is zero, giving $`\tau s=d^2`$. Equality in Cauchy–Schwarz forces all eigenvalues of $`\rho_S`$ to coincide:

```math
\rho_S=I/d.
```

Thus balance is a consequence of optimality.

For a balanced ensemble, $`M|I\rangle\!\rangle=|I\rangle\!\rangle/d`$ and $`\mathsf Q=I/d-M`$. On the traceless subspace every eigenvalue of $`M`$ is at most

```math
c=\frac1d-q=\frac{d-1}{d(N-1)}.
```

The traceless part of $`M`$ has trace $`(d-1)/d`$ and rank at most $`N-1`$. Its trace equals $`(N-1)c`$, so it must have exactly $`N-1`$ nonzero eigenvalues, all equal to $`c`$.

Consider the weighted projector Gram matrix

```math
G_{ij}=\sqrt{p_ip_j}\mathrm{Tr}(P_iP_j),
\qquad
v=(\sqrt{p_1},\ldots,\sqrt{p_N})^{\mathsf T}.
```

Its nonzero spectrum is that of $`M`$, and balance gives $`Gv=v/d`$. Since $`G`$ has rank $`N`$, the preceding spectrum determines it completely:

```math
G=cI_N+\left(\frac1d-c\right)vv^\dagger.
```

Taking diagonal entries gives

```math
p_i=c+\left(\frac1d-c\right)p_i,
\qquad\text{hence}\qquad p_i=\frac1N.
```

For distinct indices, the off-diagonal entries give

```math
\mathrm{Tr}(P_iP_j)=\frac1d-c
=\frac{N-d}{d(N-1)}.
```

These are exactly the uniform equiangular-tight-frame conditions. Conversely, such a frame has this Gram matrix. Its moment operator consequently has the spectrum just described, and its gap is $`q`$. This proves both necessity and sufficiency, including the endpoint $`N=d^2`$.

## Absolute optimum and projective designs

The operator $`\mathsf Q`$ has trace $`d-1`$, and its scalar direction has eigenvalue zero. Its minimum eigenvalue on the remaining $`d^2-1`$ dimensions cannot exceed their average:

```math
\mu_S\leq\frac{d-1}{d^2-1}=\frac1{d+1}.
```

Equality requires every traceless eigenvalue to equal this average, so

```math
\mathsf Q=\frac{I-\Pi_0}{d+1}.
```

To recover the state moment condition without assuming balance, take the partial trace over the output factor. The definition of $`\mathsf Q`$ gives $`\mathrm{Tr}_{\rm out}\mathsf Q=(d-1)\rho_S^{\mathsf T}`$. The displayed equality therefore forces $`\rho_S=I/d`$. Substituting back yields

```math
M=\frac{I+|I\rangle\!\rangle\langle\!\langle I|}{d(d+1)}.
```

Partial transposition on the input factor converts this into

```math
\sum_i p_iP_i\otimes P_i
=\frac{I+\mathbb F}{d(d+1)},
```

where $`\mathbb F`$ swaps the two $`d`$-dimensional factors. This is the weighted complex projective $`2`$-design condition. Conversely that condition gives the displayed moment operator and gap. Its moment operator has full rank $`d^2`$, so $`N\geq d^2`$ is necessary.

## Optimizing weights on a prescribed menu

For a fixed menu of rays, define

```math
\mu_*=
\max_{p\in\Delta_N}
\lambda_{\min}\left(\left.\sum_i p_i\mathsf Q_i\right|_{\mathrm{Tr}\,A=0}\right),
\qquad
C_*=\frac1{(d+1)\mu_*}
\quad(\mu_*>0).
```

The simplex $`\Delta_N`$ includes zero weights, since an optimizer may choose not to use an available ray. The objective is continuous and concave, and a maximum exists. If strictly positive weights are required, mixing an optimizer with any positive distribution approaches the same optimum.

The support theorem applies to the positive support of each candidate distribution. Since the cardinality bound increases strictly with support size below $`d^2`$, an $`N`$-ray menu with $`d\lt N\leq d^2`$ can attain the stated $`N`$-ray bound only by using every ray, uniformly, in an equiangular tight frame. For $`N\geq d^2`$, it attains $`C_*=1`$ exactly when its rays admit weights forming a projective $`2`$-design, possibly on a smaller subcollection.

The [convex minimax formula](certification.md#fixed-menu-minimax-duality) turns $`\mu_*`$ into a single physical alternative that is hard for every allowed ray. This is why the cardinality bound constrains arbitrary adaptive certification strategies rather than only a chosen weighted survival statistic.

## Consequences and known attaining constructions

Writing $`N=d+k`$ gives

```math
C_*\geq\frac{d(d+k-1)}{(d+1)k}
\qquad(1\leq k\leq d^2-d).
```

For $`k\ll d`$, this is of order $`d/k`$. Adding one ray can change the precision exponent while still leaving a coefficient at least $`d^2/(d+1)`$. Keeping the coefficient bounded by some dimension-independent constant requires $`\Omega(d)`$ additional support rays. Two mutually unbiased bases show that $`O(d)`$ additional rays suffice for a coefficient below $`2`$. Reaching the absolute optimum $`C_*=1`$ is stricter and requires at least $`d^2`$ total rays.

| Ensemble | Support size | Gap $`\mu_S`$ | Coefficient $`C_S`$ |
|---|---:|---:|---:|
| Uniform equiangular tight frame, when it exists | $`N`$ | $`(N-d)/[d(N-1)]`$ | $`d(N-1)/[(d+1)(N-d)]`$ |
| Uniform simplex frame | $`d+1`$ | $`1/d^2`$ | $`d^2/(d+1)`$ |
| Two uniformly sampled mutually unbiased bases | $`2d`$ | $`1/(2d)`$ | $`2d/(d+1)`$ |
| Weighted complex projective $`2`$-design | At least $`d^2`$ | $`1/(d+1)`$ | $`1`$ |

The symmetric-frame constructions and their fidelity coefficients are established in [Mayer–Knill](../references/RELATED_WORK.md#mayer-knill-2018); balanced verification designs and their spectral analysis also appear in [Zhu–Zhang](../references/RELATED_WORK.md#zhu-zhang-2020). Zhu–Zhang's general verification optimization permits unbalanced ensembles, while their explicit balanced formulas concern a special case. The theorem above supplies an unrestricted optimality statement for the linear coefficient and its equality conditions.

Catalogue size and repetitions are distinct. A verifier can draw random labels from a large catalogue without visiting every entry. For example, sampling from two $`d`$-element bases needs only an order-$`\log d`$ classical label description. Preparation and target-measurement complexity remain separate costs. The [certification result](certification.md) concerns the number $`T`$ of fresh channel uses under the stated access model, with fixed $`d`$ and menu in its coefficient limit.
