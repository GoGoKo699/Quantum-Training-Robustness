# Quantitative figures

The Python generator evaluates the explicit dissipative qubit channel and finite certification bounds developed in the scientific account. The two PDF assets retain their accepted labels, 7-by-3-inch geometry, and serif typography.

| Asset | Scientific content |
|---|---|
| [mechanism.pdf](output/mechanism.pdf) | Exact Haar risk and uniform two-probe or three-probe loss as the channel parameter varies; the same family plotted as risk versus training loss. The asset uses panel labels (b) and (c), allowing it to accompany a separate schematic. |
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

Here `T` counts whole-register repetitions. Each repetition invokes all `n` local channels, so the total local channel count is `nT`. The product-channel result assumes exact independent qubit channels, fresh classically selected inputs, system outputs, and ideal target-output projectors. The lower bound permits retained quantum output memory and collective readout.
