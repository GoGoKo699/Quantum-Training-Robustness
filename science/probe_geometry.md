# Probe geometry and explicit channel witnesses

The robustness criterion can be checked by linear algebra on the input vectors. A basis extracted from the probe set reveals which coordinate directions an additional probe connects. This yields exact examples where one extra ray changes the loss exponent, and it also separates that qualitative repair from the numerical size of the robustness coefficient.

Throughout, $`d\geq2`$, all probe weights are positive, and $`Q_S`$, $`\mu_S`$, and $`R`$ have the definitions in [robustness](robustness.md). The number of distinct rays is $`N`$. Experimental repetitions are counted separately in [certification](certification.md).

## A coordinate-support criterion

Assume the probes span $`\mathbb C^d`$. Select a basis $`b_1,\ldots,b_d`$ from them, form the invertible matrix $`B=[b_1\ \cdots\ b_d]`$, and expand every remaining probe as

```math
\psi_i=\sum_{j=1}^d c_{ij}b_j.
```

Construct a graph with vertices $`1,\ldots,d`$. Join $`j`$ and $`k`$ if some extra probe has both $`c_{ij}\neq0`$ and $`c_{ik}\neq0`$. Call this the **coordinate-support graph**.

**Proposition 1.** If this graph has $`m`$ connected components, then

```math
\mathcal A_S
=\left\{B\operatorname{diag}(\lambda_1,\ldots,\lambda_d)B^{-1}:
\lambda_j\text{ is constant on each component}\right\},
\qquad
\dim_{\mathbb C}\mathcal A_S=m.
```

In particular, $`\mu_S>0`$ if and only if the coordinate-support graph is connected.

**Proof.** Every common right-eigenoperator is diagonal in the selected basis, so it has the form displayed above. If it also has $`\psi_i`$ as an eigenvector with eigenvalue $`\lambda_i'`$, comparison of the unique basis coordinates gives

```math
(\lambda_j-\lambda_i')c_{ij}=0\qquad\text{for every }j.
```

Its diagonal eigenvalues must therefore coincide on the support of each extra probe, and hence on every graph component. Conversely, if the eigenvalues are constant on each component, the support of each extra probe lies within one component, so that probe is an eigenvector. Choosing one arbitrary complex eigenvalue per component proves the dimension formula.

Although the graph depends on the selected basis, the dimension it computes does not. An invariant formulation is that $`\mu_S>0`$ exactly when there is no nontrivial direct-sum decomposition

```math
\mathbb C^d=V_1\oplus\cdots\oplus V_m,\qquad m\geq2,
```

with every probe ray contained in one summand. A disconnected coordinate-support graph gives such summands by grouping basis vectors. Conversely, projections onto the summands of such a decomposition are nonscalar common right-eigenoperators. The summands need not be orthogonal, and their projections need not be Hermitian. This is a standard geometric description of an indecomposable vector configuration; the graph terminology itself is not a new mathematical ingredient.

### The two connectivity conditions

Two graphs enter the theory for different purposes.

| Graph | Vertices and edges | Property it detects |
|---|---|---|
| Overlap graph | Probe rays; a nonzero inner product gives an edge | With spanning, exact identification of the unitary target |
| Coordinate-support graph | Selected basis vectors; simultaneous nonzero coordinates in an extra probe give an edge | A scalar common right-eigenoperator space and linear robustness |

The first property is the known [Mayer–Knill identification theorem](../references/RELATED_WORK.md#mayer-knill-2018), also used in [Li et al.](../references/RELATED_WORK.md#li-et-al-2021). The second follows directly from Proposition 1 and the sharp robustness theorem.

Exactly $`d`$ independent rays form a basis with no extra probes. Their coordinate-support graph has $`d`$ isolated vertices and their common right-eigenoperator space has dimension $`d`$. If their overlap graph is connected, they identify the target exactly but lie in the square-root regime for arbitrary CPTP alternatives.

Adding a single ray whose $`d`$ basis coordinates are all nonzero makes the coordinate-support graph connected. More general added rays suffice whenever their supports connect all basis indices. This proves the qualitative $`d`$ versus $`d+1`$ repair without any assumption that the basis is orthogonal.

## An exact qubit example

Take the equally weighted two-ray ensemble

```math
S_2=\{|0\rangle,|+\rangle\},\qquad
|+\rangle=\frac{|0\rangle+|1\rangle}{\sqrt2}.
```

Its rays are independent and have nonzero overlap, so they identify the target. Define

```math
L=\begin{pmatrix}0&1\\0&1\end{pmatrix},
\qquad
K_0=\begin{pmatrix}1&0\\0&r\end{pmatrix},
\qquad
K_1=\sqrt t\,L,
\qquad
r=\sqrt{1-2t},\quad0\leq t\leq\frac12.
```

The matrix $`L`$ has both probes as right eigenvectors. The operators satisfy $`K_0^\dagger K_0+K_1^\dagger K_1=I`$ exactly. Their individual survival infidelities are

```math
e_0=0,
\qquad
e_+=\frac{(1-r)^2}{4},
\qquad
e_1=t.
```

For the two-ray ensemble,

```math
\epsilon_{S_2}=\frac{(1-r)^2}{8},
\qquad
R=\frac{1-r}{3}+\frac t6
=\sqrt{2\epsilon_{S_2}}-\frac23\epsilon_{S_2}.
```

This is an exact curve over the full displayed parameter interval. In particular, small training infidelity can hide a Haar risk proportional to its square root.

### Computing the gaps

Use the orthonormal complex operator basis $`(\sigma_x,\sigma_y,\sigma_z)/\sqrt2`$ for traceless qubit matrices. In this basis the matrix representing $`Q_{S_2}`$ is

```math
\frac14
\begin{pmatrix}
1&i&0\\
-i&2&i\\
0&-i&1
\end{pmatrix},
\qquad
\operatorname{spec}(Q_{S_2})=\left\{0,\frac14,\frac34\right\}.
```

The imaginary off-diagonal entries matter: restricting the minimization to Hermitian matrices would miss the zero direction.

Add $`|1\rangle`$ and use equal weights on the three rays. The corresponding matrix is

```math
\frac16
\begin{pmatrix}
2&0&0\\
0&3&i\\
0&-i&1
\end{pmatrix},
\qquad
\operatorname{spec}(Q_{S_3})
=\left\{\frac{2-\sqrt2}{6},\frac13,
\frac{2+\sqrt2}{6}\right\}.
```

Thus the exact optimal global linear coefficient for the uniform three-ray ensemble is

```math
\mu_{S_3}=\frac{2-\sqrt2}{6},
\qquad
R\leq(2+\sqrt2)\epsilon_{S_3}.
```

The earlier channel now has a first-order loss on the added ray, $`e_1=t`$. The improvement is caused by the added geometric constraint. It does not require the new ray to have greater superposition than the old ones.

For comparison, the two-ray commutator gap is $`\gamma_{S_2}=1/4`$. Every unital alternative already obeys the sharp inequality $`R\leq4\epsilon_{S_2}/3`$. The nonunital witness and this unital baseline are analyzed in [nonunitality](nonunitality.md).

## A minimal identifying family in arbitrary dimension

Let

```math
u=\frac1{\sqrt d}\sum_{j=0}^{d-1}|j\rangle,
\qquad
S_-=\{|1\rangle,\ldots,|d-1\rangle,u\}.
```

These $`d`$ rays form a basis. The overlap graph is a star centered at $`u`$, so the family identifies the target exactly. It nevertheless has $`\mu_{S_-}=0`$.

Choose

```math
L=\sqrt d\,|u\rangle\langle0|,
\qquad
K_1=\sqrt t\,L,
\qquad
K_0=I+\left(\sqrt{1-dt}-1\right)|0\rangle\langle0|,
\qquad
0\leq t\leq\frac1d.
```

The computational probes have eigenvalue zero under $`L`$, while $`Lu=u`$. Since $`L^\dagger L=d|0\rangle\langle0|`$, this is the exact two-Kraus construction of the robustness theorem.

Put $`h=1-\sqrt{1-dt}`$ and let $`b`$ denote the sampling weight on $`u`$. Each computational probe in $`S_-`$ is unchanged, while

```math
e_u=\frac{d-1}{d^2}h^2,
\qquad
\epsilon_{S_-}=\frac{b(d-1)}{d^2}h^2.
```

The traces of the two Kraus operators are $`d-h`$ and $`\sqrt t`$. Substitution into the exact Haar-risk identity gives

```math
\begin{aligned}
R
&=\frac{2(d-1)}{d^2}h
 -\frac{d-1}{d^2(d+1)}h^2\\
&=\frac{2\sqrt{d-1}}{d\sqrt b}\sqrt{\epsilon_{S_-}}
 -\frac{\epsilon_{S_-}}{b(d+1)}.
\end{aligned}
```

For uniform weights, $`b=1/d`$, this becomes

```math
R=2\sqrt{\frac{d-1}{d}}\sqrt{\epsilon_{S_-}}
-\frac{d}{d+1}\epsilon_{S_-}.
```

Adding the missing ray $`|0\rangle`$ detects this channel at first order, because $`e_0=(d-1)t`$. Together with $`u`$ and the full computational basis, it also makes the common right-eigenoperator space scalar for every channel direction.

This particular witness has a dimension-dependent range. Under uniform weights its maximum training loss is $`(d-1)/d^3`$, and its maximum Haar risk is

```math
R_{\max,\mathrm{witness}}
=\frac{(d-1)(2d+1)}{d^2(d+1)}=O(d^{-1}).
```

The formula establishes a sharp small-error exponent for each fixed dimension. The system-size result at fixed global accuracy instead uses the independent-channel construction in [product channels](product_channels.md).

## The full basis plus one uniform ray

Consider $`S_+=\{|0\rangle,\ldots,|d-1\rangle,u\}`$. Give each basis ray weight $`a=(1-b)/d`$ and the uniform ray weight $`b`$, with $`0<b<1`$. The basis-plus-superposition family is an established gate-characterization construction; see the discussion and references in [Mayer–Knill](../references/RELATED_WORK.md#mayer-knill-2018). The calculation here determines its full variance spectrum and optimal sampling weights.

Let $`\Pi_{\mathrm{off}}`$ be the Hilbert–Schmidt orthogonal projection onto matrices whose computational-basis diagonal vanishes, and let

```math
\mathcal R_u(A)=(I-|u\rangle\langle u|)A|u\rangle\langle u|.
```

The map $`\mathcal R_u`$ is the orthogonal projection onto the $`d-1`$ dimensional matrix space $`\{|v\rangle\langle u|:v\perp u\}`$. The operator representing the quadratic form is

```math
Q_{S_+}=a\Pi_{\mathrm{off}}+b\mathcal R_u.
```

### Spectrum

Choose an orthonormal basis $`v_1,\ldots,v_{d-1}`$ of $`u^\perp`$. For each $`q_j=|v_j\rangle\langle u|`$, its diagonal and off-diagonal components have squared norms $`1/d`$ and $`(d-1)/d`$. After normalizing those two components, their plane carries the matrix

```math
\begin{pmatrix}
b/d&b\sqrt{d-1}/d\\
b\sqrt{d-1}/d&a+b(d-1)/d
\end{pmatrix}.
```

Different $`v_j`$ give orthogonal planes. The two eigenvalues of each plane are

```math
\lambda_\pm
=\frac{a+b\pm\sqrt{(a+b)^2-4ab/d}}{2}.
```

The off-diagonal space orthogonal to these planes has dimension $`(d-1)^2`$ and eigenvalue $`a`$. The remaining direction is the identity and has eigenvalue zero. The complete spectrum is therefore

| Eigenvalue | Multiplicity |
|---|---:|
| $`0`$ | $`1`$ |
| $`a`$ | $`(d-1)^2`$ |
| $`\lambda_-`$ | $`d-1`$ |
| $`\lambda_+`$ | $`d-1`$ |

For positive $`a,b`$, $`\lambda_-<a`$, so $`\mu_{S_+}=\lambda_-`$. At uniform weights, $`a=b=1/(d+1)`$,

```math
\mu_{S_+}
=\frac{1-\sqrt{1-1/d}}{d+1},
\qquad
C_{S_+}=d+\sqrt{d(d-1)}.
```

### Optimizing all sampling weights

The gap is a concave function of the weights, because it is a minimum of linear functions of those weights. Permuting the computational basis preserves the ray $`u`$ and acts unitarily on the matrix space. Averaging any choice of basis weights over these permutations cannot decrease the gap. It is therefore sufficient to optimize the single parameter $`b`$ above; this reduction also covers competitors with unequal original basis weights.

The smaller eigenvalue satisfies

```math
\mu^2-\frac{1+(d-1)b}{d}\mu+\frac{b(1-b)}{d^2}=0.
```

It vanishes at both endpoints. At an interior stationary point, differentiation gives

```math
\mu=\frac{1-2b}{d(d-1)}.
```

Substitution into the quadratic equation, with the smaller eigenvalue selected, yields

```math
\boxed{
b_*=\frac{1+\sqrt{d-1}}{d+1+2\sqrt{d-1}},
\qquad
\mu_*=\frac{1}{d[d+1+2\sqrt{d-1}]},
\qquad
C_*=\frac{d[d+1+2\sqrt{d-1}]}{d+1}.
}
```

Concavity makes this stationary value globally optimal for this fixed menu. For a qubit, the optimal weights on $`(|0\rangle,|+\rangle,|1\rangle)`$ are $`(3/10,4/10,3/10)`$, giving $`\mu_*=1/10`$ and $`C_*=10/3`$.

The optimized coefficient is asymptotic to $`d+2\sqrt d`$, whereas the uniform coefficient is asymptotic to $`2d`$. Thus the exponent repair does not by itself give a coefficient independent of dimension. The known $`d+1`$-ray simplex has $`C=d^2/(d+1)`$; the ratio of this menu's optimized coefficient to that simplex coefficient is $`1+(1+2\sqrt{d-1})/d`$. [Optimal design](optimal_design.md) proves the universal support bound and credits the known symmetric constructions.

## Preparation and sampling resources

When $`d=2^n`$, the computational probes and $`u=|+\rangle^{\otimes n}`$ are product states with $`O(n)`$ elementary preparation gates. The support of $`S_-`$ or $`S_+`$ still has order $`2^n`$ rays. Simple preparation of each ray does not turn an exponential support into a constant support.

Simple product preparation is also available for the known simplex and for two mutually unbiased product bases; [Mayer–Knill](../references/RELATED_WORK.md#mayer-knill-2018) explicitly gives the simplex preparation. No exclusive preparation advantage is claimed for the basis-plus-uniform menu.

A randomized protocol can sample a ray from a catalogue without visiting every entry. The size of the catalogue, the cost of generating its classical index, the cost of preparing one ray, and the number of fresh output samples are separate resources. The results here concern the catalogue geometry and its loss coefficient. Their operational sample consequences are proved in [certification](certification.md).
