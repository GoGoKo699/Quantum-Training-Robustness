# Table I and companion plots

The Python generator evaluates the explicit dissipative qubit channel and finite certification bounds developed in the scientific account. Its `finite_bounds` routine reproduces Table I of the manuscript, as shown [below](#reproduce-the-manuscript-table). The manuscript contains no figures. The two PDF assets remain available as companion illustrations of the exact formulas and finite bounds, with their existing panel labels, 7-by-3-inch geometry, and serif typography.

| Asset | Scientific content |
|---|---|
| [mechanism.pdf](output/mechanism.pdf) | Exact Haar risk and uniform two-probe or three-probe loss as the channel parameter varies; the same family plotted as risk versus training loss. The companion asset retains panel labels (b) and (c). |
| [certification.pdf](output/certification.pdf) | A necessary two-direction repetition bound and an attainable three-probe cap, compared against precision and independent-register size. |
| [plot_data.json](output/plot_data.json) | All plotted values, numerical check records, source hashes, plotting environment, and output hashes. |

The formulas and hypotheses are proved in [Probe geometry](../../science/probe_geometry.md), [Certification](../../science/certification.md), and [Product channels](../../science/product_channels.md). [Model](../../science/model.md) fixes the risk and loss conventions. The generator also evaluates its formulas against the direct Kraus calculations in [check_math.py](../check_math.py), including actual tensor-product channels for one, two, and four qubits.

## Regenerate

The recorded environment is Python 3.12.14 with the complete plotting dependencies pinned in [requirements.txt](requirements.txt). Run from the repository root:

```bash
python3 -m pip install -r verification/Graph/requirements.txt
python3 verification/Graph/generate_plots.py
```

The repository and default `output/` paths are derived from the script location, so an absolute invocation also works from another current directory. `--output-dir PATH` selects a fresh destination. A relocated figure folder can use `--repo PATH` to identify its scientific sources; keep the generator and its dependency file together.

The generator completes **2,479 checks**, then writes both PDFs and their data atomically. The output depends on the stated formulas and pinned plotting stack; no TeX installation is required. PDF author and date metadata are empty.

## Verify a fresh run

Use a review directory separate from the tracked figure assets:

```bash
python3 verification/Graph/check_figures.py --output-dir /tmp/qtr-figure-review
```

The checker requires complete stored PDFs with the accepted hashes in [manifest.json](manifest.json), regenerates into a new directory, and compares both fresh PDFs byte for byte. It compares the underlying scientific values with relative tolerance `5e-13` and absolute tolerance `2e-15`, verifies the 2,479 check records, and checks source, generator, and dependency-file hashes. Floating-point residual diagnostics can vary with numerical libraries; each new generation applies the original assertions before comparison.

The recorded Git revision and environment describe each run. They are kept separate from scientific equality, so an unrelated documentation commit does not change the accepted figures. Source or generator edits require regeneration of the stored data; a changed plot requires a deliberate update of the accepted asset hashes after review. The review directory contains a generation log, fresh outputs, and `result.json`; a failed or interrupted run cannot inherit a completed success result.

## Reading the bounds

The mechanism curves evaluate one physical channel family with equal probe weights. The two-input mean loss is quadratic near zero, while the risk and three-input loss are linear.

The certification curves use decision error `alpha = 0.05`. The precision panel fixes `n = 32`; the register panel fixes `delta = 0.05`. Calibration checks cover the plotted range within `0 < delta <= 1/8`. The three-probe weights are `(3/10, 2/5, 3/10)`.

Here `T` counts whole-register repetitions. Each repetition invokes all `n` local channels, so the total local channel count is `nT`. The product-channel result assumes a product-unitary target, exact independent qubit channels, fresh classically selected inputs, system outputs, and ideal target-output projectors. The lower bound permits retained quantum output memory and collective readout.

## Reproduce the manuscript table

Table I of *Probe Geometry and the Cost of Quantum Gate Certification* uses `finite_bounds` at the five parameter pairs below. Run this from the repository root with the dependencies installed as above. Each row prints `n`, `delta`, a necessary call count for two directions, and a sufficient call count for three probes.

```bash
PYTHONPATH=verification/Graph python3 - <<'PY'
from generate_plots import finite_bounds

for n, delta in [(8, 0.05), (32, 0.05), (128, 0.05), (32, 0.10), (32, 0.025)]:
    bounds = finite_bounds(n, delta, alpha=0.05)
    print(n, f"{delta:g}", bounds["two_lower_calls"], bounds["three_upper_calls"])
PY
```

Expected output at `alpha = 0.05`:

```text
8 0.05 11312 297
32 0.05 45489 299
128 0.05 181831 299
32 0.1 10792 149
32 0.025 186626 598
```

These are a necessary count for the two-direction menu and a sufficient count for the three-probe menu at the stated finite parameters. Theorem 4 establishes the uniform repetition orders and, at fixed `n`, the joint limiting coefficient; the two columns are not claims of exact finite-parameter optimum counts.
