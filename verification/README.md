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

Similarly, the product examples evaluate selected points within the proved range. The entire interval $`0\lt \delta\le1/8`$, the lower bound for every mixed tensor string, and the validity of the product inequality for all permitted coordinates follow from the analytical arguments in [Product channels](../science/product_channels.md). The script does not simulate adaptive quantum verifiers or establish their optimality by enumeration. Those statements use the fidelity converse and minimax proof in [Certification](../science/certification.md).

The checks are numerical corroboration of the explicit mathematical constructions. They do not measure hardware performance, characterize unknown preparation or readout errors, or establish a literature-priority claim.

## Navigation and learning-map checks

The standard-library [source checker](check_structure.py) validates relative links and their anchors, mathematical fences and grouping braces, the ordered M01–M30 map, its five required fields per milestone, and backward dependencies. It also checks the 13/17 phase allocation and the selected anchor in the reading entrypoints.

Two additional guards address failures observed in this repository's actual GitHub rendering: raw less-than signs inside mathematical expressions and the `\operatorname` macro. The repaired notation uses `\lt` and upright operator labels with explicit spacing. The guards apply only to math, not to HTML anchors, links, program code, or a general TeX document.

```bash
python3 verification/check_structure.py
python3 verification/test_review.py -v
```

The [regression fixtures](test_review.py) check the source guards, committed-source provenance, complete-versus-partial capture reports, startup failure, and error-message handling. Without the optional browser, 23 source/capture-report tests run and three DOM fixtures are explicitly skipped. With Chromium installed, run all 26:

```bash
QTR_BROWSER_TESTS=1 python3 verification/test_review.py -v
```

The browser fixtures include a GitHub macro-error box beside a successfully rendered expression and an error inside an open shadow root. A page must not pass merely because another equation rendered successfully.

Printed counts refer to the checked tree. These tests do not establish that the prose teaches the intended concepts, that the equations are true, or that GitHub has rendered the current public pages correctly. Those require semantic and visual review.

## Explanatory report

The [report PDF](../learning/report/Quantum_Training_Robustness_Report.pdf) is paired with its self-contained [LaTeX source](../learning/source/Quantum_Training_Robustness_Report.tex). Figures and analytic curves are inline TikZ/PGFPlots. The [manifest](report-manifest.json) records the reviewed source/PDF hashes, 30-page length, and actual pdfLaTeX engine. It must be updated together with both artifacts after a reviewed report revision.

Install the separate [PDF-check dependency](requirements-report.txt), then check the stored pair:

```bash
python3 -m pip install -r verification/requirements-report.txt
python3 verification/check_report.py
python3 verification/test_report.py -v
```

This verifies hashes, page count, and empty author/date metadata. It performs no compilation. The negative fixtures verify that changed source, a failing compiler, or missing fresh output cannot pass because a stored PDF exists.

To require a fresh build, use **pdfLaTeX 1.40.28 from TeX Live 2025**:

```bash
python3 verification/check_report.py --build --engine /path/to/texlive2025/bin/x86_64-linux/pdflatex
```

The checker copies the source into a new directory under `review-output/report/`, compiles three times without shell escape, and requires both the fresh PDF and its corresponding final log. It rejects layout, glyph, reference, and package warnings, except the optional epstopdf shell-escape notice: this report has no EPS inputs. The fresh PDF must be byte-identical to the stored PDF. A failed build is a failed check; an existing PDF cannot replace missing fresh output. The result JSON is marked incomplete before checking starts; success requires `run_status: complete` and `passed: true`. Per-pass output and the final log remain beside it for inspection.

Use the frozen final TeX Live 2025 distribution for reproduction; another TeX Live release or updated package set may produce different bytes. The [CI installer](install_report_tex.sh) verifies the frozen installer and package-database checksums before installing the required packages. To install into a new local directory and build:

```bash
bash verification/install_report_tex.sh "$PWD/../report-texlive2025"
python3 verification/check_report.py --build --engine "$PWD/../report-texlive2025/bin/x86_64-linux/pdflatex"
```

Keep the toolchain outside the tracked source. The build is a source/output integrity check, not a proof check. The topic pages retain attribution and authoritative scientific statements. Two report symbols differ from the topic pages: `h(z)` is the scalar aggregation called `F(z)` in the product-channel proof, and `rho_S` is the mean state called `overline rho` in the nonunitality proof.

## Actual hosted mathematical rendering

The optional [capture script](capture_hosted.py) opens every Markdown page containing mathematics at the full SHA of the checked-out commit. This includes the README, both learning pages, all scientific pages, related work, and this verification guide. Before capture, it derives the Markdown inventory from that commit and verifies every local document against its committed blob. Changed, missing, or added Markdown sources require a new committed revision. It saves full-page screenshots, hosted HTML and text, heading coordinates, source blob hashes, and a JSON report. It does not render local Markdown as a substitute for the hosted page.

The report is initialized before source validation or browser startup and records the full planned page manifest before capture. It remains marked `in_progress` if execution is interrupted. A completed report is checked against the entire manifest, including each page's source hash and expression count; success requires `run_status: complete` and `passed: true`. A successful subset of pages cannot establish a successful run. A newly started run replaces any previous report in the output directory.

For each page, the expected expression count is obtained from the checked source. Every expression must have a successful mathematical host. The scan traverses open shadow roots, detects GitHub macro-error boxes and other known renderer errors, and rejects incomplete or mismatched counts. It records horizontal overflow for visual inspection rather than treating a legitimate scrollable display as an automatic failure.

```bash
python3 -m pip install -r verification/requirements-browser.txt
python3 -m playwright install --with-deps chromium
python3 verification/capture_hosted.py --ref "$(git rev-parse HEAD)"
```

The optional [browser dependency](requirements-browser.txt) is separate from the numerical suite. A network failure or an unrecognized renderer is a failed or incomplete capture, not evidence of a clean page. Successful capture still requires visual inspection of screenshots for clipping, table collisions, notation, and layout. The recorded viewport is 1440 by 1100 pixels; this is not a claim about every browser or screen size.

The [repository audit workflow](../.github/workflows/sanity.yml) uses pinned action revisions, read-only contents permission, and no secrets. It runs on manual dispatch and on relevant source, documentation, report PDF/TeX, or verification changes to `main` or verification branches. Its explicit Bash configuration propagates failures through logged pipelines. The source/browser job has a 15-minute cap; the separate fresh-report job has a 20-minute cap and records its fresh PDF and final log. Artifacts contain only checked public sources, test/build output, and rendering diagnostics; they are retained for seven days. Workflow success is not a proof certificate or an automatic release action.
