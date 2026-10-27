#!/usr/bin/env python3
"""Verify the stored report pair, optionally compiling it in a new directory."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def check_pdf(path: Path, manifest: dict) -> None:
    require(sha256(path) == manifest['pdf_sha256'], f'PDF hash mismatch: {path}')
    reader = PdfReader(path)
    require(len(reader.pages) == manifest['pages'], 'Unexpected report page count')
    metadata = reader.metadata or {}
    require(not metadata.get('/Author'), 'Report PDF has author metadata')
    require(not metadata.get('/CreationDate') and not metadata.get('/ModDate'),
            'Report PDF has date metadata')


def check_stored(root: Path) -> dict:
    manifest = json.loads((root / 'verification/report-manifest.json').read_text())
    source = root / manifest['source']
    require(sha256(source) == manifest['source_sha256'], 'Report source hash mismatch')
    check_pdf(root / manifest['pdf'], manifest)
    return manifest


def build_report(root: Path, manifest: dict, engine: str, output: Path) -> dict:
    executable = shutil.which(engine)
    require(executable is not None, f'Compiler not found: {engine}')
    version = subprocess.check_output([executable, '--version'], text=True).splitlines()[0]
    require(version == manifest['engine'], f'Wrong compiler: {version}')
    # Every invocation gets an empty directory: a stored PDF or old log cannot pass.
    output.mkdir(parents=True, exist_ok=True)
    build = Path(tempfile.mkdtemp(prefix='fresh-', dir=output.resolve()))
    source = root / manifest['source']
    shutil.copyfile(source, build / source.name)
    for index in range(1, 4):
        with (build / f'pass-{index}.txt').open('w') as stream:
            subprocess.run(
                [executable, '-no-shell-escape', '-interaction=nonstopmode',
                 '-halt-on-error', '-file-line-error', source.name],
                cwd=build, stdout=stream, stderr=subprocess.STDOUT, check=True,
                timeout=120,
            )
    fresh = build / source.with_suffix('.pdf').name
    log_path = build / source.with_suffix('.log').name
    require(fresh.is_file() and log_path.is_file(), 'Missing fresh PDF or final log')
    log = log_path.read_text(errors='replace')
    require('TeX Live 2025' in log.splitlines()[0], 'Wrong engine in fresh log')
    require(re.search(rf'Output written on {re.escape(fresh.name)} '
                      rf'\({manifest["pages"]} pages,', log) is not None,
            'Final log does not describe the fresh report')
    # PGF loads epstopdf, but this document has no EPS inputs or shell commands.
    checked_log = log.replace('Package epstopdf Warning: Shell escape feature is not enabled.', '')
    require(re.search(r'Overfull|Underfull|Missing character:|LaTeX Warning:|'
                      r'Package \S+ Warning:|^!', checked_log, re.MULTILINE) is None,
            'Fresh report has layout, glyph, reference, or package warnings')
    check_pdf(fresh, manifest)
    return {'engine': version, 'build_directory': str(build),
            'fresh_pdf_sha256': sha256(fresh), 'final_log': str(log_path),
            'byte_identical': True}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true', help='Require a fresh three-pass build')
    parser.add_argument('--engine', default='pdflatex', help='pdfLaTeX executable (TeX Live 2025)')
    parser.add_argument('--output-dir', type=Path, default=Path('review-output/report'))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result = {'passed': False, 'run_status': 'in_progress',
              'mode': 'fresh build' if args.build else 'stored artifacts only'}
    result_path = args.output_dir / 'result.json'
    # Invalidate an earlier success before any validation or compiler startup.
    result_path.write_text(json.dumps(result, indent=2) + '\n')
    try:
        manifest = check_stored(ROOT)
        result.update(source_sha256=manifest['source_sha256'], pdf_sha256=manifest['pdf_sha256'],
                      pages=manifest['pages'])
        if args.build:
            result.update(build_report(ROOT, manifest, args.engine, args.output_dir))
        result['passed'] = True
        result['run_status'] = 'complete'
    except Exception as error:
        result['error'] = str(error)
        result['run_status'] = 'failed'
        raise
    finally:
        result_path.write_text(json.dumps(result, indent=2) + '\n')
    print('PASS fresh three-pass report build; PDF byte-identical to stored report'
          if args.build else 'PASS stored report pair; no compilation performed')


if __name__ == '__main__':
    main()
