#!/usr/bin/env python3
"""Check repository navigation and the common learning map, without network access.

These are source checks, not mathematical proof or hosted-rendering validation.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
FIELDS = (
    'Central question', 'Understanding target', 'Dependencies and story role',
    'Conceptual connection', 'Sources',
)


def anchors(text: str) -> set[str]:
    """Collect explicit IDs and the heading slugs used by these Markdown files."""
    result = set(re.findall(r'<a\s+id=[\"\']([^\"\']+)', text))
    seen: dict[str, int] = {}
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
        if in_fence:
            continue
        match = re.match(r'^#{1,6}\s+(.+?)\s*#*$', line)
        if match:
            title = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', match[1])
            title = re.sub(r'<[^>]+>', '', title).lower()
            slug = re.sub(r'[^\w\s-]', '', title).replace(' ', '-')
            index = seen.get(slug, 0)
            seen[slug] = index + 1
            result.add(slug if index == 0 else f'{slug}-{index}')
    return result


def source_math(text: str, name: str) -> int:
    """Validate paired fences, inline delimiters, and unescaped grouping braces."""
    if any(ord(c) < 32 and c not in '\n\t' for c in text):
        raise AssertionError(f'{name}: unexpected control character')
    fence = None
    block: list[str] = []
    expressions: list[str] = []
    for line in text.splitlines():
        match = re.match(r'^\s*```(\w*)\s*$', line)
        if match:
            if fence is None:
                fence = match[1]
                block = []
            else:
                if match[1]:
                    raise AssertionError(f'{name}: nested or mismatched fence')
                if fence == 'math':
                    expressions.append('\n'.join(block))
                fence = None
            continue
        if fence is not None:
            block.append(line)
            continue
        if line.count('$`') != line.count('`$'):
            raise AssertionError(f'{name}: unpaired inline math delimiter')
        expressions.extend(re.findall(r'\$`(.*?)`\$', line))
    if fence is not None:
        raise AssertionError(f'{name}: unclosed fence')
    for expression in expressions:
        depth = 0
        for token in re.finditer(r'(?<!\\)[{}]', expression):
            depth += 1 if token[0] == '{' else -1
            if depth < 0:
                raise AssertionError(f'{name}: unmatched math brace')
        if depth:
            raise AssertionError(f'{name}: unmatched math brace')
    return len(expressions)


def audit(root: Path = ROOT) -> dict:
    docs = sorted([*root.rglob('*.md'), root / 'llms.txt'])
    docs = [p for p in docs if '.git' not in p.parts and 'review-output' not in p.parts]
    text = {p.resolve(): p.read_text(encoding='utf-8') for p in docs}
    known_anchors = {p: anchors(t) for p, t in text.items()}
    links = 0
    math = 0
    for path, value in text.items():
        name = str(path.relative_to(root.resolve()))
        math += source_math(value, name)
        for match in re.finditer(r'\[[^\]\n]+\]\(([^\s)]+)\)', value):
            target = urlsplit(match[1])
            if target.scheme or target.netloc:
                continue
            dest = (path.parent / unquote(target.path)).resolve() if target.path else path
            if not dest.is_relative_to(root.resolve()):
                raise AssertionError(f'{name}: link leaves the repository: {match[1]}')
            if not dest.exists():
                raise AssertionError(f'{name}: missing link target: {match[1]}')
            if target.fragment and unquote(target.fragment) not in known_anchors.get(dest, set()):
                raise AssertionError(f'{name}: missing anchor: {match[1]}')
            links += 1
    milestone_path = (root / 'learning/MILESTONES.md').resolve()
    value = text[milestone_path]
    matches = list(re.finditer(r'^### M(\d{2})\. (.+)$', value, re.M))
    if [int(m[1]) for m in matches] != list(range(1, 31)):
        raise AssertionError('Milestone IDs must be exactly M01 through M30 in order')
    split = value.index('## Phase II:')
    if sum(m.start() < split for m in matches) != 13:
        raise AssertionError('Expected 13 background and 17 narrative milestones')
    dependencies = 0
    for pos, match in enumerate(matches):
        end = matches[pos + 1].start() if pos + 1 < len(matches) else len(value)
        block = value[match.end():end]
        for field in FIELDS:
            if block.count(f'**{field}:**') != 1:
                raise AssertionError(f'M{match[1]}: missing or duplicate {field}')
        dep = re.search(r'\*\*Dependencies and story role:\*\* ([^\n]+)', block)[1]
        for first, last in re.findall(r'M(\d{2})(?:[–-]M?(\d{2}))?', dep):
            refs = range(int(first), int(last or first) + 1)
            for previous in refs:
                if not 1 <= previous < int(match[1]):
                    raise AssertionError(f'M{match[1]}: non-backward dependency M{previous:02d}')
                dependencies += 1
    if list(root.rglob('COACHING.md')) or (root / 'manuscript').exists():
        raise AssertionError('Personal coaching or an obsolete manuscript entrypoint is present')
    for relative in ['README.md', 'llms.txt', 'learning/MILESTONES.md', 'learning/WATROUS_BRIDGE.md']:
        if 'Watrous' not in (root / relative).read_text(encoding='utf-8'):
            raise AssertionError(f'{relative}: missing selected anchor')
    return {
        'documents': len(docs), 'relative_links': links, 'math_expressions': math,
        'milestones': 30, 'required_fields': 150, 'phase_allocation': [13, 17],
        'backward_dependency_edges': dependencies,
        'scope': 'Source syntax, file/anchor navigation, and map structure only.',
    }


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
    print('PASS source structure and learning-map checks')
