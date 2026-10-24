#!/usr/bin/env python3
"""Capture actual public GitHub pages at the checked immutable revision.

No login, token, account mutation, or local Markdown re-rendering is used.
Every source math expression must have a rendered host. DOM checks cannot
replace visual inspection of the saved screenshots.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import re
import subprocess
import time
from pathlib import Path

from check_structure import ROOT, math_expressions

DOM_SCAN = r"""root => {
  function descendants(node) {
    const out = [];
    for (const el of node.querySelectorAll('*')) {
      out.push(el);
      if (el.shadowRoot) out.push(...descendants(el.shadowRoot));
    }
    return out;
  }
  const all = descendants(root);
  const errorSelector = '.flash-error, .katex-error, mjx-merror, merror, [data-mjx-error]';
  const errorText = /following macros are not allowed|unable to render|math rendering error|undefined control sequence/i;
  const hosts = all.filter(e => e.matches('math-renderer'));
  const renderedSelector = 'mjx-container, .katex, math';
  const hostResults = hosts.map((host, index) => {
    const nodes = descendants(host);
    const errors = nodes.filter(e => e.matches(errorSelector));
    const text = host.textContent || '';
    const rendered = nodes.filter(e => e.matches(renderedSelector)).length;
    const b = host.getBoundingClientRect();
    return {index, rendered_nodes: rendered,
      error: errors.length > 0 || errorText.test(text),
      text: (!rendered || errors.length || errorText.test(text)) ? text.slice(0, 600) : null,
      x: b.x, y: b.y + window.scrollY, width: b.width, height: b.height,
      horizontal_overflow: host.scrollWidth > host.clientWidth + 2};
  });
  const errors = all.filter(e => e.matches(errorSelector)).map(e =>
    (e.textContent || e.getAttribute('data-mjx-error') || '').slice(0, 600));
  const failed = hostResults.filter(h => h.error || h.rendered_nodes === 0);
  const headings = all.filter(e => /^H[1-6]$/.test(e.tagName)).map(e => {
    const b = e.getBoundingClientRect();
    return {text: e.innerText, x: b.x, y: b.y + window.scrollY, width: b.width, height: b.height};
  });
  return {math_hosts: hosts.length,
    rendered_hosts: hostResults.filter(h => h.rendered_nodes > 0 && !h.error).length,
    rendered_nodes: all.filter(e => e.matches(renderedSelector)).length,
    failed_hosts: failed, errors, headings,
    overflowing_hosts: hostResults.filter(h => h.horizontal_overflow),
    text_length: root.innerText.length};
}"""


def validate_capture(item: dict, expected: int) -> None:
    """Fail closed on partial rendering, including GitHub's macro-error boxes."""
    if item.get('http_status') != 200:
        raise AssertionError('The hosted page did not return HTTP 200')
    if item.get('text_length', 0) < 200:
        raise AssertionError('The rendered article is unexpectedly short')
    if item.get('math_hosts') != expected:
        raise AssertionError(f'Source/host count mismatch: expected {expected}, got {item.get("math_hosts")}')
    if item.get('rendered_hosts') != expected or item.get('failed_hosts') or item.get('errors'):
        raise AssertionError('At least one source expression failed hosted rendering')


def collect_source_pages(root: Path, ref: str) -> list[tuple[str, int, str]]:
    """Bind the complete local Markdown set to its immutable Git source."""
    tree = subprocess.check_output(
        ['git', 'ls-tree', '-rz', '--full-tree', ref], cwd=root)
    committed = {}
    for entry in tree.split(b'\0'):
        if not entry:
            continue
        metadata, raw_path = entry.split(b'\t', 1)
        mode, kind, blob = metadata.decode().split()
        path = raw_path.decode('utf-8')
        if path.endswith('.md'):
            if kind != 'blob' or mode not in {'100644', '100755'}:
                raise AssertionError(f'Unsupported Markdown source: {path}')
            committed[path] = blob
    local = {path.relative_to(root).as_posix() for path in root.rglob('*.md')
             if '.git' not in path.relative_to(root).parts
             and 'review-output' not in path.relative_to(root).parts}
    if local != set(committed):
        raise AssertionError(
            f'Markdown source set differs from {ref}: '
            f'missing={sorted(set(committed) - local)}, '
            f'added={sorted(local - set(committed))}')
    pages = []
    for filename, blob in sorted(committed.items()):
        data = (root / filename).read_bytes()
        actual = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
        if actual != blob:
            raise AssertionError(f'Markdown source differs from {ref}: {filename}')
        expected = len(math_expressions(data.decode('utf-8'), filename))
        if expected:
            pages.append((filename, expected, blob))
    if not pages:
        raise AssertionError('No mathematical source pages found')
    return pages


def validate_report(report: dict) -> None:
    """Reject interrupted runs and omissions, even when captured pages pass."""
    manifest = report.get('source_manifest', [])
    pages = report.get('pages', [])
    if report.get('run_status') != 'complete' or not manifest:
        raise AssertionError('The hosted capture run is incomplete')
    if [p.get('path') for p in pages] != [p['path'] for p in manifest]:
        raise AssertionError('The hosted report does not cover its source manifest')
    for item, source in zip(pages, manifest):
        for key in ['source_blob', 'expected_math']:
            if item.get(key) != source[key]:
                raise AssertionError(f'Hosted report source mismatch: {source["path"]}')
        if item.get('status') != 'captured':
            raise AssertionError(f'Hosted capture failed: {source["path"]}')
        validate_capture(item, source['expected_math'])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default='GoGoKo699/Quantum-Training-Robustness')
    parser.add_argument('--ref', default=None, help='Full immutable SHA of the checked-out source')
    parser.add_argument('--output', type=Path, default=Path('review-output/hosted'))
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', args.repo):
        parser.error('Invalid repository name')
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    ref = args.ref or head
    if not re.fullmatch(r'[0-9a-f]{40}', ref) or ref != head:
        parser.error('--ref must equal the full immutable SHA of the checked-out source')
    args.output.mkdir(parents=True, exist_ok=True)
    report = {'repository': args.repo, 'revision': ref,
              'run_status': 'in_progress', 'source_manifest': [], 'pages': [],
              'viewport': {'width': 1440, 'height': 1100},
              'scope': 'Actual public GitHub DOM and screenshots; visual review remains required.'}
    report_path = args.output / 'report.json'
    # Invalidate any earlier report before source validation or browser startup.
    report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    pages = collect_source_pages(ROOT, ref)
    report['source_manifest'] = [
        {'path': filename, 'expected_math': expected, 'source_blob': blob}
        for filename, expected, blob in pages]
    report['playwright'] = importlib.metadata.version('playwright')
    report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        report['browser'] = browser.version
        context = browser.new_context(viewport=report['viewport'], device_scale_factor=1)
        for filename, expected, blob in pages:
            page = context.new_page()
            slug = filename.replace('/', '__').replace('.md', '')
            url = f'https://github.com/{args.repo}/blob/{ref}/{filename}'
            item = {'path': filename, 'url': url, 'source_blob': blob, 'expected_math': expected}
            try:
                response = page.goto(url, wait_until='domcontentloaded', timeout=60000)
                item['http_status'] = response.status if response else None
                if item['http_status'] != 200:
                    raise RuntimeError(f'HTTP status {item["http_status"]}')
                article = page.locator('article.markdown-body').first
                if not article.count():
                    article = page.locator('.markdown-body').first
                article.wait_for(state='visible', timeout=30000)
                # Scroll to activate lazy math, repeating if page height changes.
                for attempt in range(2):
                    height = page.evaluate('document.documentElement.scrollHeight')
                    for y in range(0, int(height), 800):
                        page.evaluate('y => window.scrollTo(0,y)', y)
                        page.wait_for_timeout(80)
                    page.wait_for_timeout(1500)
                    item.update(article.evaluate(DOM_SCAN))
                    if item['errors'] or item['rendered_hosts'] == expected:
                        break
                page.evaluate('document.fonts.ready.then(() => true)')
                page.evaluate('window.scrollTo(0,0)')
                page.screenshot(path=str(args.output / f'{slug}.png'), full_page=True)
                (args.output / f'{slug}.html').write_text(page.content(), encoding='utf-8')
                (args.output / f'{slug}.txt').write_text(article.inner_text(), encoding='utf-8')
                validate_capture(item, expected)
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
                report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
                print(json.dumps({k: v for k, v in item.items() if k not in ['headings', 'overflowing_hosts']}), flush=True)
                page.close()
                time.sleep(1)
        browser.close()
    report['run_status'] = 'complete'
    try:
        validate_report(report)
        report['passed'] = True
    except AssertionError as exc:
        report['passed'] = False
        report['failure'] = str(exc)
    report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    return int(not report['passed'])


if __name__ == '__main__':
    raise SystemExit(main())
