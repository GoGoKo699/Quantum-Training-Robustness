#!/usr/bin/env python3
"""Regression fixtures for source and hosted-rendering checks.

Run without dependencies for source/report tests. Set QTR_BROWSER_TESTS=1
with Playwright and Chromium installed to exercise the actual DOM scanner.
Fixtures validate detection behavior, not scientific claims.
"""
from __future__ import annotations

import os
import unittest

from capture_hosted import DOM_SCAN, validate_capture
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
