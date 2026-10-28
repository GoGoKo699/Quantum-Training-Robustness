#!/usr/bin/env python3
"""Regenerate the quantitative figures and compare assets, data and provenance."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE_FILES = [
    'verification/check_math.py', 'science/model.md', 'science/probe_geometry.md',
    'science/product_channels.md', 'science/robustness.md', 'science/certification.md',
]
ASSETS = ['mechanism.pdf', 'certification.pdf']


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def compare(left, right, location: str, rtol: float, atol: float) -> None:
    """Compare scientific values while allowing stated floating-point roundoff."""
    if isinstance(left, dict) and isinstance(right, dict):
        require(left.keys() == right.keys(), f'{location}: dictionary keys changed')
        for key in left:
            compare(left[key], right[key], f'{location}.{key}', rtol, atol)
    elif isinstance(left, list) and isinstance(right, list):
        require(len(left) == len(right), f'{location}: list length changed')
        for index, (a, b) in enumerate(zip(left, right)):
            compare(a, b, f'{location}[{index}]', rtol, atol)
    elif isinstance(left, float) or isinstance(right, float):
        require(isinstance(left, (float, int)) and isinstance(right, (float, int)),
                f'{location}: numerical type changed')
        require(math.isfinite(left) and math.isfinite(right), f'{location}: nonfinite value')
        require(math.isclose(left, right, rel_tol=rtol, abs_tol=atol),
                f'{location}: numerical value changed ({left!r} versus {right!r})')
    else:
        require(type(left) is type(right) and left == right, f'{location}: value changed')


def check_records(stored: dict, fresh: dict, count: int, rtol: float, atol: float) -> None:
    for label, record in [('stored', stored), ('fresh', fresh)]:
        require(record['passed'] == count, f'{label}: wrong numerical check count')
        require(len(record['records']) == count, f'{label}: incomplete check records')
        for item in record['records']:
            require(bool(item.get('name')), f'{label}: unnamed check')
            if 'max_absolute_error' in item:
                error = item['max_absolute_error']
                require(isinstance(error, (float, int)) and math.isfinite(error) and error >= 0,
                        f'{label}: invalid roundoff diagnostic')
    # The generator has already applied each check's own assertion/tolerance.
    # BLAS-dependent residuals diagnose those checks rather than define the data.
    a = [{k: v for k, v in row.items() if k != 'max_absolute_error'} for row in stored['records']]
    b = [{k: v for k, v in row.items() if k != 'max_absolute_error'} for row in fresh['records']]
    compare(a, b, 'checks.records', rtol, atol)


def check(output: Path) -> dict:
    manifest = json.loads((HERE/'manifest.json').read_text())
    stored_dir = HERE/'output'
    stored = json.loads((stored_dir/'plot_data.json').read_text())
    require(manifest['schema_version'] == 1, 'Unsupported figure manifest schema')
    require(set(manifest['assets']) == set(ASSETS), 'Unexpected manifest asset inventory')
    rtol = manifest['data_comparison']['relative_tolerance']
    atol = manifest['data_comparison']['absolute_tolerance']
    for name in ASSETS:
        path = stored_dir/name
        data = path.read_bytes()
        require(data.startswith(b'%PDF-') and data.rstrip().endswith(b'%%EOF'),
                f'{name}: incomplete stored PDF')
        require(digest(path) == manifest['assets'][name], f'{name}: stored asset hash mismatch')
        require(stored['output_sha256'][name] == manifest['assets'][name],
                f'{name}: stored data/asset provenance mismatch')

    fresh_dir = Path(tempfile.mkdtemp(prefix='fresh-', dir=output))
    command = [sys.executable, str(HERE/'generate_plots.py'), '--output-dir', str(fresh_dir)]
    process = subprocess.run(command, cwd=REPO, text=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
    (output/'generation.log').write_text(process.stdout)
    require(process.returncode == 0, f'Generator failed; see {output / "generation.log"}')
    fresh = json.loads((fresh_dir/'plot_data.json').read_text())
    for label, record in [('stored', stored), ('fresh', fresh)]:
        require(record['canonical_sources_sha256'] == {name: digest(REPO/name) for name in SOURCE_FILES},
                f'{label}: canonical source hashes changed; regenerate the stored data')
        require(record['generator_sha256'] == digest(HERE/'generate_plots.py'),
                f'{label}: generator hash mismatch')
        require(record['requirements_sha256'] == digest(HERE/'requirements.txt'),
                f'{label}: requirements hash mismatch')
    for name in ASSETS:
        require((fresh_dir/name).read_bytes() == (stored_dir/name).read_bytes(),
                f'{name}: fresh PDF differs; use the documented pinned plotting environment')
        require(fresh['output_sha256'][name] == manifest['assets'][name],
                f'{name}: fresh provenance hash mismatch')
    compare(stored['data'], fresh['data'], 'data', rtol, atol)
    compare(stored['figure_scope'], fresh['figure_scope'], 'figure_scope', rtol, atol)
    check_records(stored['checks'], fresh['checks'], manifest['expected_numerical_checks'], rtol, atol)
    return {
        'run_status': 'complete', 'passed': True,
        'numerical_checks': fresh['checks']['passed'],
        'pdf_assets_byte_identical': ASSETS,
        'asset_sha256': manifest['assets'],
        'plotted_values_match': True, 'check_records_match': True,
        'canonical_source_hashes_match': True, 'generator_and_requirements_hashes_match': True,
        'data_comparison': manifest['data_comparison'],
        'stored_canonical_revision': stored['canonical_revision'],
        'fresh_canonical_revision': fresh['canonical_revision'],
        'stored_environment': stored['environment'], 'fresh_environment': fresh['environment'],
        'provenance_comparison': 'Git identity and environment are recorded separately from scientific equality.',
        'fresh_output_directory': str(fresh_dir),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=REPO/'review-output/figures',
                        help='Fresh outputs, generation log and result JSON (default: review-output/figures)')
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    result_path = output/'result.json'
    result = {'run_status': 'in_progress', 'passed': False}
    result_path.write_text(json.dumps(result, indent=2)+'\n')
    try:
        result = check(output)
    except Exception as error:
        result = {'run_status': 'complete', 'passed': False,
                  'error': f'{type(error).__name__}: {error}'}
        result_path.write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps(result, indent=2))
        return 1
    result_path.write_text(json.dumps(result, indent=2)+'\n')
    print(f'PASS {result["numerical_checks"]} numerical checks; both figure PDFs reproduce byte for byte')
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
