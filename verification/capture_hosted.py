#!/usr/bin/env python3
"""Capture actual public GitHub pages at an immutable revision.

No login, token, account mutation, or local Markdown re-rendering is used.
DOM checks cannot replace visual inspection of the saved screenshots.
"""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import re
import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PAGES = [
    'README.md', 'learning/WATROUS_BRIDGE.md', 'learning/MILESTONES.md',
    'science/robustness.md', 'science/optimal_design.md',
    'science/nonunitality.md', 'science/certification.md', 'science/product_channels.md',
]
DOM_SCAN = r"""root => {
  const all = [];
  function walk(node) {
    for (const el of node.querySelectorAll('*')) {
      all.push(el);
      if (el.shadowRoot) walk(el.shadowRoot);
    }
  }
  walk(root);
  const errors = all.filter(e => e.matches('.katex-error, mjx-merror, merror, [data-mjx-error]'));
  const hosts = all.filter(e => e.matches('math-renderer'));
  const rendered = all.filter(e => e.matches('mjx-container, .katex, math'));
  const headings = all.filter(e => /^H[1-6]$/.test(e.tagName)).map(e => {
    const b = e.getBoundingClientRect();
    return {text: e.innerText, x: b.x, y: b.y + window.scrollY, width: b.width, height: b.height};
  });
  return {math_hosts: hosts.length, rendered_nodes: rendered.length,
    errors: errors.map(e => (e.textContent || e.getAttribute('data-mjx-error') || '').slice(0, 500)),
    headings, text_length: root.innerText.length};
}"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default='GoGoKo699/Quantum-Training-Robustness')
    parser.add_argument('--ref', default=None, help='Full immutable Git commit SHA')
    parser.add_argument('--output', type=Path, default=Path('review-output/hosted'))
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', args.repo):
        parser.error('Invalid repository name')
    ref = args.ref or subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    if not re.fullmatch(r'[0-9a-f]{40}', ref):
        parser.error('--ref must be a full lowercase commit SHA')
    args.output.mkdir(parents=True, exist_ok=True)
    report = {'repository': args.repo, 'revision': ref,
              'playwright': importlib.metadata.version('playwright'), 'pages': [],
              'scope': 'Actual public GitHub DOM and screenshots; visual review remains required.'}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        report['browser'] = browser.version
        context = browser.new_context(viewport={'width': 1440, 'height': 1100}, device_scale_factor=1)
        for filename in PAGES:
            page = context.new_page()
            slug = filename.replace('/', '__').replace('.md', '')
            url = f'https://github.com/{args.repo}/blob/{ref}/{filename}'
            item = {'path': filename, 'url': url}
            try:
                response = page.goto(url, wait_until='domcontentloaded', timeout=60000)
                item['http_status'] = response.status if response else None
                if response is None or response.status != 200:
                    raise RuntimeError(f'HTTP status {item["http_status"]}')
                article = page.locator('article.markdown-body').first
                if not article.count():
                    article = page.locator('.markdown-body').first
                article.wait_for(state='visible', timeout=30000)
                # Scroll to load intersection-triggered mathematical rendering.
                height = page.evaluate('document.documentElement.scrollHeight')
                for y in range(0, int(height), 800):
                    page.evaluate('y => window.scrollTo(0,y)', y)
                    page.wait_for_timeout(150)
                page.wait_for_timeout(1500)
                item.update(article.evaluate(DOM_SCAN))
                if item['math_hosts'] and not item['rendered_nodes']:
                    page.wait_for_timeout(5000)
                    item.update(article.evaluate(DOM_SCAN))
                await_fonts = 'document.fonts.ready.then(() => true)'
                page.evaluate(await_fonts)
                page.evaluate('window.scrollTo(0,0)')
                page.screenshot(path=str(args.output / f'{slug}.png'), full_page=True)
                (args.output / f'{slug}.html').write_text(page.content(), encoding='utf-8')
                (args.output / f'{slug}.txt').write_text(article.inner_text(), encoding='utf-8')
                if item['text_length'] < 200:
                    raise RuntimeError('The rendered article is unexpectedly short')
                if not item['rendered_nodes']:
                    raise RuntimeError('No rendered mathematical nodes were observed')
                if item['errors']:
                    raise RuntimeError('The hosted renderer reports a mathematical error')
                item['status'] = 'captured'
            except Exception as exc:
                item['status'] = 'failed'
                item['failure'] = f'{type(exc).__name__}: {exc}'
                try:
                    page.screenshot(path=str(args.output / f'{slug}__failure.png'), full_page=True)
                except Exception:
                    pass
            finally:
                report['pages'].append(item)
                (args.output / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
                print(json.dumps({k: v for k, v in item.items() if k != 'headings'}), flush=True)
                page.close()
                time.sleep(1)
        browser.close()
    return int(any(p['status'] != 'captured' for p in report['pages']))


if __name__ == '__main__':
    raise SystemExit(main())
