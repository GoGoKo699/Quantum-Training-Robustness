#!/usr/bin/env python3
"""Generate exact finite-bound figures for Quantum Training Robustness.

Run from the repository root with Python 3.12.14 and the pinned requirements.txt:
  python verification/Graph/generate_plots.py

The repository root is inferred from this script. An explicit --repo remains
available for a relocated copy; --output-dir selects another output directory.

The output data and numerical check record are saved beside the PDFs. The
figures evaluate an explicit channel family and proved finite necessary and
sufficient call bounds.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import importlib.util
from importlib.metadata import version as package_version
import itertools
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter
import numpy as np


BLUE = '#2166AC'
ORANGE = '#C76424'
INK = '#22262B'
ALPHA = 0.05
FIXED_N = 32
FIXED_DELTA = 0.05
CHECKS: list[dict] = []


def require(name: str, condition: bool, **details) -> None:
    if not condition:
        raise AssertionError(f'{name}: {details}')
    CHECKS.append({'name': name, **details})


def close(name: str, actual, expected, *, atol=3e-13, rtol=3e-11) -> None:
    a, b = np.asarray(actual), np.asarray(expected)
    require(name, bool(np.allclose(a, b, atol=atol, rtol=rtol)),
            max_absolute_error=float(np.max(np.abs(a - b))))


def local_values(t):
    """Stable exact formulas for K0=diag(1,s), K1=sqrt(t)[[0,1],[0,1]]."""
    t = np.asarray(t, dtype=float)
    s = np.sqrt(1.0 - 2.0*t)
    one_minus_s = 2.0*t/(1.0+s)
    yplus = (t/(1.0+s))**2
    risk = one_minus_s/3.0+t/6.0
    x = one_minus_s/2.0+t/4.0
    return {'t': t, 's': s, 'yplus': yplus, 'yone': t,
            'risk': risk, 'x': x, 'epsilon2': yplus/2.0,
            'epsilon3': (yplus+t)/3.0}


def factor(n: int) -> float:
    return 1.0/(1.0+2.0**(-int(n)))


def calibration(n: int, delta: float) -> dict:
    """Calibrate the exact independent witness to global Haar risk delta."""
    if n < 1 or not 0.0 < delta <= 1.0/8.0:
        raise ValueError('Require integer n >= 1 and 0 < delta <= 1/8')
    f = factor(n)
    goal = -math.expm1(math.log1p(-delta/f)/n)
    low, high = 0.0, 0.25
    # Monotonicity of x(t) gives a unique solution within this proved interval.
    for _ in range(90):
        mid = (low+high)/2.0
        if float(local_values(mid)['x']) < goal:
            low = mid
        else:
            high = mid
    t = (low+high)/2.0
    values = local_values(t)
    x = float(values['x'])
    y = float(values['yplus'])
    b = -math.expm1(n*math.log1p(-y))
    global_risk = f*(-math.expm1(n*math.log1p(-x)))
    return {'n': n, 'delta': delta, 'factor': f, 't': t,
            'local_entanglement_infidelity': x, 'local_plus_loss': y,
            'b': b, 'global_risk': global_risk}


def finite_bounds(n: int, delta: float, alpha: float = ALPHA) -> dict:
    """Rigorous integer lower bound for two directions and upper for three."""
    if not 0.0 < alpha < 0.5:
        raise ValueError('Require 0 < alpha < 1/2')
    result = calibration(n, delta)
    b = result['b']
    numerator = math.log(1.0/(4.0*alpha*(1.0-alpha)))
    lower_real = numerator/(-math.log1p(-b))
    coefficient = 5.0*factor(n)
    rejection = delta/coefficient
    upper_real = math.log(1.0/alpha)/(-math.log1p(-rejection))
    result.update(alpha=alpha, two_lower_real=lower_real,
                  two_lower_calls=math.ceil(lower_real),
                  three_coefficient=coefficient,
                  three_rejection_lower_bound=rejection,
                  three_upper_real=upper_real,
                  three_upper_calls=math.ceil(upper_real))
    return result


def canonical_module(repo: Path):
    path = repo/'verification/check_math.py'
    spec = importlib.util.spec_from_file_location('qtr_canonical_check_math', path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'Cannot load canonical implementation {path}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_against_canonical(repo: Path) -> None:
    canonical = canonical_module(repo)
    zero = np.array([1, 0], dtype=complex)
    one = np.array([0, 1], dtype=complex)
    plus = (zero+one)/math.sqrt(2.0)
    probes = [zero, plus, one]
    for t in np.geomspace(1e-4, 0.25, 25):
        values = local_values(t)
        kraus = [np.diag([1.0, values['s']]).astype(complex),
                 math.sqrt(t)*np.array([[0, 1], [0, 1]], dtype=complex)]
        close('Kraus trace preservation', sum(k.conj().T@k for k in kraus), np.eye(2))
        errors = canonical.survival_errors(kraus, probes)
        close('Probe losses against canonical matrices', errors,
              [0.0, values['yplus'], t])
        close('Haar risk against canonical Kraus formula', canonical.risk(kraus), values['risk'])
        close('Two-probe equal-weight loss', np.mean(errors[:2]), values['epsilon2'])
        close('Three-probe equal-weight loss', np.mean(errors), values['epsilon3'])
        close('Exact two-probe witness loss-risk relation', values['risk'],
              math.sqrt(2.0*values['epsilon2'])-2.0*values['epsilon2']/3.0)
    close('Optimized three-ray canonical gap',
          np.linalg.eigvalsh(canonical.gap_matrix(probes, [0.3, 0.4, 0.3]))[0], 0.1)

    # Actual small-register Kraus tensors independently check the scalar
    # calibration. Large registers below use only stable scalar identities.
    for n in [1, 2, 4]:
        for delta in [0.001, 0.05, 0.125]:
            calibrated = calibration(n, delta)
            values = local_values(calibrated['t'])
            local = [np.diag([1.0, values['s']]).astype(complex),
                     math.sqrt(calibrated['t'])*np.array([[0, 1], [0, 1]], dtype=complex)]
            kraus = []
            for choices in itertools.product(range(2), repeat=n):
                k = np.array([[1.0]], dtype=complex)
                for choice in choices:
                    k = np.kron(k, local[choice])
                kraus.append(k)
            close('Tensor-Kraus risk calibration', canonical.risk(kraus), delta)
            plus_register = plus
            for _ in range(1, n):
                plus_register = np.kron(plus_register, plus)
            close('Tensor-Kraus all-plus loss',
                  canonical.survival_errors(kraus, [plus_register])[0], calibrated['b'])


def validate_bounds(rows: list[dict]) -> None:
    for row in rows:
        n, delta, alpha, t, b = (row[k] for k in ['n', 'delta', 'alpha', 't', 'b'])
        close('Exact global risk in plotted calibration', row['global_risk'], delta,
              atol=2e-15, rtol=5e-13)
        require('Uniform witness interval',
                delta/n-1e-16 <= t <= 8.0*delta/(3.0*n)+1e-16,
                n=n, delta=delta, t=t)
        require('Proved uniform probe-loss bound', b <= 32.0*delta**2/(9.0*n)+1e-16,
                n=n, delta=delta, b=b)
        require('Three-probe sufficient cap meets confidence',
                row['three_upper_calls']*math.log1p(-row['three_rejection_lower_bound'])
                <= math.log(alpha)+1e-12)
        require('Previous three-probe cap misses this sufficient confidence threshold',
                (row['three_upper_calls']-1)*math.log1p(-row['three_rejection_lower_bound'])
                > math.log(alpha)-1e-12)
        require('Two-direction necessary cap follows fidelity converse',
                row['two_lower_calls'] >= row['two_lower_real'])
        require('Previous two-direction cap violates fidelity necessary condition',
                (row['two_lower_calls']-1)*(-math.log1p(-b))
                < math.log(1.0/(4.0*alpha*(1.0-alpha)))+1e-10)


def style() -> None:
    plt.rcParams.update({
        'font.family': 'serif', 'font.serif': ['STIXGeneral'], 'font.size': 9.5,
        'mathtext.fontset': 'stix', 'axes.labelsize': 10.0,
        'axes.titlesize': 10.0, 'xtick.labelsize': 9.0, 'ytick.labelsize': 9.0,
        'legend.fontsize': 9.5, 'axes.spines.top': False, 'axes.spines.right': False,
        'axes.linewidth': 0.7, 'lines.linewidth': 1.8, 'pdf.fonttype': 42,
        'ps.fonttype': 42, 'savefig.dpi': 220, 'axes.labelcolor': INK,
        'text.color': INK, 'xtick.color': INK, 'ytick.color': INK,
    })


def log_axis(ax) -> None:
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(which='major', color='#E5E7EB', linewidth=0.6)
    ax.tick_params(which='both', direction='out', width=0.65)
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.xaxis.set_major_locator(LogLocator(base=10, numticks=5))
    ax.yaxis.set_major_locator(LogLocator(base=10, numticks=6))
    ax.xaxis.set_minor_locator(LogLocator(base=10, subs=(2, 5), numticks=12))
    ax.yaxis.set_minor_locator(LogLocator(base=10, subs=(2, 5), numticks=12))


def publish(path: Path, data: bytes) -> None:
    """Publish a complete output with one atomic rename."""
    fd, temporary = tempfile.mkstemp(prefix='complete-', suffix='.bin', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def save(fig, path: Path, title: str) -> None:
    metadata = {'Title': title, 'Author': '', 'Creator': 'Python / Matplotlib',
                'CreationDate': None, 'ModDate': None}
    buffer = io.BytesIO()
    fig.savefig(buffer, format='pdf', metadata=metadata)
    publish(path, buffer.getvalue())
    plt.close(fig)


def mechanism(output: Path) -> dict:
    t = np.geomspace(1e-4, 0.25, 400)
    values = local_values(t)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    fig.subplots_adjust(left=0.09, right=0.985, bottom=0.18, top=0.80, wspace=0.34)
    a, b = axes
    for ax in axes:
        log_axis(ax)
    a.plot(t, values['risk'], color=INK, label=r'Haar risk $R$')
    a.plot(t, values['epsilon3'], color=ORANGE, linestyle=(0, (4, 2)),
           label=r'Three-probe loss $\epsilon_3$')
    a.plot(t, values['epsilon2'], color=BLUE, linestyle=(0, (1.2, 1.8)),
           label=r'Two-probe loss $\epsilon_2$')
    a.set(xlim=(1e-4, 0.25), ylim=(6e-10, 0.25),
          xlabel=r'Noise strength $t$', ylabel='Mean loss or risk')
    a.set_title('(b) Hidden dissipative error', loc='left', pad=8)
    b.plot(values['epsilon2'], values['risk'], color=BLUE, linestyle=(0, (1.2, 1.8)),
           label='Two training probes')
    b.plot(values['epsilon3'], values['risk'], color=ORANGE, linestyle=(0, (4, 2)),
           label='Three training probes')
    b.set(xlim=(8e-10, 0.13), ylim=(3e-5, 0.25),
          xlabel=r'Mean training loss $\epsilon$', ylabel=r'Haar risk $R$')
    b.set_title('(c) Risk versus training loss', loc='left', pad=8)
    handles, labels = a.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.53, 1.005),
               ncols=3, frameon=False, columnspacing=1.1, handlelength=2.2,
               fontsize=9.5)
    save(fig, output/'mechanism.pdf', 'Exact dissipative qubit witness')
    return {k: np.asarray(v).tolist() for k, v in values.items()}


def certification(output: Path) -> dict:
    deltas = np.geomspace(0.001, 0.125, 260)
    sizes = sorted(set(np.rint(np.geomspace(1, 256, 110)).astype(int).tolist()))
    precision = [finite_bounds(FIXED_N, float(delta)) for delta in deltas]
    registers = [finite_bounds(int(n), FIXED_DELTA) for n in sizes]
    validate_bounds(precision+registers)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    fig.subplots_adjust(left=0.09, right=0.985, bottom=0.18, top=0.80, wspace=0.34)
    for ax in axes:
        log_axis(ax)
    for ax, rows, xname in [(axes[0], precision, 'delta'), (axes[1], registers, 'n')]:
        xs = [r[xname] for r in rows]
        ax.plot(xs, [r['two_lower_calls'] for r in rows], color=BLUE,
                linestyle=(0, (4, 2)), label='Two directions: lower bound')
        ax.plot(xs, [r['three_upper_calls'] for r in rows], color=ORANGE,
                label='Three probes: upper bound')
        ax.set_ylabel(r'Global repetitions $T$')
    axes[0].set(xlim=(0.001, 0.125), xlabel=r'Risk threshold $\delta$')
    axes[0].set_title(r'(a) Precision, $n=32$', loc='left', pad=8)
    axes[1].set(xlim=(1, 320), xlabel=r'Independent qubits $n$')
    axes[1].set_xticks([1, 4, 16, 64, 256], labels=['1', '4', '16', '64', '256'])
    axes[1].set_title(r'(b) Register size, $\delta=0.05$', loc='left', pad=8)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.53, 1.005),
               ncols=2, frameon=False, columnspacing=1.4, handlelength=2.5,
               fontsize=9.5)
    save(fig, output/'certification.pdf', 'Finite certification bounds for independent qubit channels')
    return {'alpha': ALPHA, 'precision_panel_n': FIXED_N,
            'register_panel_delta': FIXED_DELTA,
            'precision_panel': precision, 'register_panel': registers}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2],
                        help='Canonical repository root (default: inferred from this script)')
    parser.add_argument('--output-dir', type=Path,
                        default=Path(__file__).resolve().parent/'output')
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    check_against_canonical(repo)
    style()
    data = {'mechanism': mechanism(output), 'certification': certification(output)}
    files = ['verification/check_math.py', 'science/model.md',
             'science/probe_geometry.md', 'science/product_channels.md',
             'science/robustness.md', 'science/certification.md']
    # Git identity records where the run happened; source hashes identify the
    # mathematical inputs. Source archives without Git metadata remain usable.
    try:
        top = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', '--show-toplevel'],
                                      text=True, stderr=subprocess.DEVNULL).strip()
        revision = (subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'],
                                           text=True, stderr=subprocess.DEVNULL).strip()
                    if Path(top).resolve() == repo else None)
    except (OSError, subprocess.CalledProcessError):
        revision = None
    provenance = {
        'canonical_repository': 'GoGoKo699/Quantum-Training-Robustness',
        'canonical_revision': revision,
        'canonical_sources_sha256': {f: sha256(repo/f) for f in files},
        'generator_sha256': sha256(Path(__file__)),
        'requirements_sha256': sha256(Path(__file__).resolve().with_name('requirements.txt')),
        'environment': {'python': platform.python_version(),
                        'numpy': np.__version__, 'matplotlib': matplotlib.__version__,
                        'resolved_plot_dependencies': {
                            name: package_version(name) for name in [
                                'contourpy', 'cycler', 'fonttools', 'kiwisolver',
                                'packaging', 'pillow', 'pyparsing', 'python-dateutil', 'six']}},
        'figure_scope': {
            'mechanism': 'Exact explicit-channel curves with uniform weights on {0,+} or {0,+,1}.',
            'certification': 'Two-direction necessary fidelity bound and a sufficient survival-test cap using three global inputs with optimized weights.',
            'access': 'Fresh classical input labels, inaccessible environment, arbitrary quantum output memory, exact independent local channels, ideal target projectors.',
            'valid_range': 'Integer n>=1, 0<delta<=1/8, 0<alpha<1/2.',
            'three_probe_weights': [0.3, 0.4, 0.3],
            'resource': 'T full n-qubit global examples; each invokes n local channels.'},
        'checks': {'passed': len(CHECKS), 'records': CHECKS},
        'output_sha256': {p.name: sha256(p) for p in sorted(output.glob('*.pdf'))},
        'data': data,
    }
    publish(output/'plot_data.json', (json.dumps(provenance, indent=2, allow_nan=False)+'\n').encode())
    print(f'PASS {len(CHECKS)} numerical checks; generated mechanism.pdf and certification.pdf')
    print(json.dumps(provenance['output_sha256'], indent=2))


if __name__ == '__main__':
    main()
