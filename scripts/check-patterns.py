#!/usr/bin/env python3
"""Check pattern files against the format and the master plan (docs/pattern-plan.md).

Usage: python3 scripts/check-patterns.py [id ...]   (no ids = check every pattern file)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / 'docs' / 'pattern-plan.md'
PATTERNS = ROOT / 'src' / 'content' / 'patterns'
TYPES = {'ingredient', 'technique', 'process', 'preparation', 'safety', 'etiquette', 'pairing'}

plan = {}
cluster = None
for line in PLAN.read_text().splitlines():
    m = re.match(r'## \d+\. ([a-z-]+):', line)
    if m:
        cluster = m.group(1)
    m = re.match(r'\| ([a-z0-9-]+) \| (.+?) \| ([a-z]+) \|', line)
    if m and m.group(1) != 'id':
        plan[m.group(1)] = {'title': m.group(2), 'type': m.group(3), 'cluster': cluster}


def check(path: Path) -> list[str]:
    errs = []
    pid = path.stem
    text = path.read_text()
    m = re.match(r'---\n(.*?)\n---\n(.*)', text, re.S)
    if not m:
        return ['no frontmatter']
    fm, body = m.groups()
    if pid not in plan:
        errs.append('id not in plan')
        return errs
    p = plan[pid]

    def field(name):
        fm_m = re.search(rf'^{name}:\s*(.*)$', fm, re.M)
        return fm_m.group(1).strip() if fm_m else None

    if field('title') != p['title']:
        errs.append(f"title {field('title')!r} != plan {p['title']!r}")
    if field('type') != p['type']:
        errs.append(f"type {field('type')!r} != plan {p['type']!r}")
    if field('cluster') != p['cluster']:
        errs.append(f"cluster {field('cluster')!r} != plan {p['cluster']!r}")
    if not field('problem'):
        errs.append('missing problem')
    if field('published') is None:
        errs.append('missing published')
    applies = re.findall(r'^  - (.+)$', fm.split('appliesWhen:')[1].split('\n', 1)[1] if 'appliesWhen:' in fm else '', re.M)
    applies = applies[:3] if applies else []
    if len(re.findall(r'^  - ', fm, re.M)) < 3:
        errs.append('appliesWhen needs 3 items')
    rel = field('related') or ''
    rel_ids = re.findall(r'[a-z0-9-]+', rel.strip('[]'))
    for r in rel_ids:
        if r not in plan:
            errs.append(f'related id not in plan: {r}')
        if r == pid:
            errs.append('related lists itself')

    heads = re.findall(r'^## (.+)$', body, re.M)
    if heads != ['Summary', 'Context', 'Usage', 'References']:
        errs.append(f'sections are {heads}')
    summary = body.split('## Context')[0]
    if not re.search(r'This pattern is for', summary):
        errs.append('Summary should start "This pattern is for"')
    rows = [l for l in summary.splitlines() if l.startswith('|')]
    if not rows or not rows[0].startswith('| Recommendation | Why? |'):
        errs.append('Summary table header must be | Recommendation | Why? |')
    n = len(rows) - 2
    if not 3 <= n <= 6:
        errs.append(f'table has {n} rows (3 to 6)')
    context = body.split('## Context')[1].split('## Usage')[0] if '## Context' in body else ''
    for phrase in ['This pattern suits', 'It does not suit', "There's a trade-off"]:
        if phrase not in context:
            errs.append(f'Context missing "{phrase}"')
    usage = body.split('## Usage')[1].split('## References')[0] if '## Usage' in body else ''
    paras = [x for x in usage.strip().split('\n\n') if x.strip() and not x.startswith('```')]
    bold_paras = [x for x in paras if re.match(r'\*\*[^*]+:\*\*', x.strip())]
    if not 2 <= len(bold_paras) <= 4:
        errs.append(f'Usage has {len(bold_paras)} paragraphs starting **Label:** (2 to 4)')
    refs = body.split('## References')[1] if '## References' in body else ''
    ref_lines = [l for l in refs.splitlines() if l.startswith('- ')]
    if not 3 <= len(ref_lines) <= 5:
        errs.append(f'{len(ref_lines)} references (3 to 5)')
    for l in ref_lines:
        if not re.match(r'- \[[^\]]+\]\(https?://[^)]+\), .+\. .+', l):
            errs.append(f'reference format: {l[:70]}')
    for link in re.findall(r'\]\(\.\./([a-z0-9-]+)/\)', body):
        if link not in plan:
            errs.append(f'inline link to unknown id: {link}')
        if link == pid:
            errs.append('links to itself')
    for bad in re.findall(r'\]\((?!https?://|\.\./[a-z0-9-]+/\))[^)]*\)', body):
        errs.append(f'odd link target: {bad}')
    words = len(re.sub(r'\(https?://[^)]+\)', '', body).split())
    if not 400 <= words <= 800:
        errs.append(f'{words} words (aim for 450 to 700)')
    if '—' in body:
        errs.append('contains an em dash; rephrase')
    for us, au in [('color', 'colour'), ('flavor', 'flavour'), ('favorite', 'favourite'), ('center', 'centre'), ('fiber', 'fibre'), ('liter', 'litre'), ('gray', 'grey')]:
        if re.search(rf'\b{us}(s|ed|ing|ful)?\b', body.split('## References')[0] + fm, re.I):
            errs.append(f'US spelling "{us}" (use "{au}")')
    return errs


ids = sys.argv[1:] or sorted(p.stem for p in PATTERNS.glob('*.md'))
bad = 0
for pid in ids:
    path = PATTERNS / f'{pid}.md'
    if not path.exists():
        print(f'{pid}: MISSING')
        bad += 1
        continue
    errs = check(path)
    if errs:
        bad += 1
        print(f'{pid}:')
        for e in errs:
            print(f'  - {e}')
print(f'{len(ids) - bad}/{len(ids)} OK' + (f'; {len(plan) - len(list(PATTERNS.glob("*.md")))} plan ids not written yet' if not sys.argv[1:] else ''))
