#!/usr/bin/env python3
"""Check journey files: frontmatter, steps, body sections, and that every pattern is used by some journey.

Usage: python3 scripts/check-journeys.py [id ...]   (no ids = check all, plus coverage)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JOURNEYS = ROOT / 'src' / 'content' / 'journeys'
PATTERNS = ROOT / 'src' / 'content' / 'patterns'
PLAN = ROOT / 'docs' / 'pattern-plan.md'
COURSES = {'antipasto', 'primo', 'secondo', 'contorno', 'pizza and bread', 'dolce', 'whole meal'}
LEVELS = {'first steps', 'building skills', 'confident cook'}

journey_plan_ids = {c.split('|')[2].strip() for c in (ROOT / 'docs' / 'journey-plan.md').read_text().splitlines() if re.match(r'\| \d+ \|', c)}
plan_ids = {m.group(1) for l in PLAN.read_text().splitlines() if (m := re.match(r'\| ([a-z0-9-]+) \| ', l))} - {'id', '---'}


def steps_of(fm: str) -> list[tuple[str, str]]:
    return re.findall(r'^  - pattern: ([a-z0-9-]+)\n    note: (.+)$', fm, re.M)


def check(path: Path) -> list[str]:
    errs = []
    text = path.read_text()
    m = re.match(r'---\n(.*?)\n---\n(.*)', text, re.S)
    if not m:
        return ['no frontmatter']
    fm, body = m.groups()

    def field(name):
        f = re.search(rf'^{name}:\s*(.*)$', fm, re.M)
        return f.group(1).strip().strip('"\'') if f else None

    for f in ['title', 'region', 'course', 'level', 'order', 'time', 'serves', 'intro', 'published']:
        if not field(f):
            errs.append(f'missing {f}')
    if field('course') not in COURSES:
        errs.append(f'course {field("course")!r}')
    if field('level') not in LEVELS:
        errs.append(f'level {field("level")!r}')
    steps = steps_of(fm)
    n_dash = len(re.findall(r'^  - ', fm, re.M))
    if len(steps) != n_dash:
        errs.append(f'{n_dash} step items but {len(steps)} parse as "- pattern: id" + "note: one line"')
    if len(steps) < 4:
        errs.append('fewer than 4 steps')
    for pid, note in steps:
        if pid not in plan_ids:
            errs.append(f'unknown pattern {pid}')
        if len(note.split()) < 8:
            errs.append(f'note for {pid} is very short')
        if note.startswith(("'", '"')) and not note.endswith(note[0]):
            errs.append(f'note for {pid} has an unclosed quote')
        if ': ' in note and not note.startswith(("'", '"')):
            errs.append(f'note for {pid} contains ": " and must be quoted for YAML')
    heads = re.findall(r'^## (.+)$', body, re.M)
    if heads != ['About the dish', 'What you need', 'Where it usually goes wrong']:
        errs.append(f'sections are {heads}')
    journey_ids = {p.stem for p in JOURNEYS.glob('*.md')} | journey_plan_ids
    for link in re.findall(r'\]\((\.\./[^)]*)\)', text):
        mm = re.fullmatch(r'\.\./\.\./patterns/([a-z0-9-]+)/', link)
        mj = re.fullmatch(r'\.\./([a-z0-9-]+)/', link)
        if not ((mm and mm.group(1) in plan_ids) or (mj and mj.group(1) in journey_ids)):
            errs.append(f'link {link} (use ../../patterns/<id>/ or ../<journey-id>/)')
    if '—' in text:
        errs.append('contains an em dash')
    for us, au in [('color', 'colour'), ('flavor', 'flavour'), ('center', 'centre'), ('liter', 'litre'), ('gray', 'grey')]:
        if re.search(rf'\b{us}(s|ed|ing|ful)?\b', text, re.I):
            errs.append(f'US spelling "{us}"')
    return errs


ids = sys.argv[1:] or sorted(p.stem for p in JOURNEYS.glob('*.md'))
bad = 0
for jid in ids:
    path = JOURNEYS / f'{jid}.md'
    if not path.exists():
        print(f'{jid}: MISSING')
        bad += 1
        continue
    errs = check(path)
    if errs:
        bad += 1
        print(f'{jid}:')
        for e in errs:
            print(f'  - {e}')
print(f'{len(ids) - bad}/{len(ids)} OK')

if not sys.argv[1:]:
    used = set()
    for p in JOURNEYS.glob('*.md'):
        used |= {pid for pid, _ in steps_of(p.read_text().split('\n---\n')[0])}
    unused = sorted(plan_ids - used)
    print(f'patterns used by no journey ({len(unused)}): {", ".join(unused) or "none"}')
