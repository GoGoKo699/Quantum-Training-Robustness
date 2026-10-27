#!/usr/bin/env python3
"""Negative fixtures for report provenance and fresh-build verification.

Run with ``python3 verification/test_report.py -v``. The stored report is
copied to temporary directories; compiler discovery and execution are mocked.
No TeX installation is needed, and no repository artifacts are modified.
"""
from __future__ import annotations

from contextlib import contextmanager
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import check_report


class ReportVerificationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        manifest_path = Path('verification/report-manifest.json')
        self.manifest = json.loads((check_report.ROOT / manifest_path).read_text())
        for relative in (manifest_path, Path(self.manifest['source']),
                         Path(self.manifest['pdf'])):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(check_report.ROOT / relative, target)
        # Establish that later failures concern the mutation or compiler, not
        # an invalid fixture pair or mismatched metadata.
        self.assertEqual(check_report.check_stored(self.root), self.manifest)

    @contextmanager
    def compiler(self, implementation):
        with patch.object(check_report.shutil, 'which', return_value='/mock/pdflatex'), \
             patch.object(check_report.subprocess, 'check_output',
                          return_value=self.manifest['engine'] + '\n'), \
             patch.object(check_report.subprocess, 'run',
                          side_effect=implementation) as run:
            yield run

    def matching_outputs(self, directory):
        """Supply valid-looking outputs so exit status is the failure cause."""
        stem = Path(self.manifest['source']).stem
        shutil.copyfile(self.root / self.manifest['pdf'], directory / (stem + '.pdf'))
        (directory / (stem + '.log')).write_text(
            self.manifest['engine'] + '\n'
            f'Output written on {stem}.pdf ({self.manifest["pages"]} pages, 1 bytes).\n'
        )

    def test_mutated_source_rejected_with_intact_stored_pdf(self):
        source = self.root / self.manifest['source']
        source.write_bytes(source.read_bytes() + b'\n% fixture mutation\n')
        self.assertEqual(check_report.sha256(self.root / self.manifest['pdf']),
                         self.manifest['pdf_sha256'])
        with self.assertRaisesRegex(ValueError, 'Report source hash mismatch'):
            check_report.check_stored(self.root)

    def test_nonzero_compiler_rejected_even_with_matching_outputs(self):
        def failed_command(command, **kwargs):
            self.matching_outputs(Path(kwargs['cwd']))
            # Model subprocess.run's real check= behavior. If the verifier
            # stops checking exits and ignores the return code, this fixture
            # returns normally and its otherwise matching outputs could pass.
            if kwargs.get('check'):
                raise subprocess.CalledProcessError(7, command)
            return subprocess.CompletedProcess(command, 7)

        with self.compiler(failed_command) as run:
            with self.assertRaises(subprocess.CalledProcessError) as failure:
                check_report.build_report(self.root, self.manifest, 'pdflatex',
                                          self.root / 'output')
            self.assertEqual(failure.exception.returncode, 7)
            self.assertEqual(run.call_count, 1)

    def test_zero_exit_without_fresh_pdf_and_log_rejected(self):
        output = self.root / 'output'
        output.mkdir()
        # A previous matching PDF/log beside the fresh build must not rescue a
        # successful command that produced neither required fresh artifact.
        self.matching_outputs(output)

        def successful_no_output(command, **kwargs):
            self.assertNotEqual(Path(kwargs['cwd']), output)
            return subprocess.CompletedProcess(command, 0)

        with self.compiler(successful_no_output) as run:
            with self.assertRaisesRegex(ValueError, 'Missing fresh PDF or final log'):
                check_report.build_report(self.root, self.manifest, 'pdflatex', output)
            self.assertEqual(run.call_count, 3)

    def test_interrupted_restart_replaces_previous_success_before_validation(self):
        output = self.root / 'output'
        output.mkdir()
        report = output / 'result.json'
        report.write_text(json.dumps({
            'passed': True, 'run_status': 'complete', 'byte_identical': True,
            'final_log': 'previous-build/report.log',
        }))

        def interrupted_validation(root):
            # Check while the new run is active, before finally can rewrite
            # anything: a hard interruption here must not expose old success.
            active = json.loads(report.read_text())
            self.assertFalse(active['passed'])
            self.assertEqual(active['run_status'], 'in_progress')
            self.assertNotIn('byte_identical', active)
            self.assertNotIn('final_log', active)
            raise KeyboardInterrupt

        with patch('sys.argv', ['check_report.py', '--build', '--output-dir', str(output)]), \
             patch.object(check_report, 'check_stored', side_effect=interrupted_validation):
            with self.assertRaises(KeyboardInterrupt):
                check_report.main()

        interrupted = json.loads(report.read_text())
        self.assertFalse(interrupted['passed'])
        self.assertEqual(interrupted['run_status'], 'in_progress')
        self.assertNotIn('byte_identical', interrupted)
        self.assertNotIn('final_log', interrupted)


if __name__ == '__main__':
    unittest.main()
