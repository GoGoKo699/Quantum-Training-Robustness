#!/usr/bin/env python3
"""Regression fixtures for source and hosted-rendering checks.

Run without dependencies for source/report tests. Set QTR_BROWSER_TESTS=1
with Playwright and Chromium installed to exercise the actual DOM scanner.
Fixtures validate detection behavior, not scientific claims.
"""
from __future__ import annotations

import os
import json
from pathlib import Path
import subprocess
import tempfile
from types import ModuleType
import unittest
from unittest.mock import MagicMock, patch

import capture_hosted
from capture_hosted import DOM_SCAN, collect_source_pages, validate_capture, validate_report
from check_structure import math_expressions


class SourceTests(unittest.TestCase):
    def test_counts_inline_and_display(self):
        self.assertEqual(len(math_expressions('$`x`$\n```math\ny^2\n```\n', 'fixture')), 2)

    def test_ignores_nonmath_code_and_html(self):
        text = '<a id="x"></a>\n```python\nx < y\n\\operatorname{Tr}\n```\n'
        self.assertEqual(math_expressions(text, 'fixture'), [])

    def test_inline_less_than_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'less-than'):
            math_expressions('$`d<N`$', 'fixture')

    def test_display_less_than_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'less-than'):
            math_expressions('```math\nx<1\n```', 'fixture')

    def test_prohibited_macro_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'operatorname'):
            math_expressions(r'$`\operatorname{Tr} A`$', 'fixture')

    def test_repaired_notation_accepted(self):
        self.assertEqual(len(math_expressions(r'$`\mathrm{Tr}\,A=0, d\lt N`$', 'fixture')), 1)

    def test_unpaired_delimiter_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'unpaired'):
            math_expressions('$`x', 'fixture')

    def test_control_character_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'control'):
            math_expressions('$`x\ry`$', 'fixture')

    def test_grouping_and_fence_rejected(self):
        for text in [r'$`\frac{1}{d`$', '```math\nx']:
            with self.subTest(text=text), self.assertRaises(AssertionError):
                math_expressions(text, 'fixture')


class ReportTests(unittest.TestCase):
    def good(self):
        return dict(http_status=200, text_length=300, math_hosts=2,
                    rendered_hosts=2, failed_hosts=[], errors=[])

    def test_complete_report_accepted(self):
        validate_capture(self.good(), 2)

    def test_partial_render_rejected(self):
        value = self.good()
        value.update(rendered_hosts=1, failed_hosts=[{'index': 1}])
        with self.assertRaises(AssertionError):
            validate_capture(value, 2)

    def test_source_host_mismatch_rejected(self):
        with self.assertRaises(AssertionError):
            validate_capture(self.good(), 3)

    def test_error_message_rejected(self):
        value = self.good()
        value['errors'] = ['The following macros are not allowed: operatorname']
        with self.assertRaises(AssertionError):
            validate_capture(value, 2)

    def test_bad_http_or_empty_article_rejected(self):
        for field, bad in [('http_status', 503), ('text_length', 10)]:
            value = self.good()
            value[field] = bad
            with self.subTest(field=field), self.assertRaises(AssertionError):
                validate_capture(value, 2)


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.git('init', '-q')
        (self.root / 'README.md').write_text('# Fixture\n$`x`$\n', encoding='utf-8')
        (self.root / 'science').mkdir()
        (self.root / 'science/proof.md').write_text('# Proof\n$`y`$\n', encoding='utf-8')
        self.git('add', '.')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Fixture')
        self.ref = self.git('rev-parse', 'HEAD')

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, text=True).strip()

    def test_clean_manifest_matches_committed_blobs(self):
        pages = collect_source_pages(self.root, self.ref)
        self.assertEqual([(p, n) for p, n, _ in pages],
                         [('README.md', 1), ('science/proof.md', 1)])
        for path, _, blob in pages:
            self.assertEqual(blob, self.git('rev-parse', f'{self.ref}:{path}'))

    def test_same_count_equation_edit_rejected(self):
        (self.root / 'README.md').write_text('# Fixture\n$`2*x`$\n', encoding='utf-8')
        with self.assertRaisesRegex(AssertionError, 'source differs'):
            collect_source_pages(self.root, self.ref)

    def test_deleted_math_page_rejected(self):
        (self.root / 'science/proof.md').unlink()
        with self.assertRaisesRegex(AssertionError, 'missing='):
            collect_source_pages(self.root, self.ref)

    def test_uncommitted_math_page_rejected(self):
        (self.root / 'science/new.md').write_text('$`z`$\n', encoding='utf-8')
        with self.assertRaisesRegex(AssertionError, 'added='):
            collect_source_pages(self.root, self.ref)

    def test_browser_startup_failure_invalidates_previous_report(self):
        output = self.root / 'review-output'
        output.mkdir()
        report_path = output / 'report.json'
        report_path.write_text('{"run_status":"complete","passed":true}', encoding='utf-8')
        module = ModuleType('playwright.sync_api')
        module.sync_playwright = MagicMock()
        module.sync_playwright.return_value.__enter__.return_value.chromium.launch.side_effect = RuntimeError('Browser unavailable')
        with patch.object(capture_hosted, 'ROOT', self.root), \
             patch('sys.argv', ['capture_hosted.py', '--ref', self.ref, '--output', str(output)]), \
             patch('importlib.metadata.version', return_value='fixture'), \
             patch.dict('sys.modules', {'playwright': ModuleType('playwright'),
                                        'playwright.sync_api': module}), \
             self.assertRaisesRegex(RuntimeError, 'Browser unavailable'):
            capture_hosted.main()
        report = json.loads(report_path.read_text(encoding='utf-8'))
        self.assertEqual(report['run_status'], 'in_progress')
        self.assertEqual(len(report['source_manifest']), 2)
        self.assertEqual(report['pages'], [])
        self.assertNotIn('passed', report)


class CompleteReportTests(unittest.TestCase):
    def good(self):
        manifest = [{'path': p, 'source_blob': 'a' * 40, 'expected_math': 2}
                    for p in ['README.md', 'science/proof.md']]
        pages = [dict(source, http_status=200, text_length=300, math_hosts=2,
                      rendered_hosts=2, failed_hosts=[], errors=[], status='captured')
                 for source in manifest]
        return dict(run_status='complete', source_manifest=manifest, pages=pages)

    def test_full_report_accepted(self):
        validate_report(self.good())

    def test_successful_subset_rejected(self):
        value = self.good()
        value['pages'].pop()
        with self.assertRaisesRegex(AssertionError, 'source manifest'):
            validate_report(value)

    def test_interrupted_run_rejected(self):
        value = self.good()
        value['run_status'] = 'in_progress'
        with self.assertRaisesRegex(AssertionError, 'incomplete'):
            validate_report(value)

    def test_wrong_blob_rejected(self):
        value = self.good()
        value['pages'][0]['source_blob'] = 'b' * 40
        with self.assertRaisesRegex(AssertionError, 'source mismatch'):
            validate_report(value)


@unittest.skipUnless(os.environ.get('QTR_BROWSER_TESTS') == '1', 'optional Chromium DOM fixtures')
class BrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch()
        cls.page = cls.browser.new_page()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def scan(self, html):
        self.page.set_content('<article>' + '<p>Fixture text. </p>' * 30 + html + '</article>')
        value = self.page.locator('article').evaluate(DOM_SCAN)
        value['http_status'] = 200
        return value

    def test_successful_mathml(self):
        value = self.scan('<math-renderer><math><mi>x</mi></math></math-renderer>')
        self.assertEqual(value['rendered_hosts'], 1)
        validate_capture(value, 1)

    def test_github_macro_error_despite_other_success(self):
        value = self.scan('<math-renderer><math><mi>x</mi></math></math-renderer>'
                          '<math-renderer><div class="flash flash-error">'
                          'The following macros are not allowed: operatorname</div>'
                          '<pre>$$\\operatorname{Tr} A$$</pre></math-renderer>')
        self.assertEqual(value['math_hosts'], 2)
        self.assertEqual(value['rendered_hosts'], 1)
        self.assertTrue(value['errors'])
        with self.assertRaises(AssertionError):
            validate_capture(value, 2)

    def test_open_shadow_root_error(self):
        self.scan('<math-renderer id="shadow"></math-renderer>')
        self.page.evaluate("document.getElementById('shadow').attachShadow({mode:'open'}).innerHTML = '<merror>Invalid expression</merror>'")
        value = self.page.locator('article').evaluate(DOM_SCAN)
        value['http_status'] = 200
        self.assertTrue(value['failed_hosts'])
        self.assertTrue(value['errors'])
        with self.assertRaises(AssertionError):
            validate_capture(value, 1)


if __name__ == '__main__':
    unittest.main()
