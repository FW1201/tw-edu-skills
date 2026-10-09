#!/usr/bin/env python3
"""Validate the installable inventory, entrypoints and local resource references."""
import ast
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote
import yaml

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {'課程設計', '評量命題', '教材資源', '學生表現', '班級經營', '教育行政', '教師專業', '套組設定'}
V5_SECTIONS = ['定位與邊界', '開始前', '思維路線', '台灣情境要點', '產出', '品質關卡', '交接']
BUNDLE_FILES = {'curriculum': ['scripts/lookup_curriculum.py', 'references/curriculum/snapshot-manifest.json', 'references/108_core_competencies.md']}

def validate(root=ROOT):
    manifest = json.loads((root / 'skills-manifest.json').read_text())
    records = manifest['skills']
    names = [item['name'] for item in records]
    errors = []
    actual = sorted(p.parent.name for p in root.glob('tw-edu-*/SKILL.md'))
    if len(set(names)) != len(names) or sorted(names) != actual:
        errors.append('Manifest must list every installable tw-edu-* Skill exactly once')
    for item in records:
        base = root / item['name']
        if item.get('category') not in CATEGORIES:
            errors.append(f"{base.name}: category must be one of {sorted(CATEGORIES)}")
        for bundle in item.get('bundles', []):
            if bundle not in BUNDLE_FILES:
                errors.append(f'{base.name}: unknown bundle {bundle}')
                continue
            for rel in BUNDLE_FILES[bundle]:
                if not (base / rel).is_file():
                    errors.append(f'{base.name}: bundle {bundle} missing {rel}')
        text = (base / 'SKILL.md').read_text()
        try:
            meta = yaml.safe_load(text.split('---', 2)[1])
            if meta['name'] != item['name'] or str(meta.get('version',meta.get('metadata',{}).get('version'))) != item['version']:
                errors.append(f'{base.name}: metadata differs from manifest')
            description = meta.get('description')
            if not isinstance(description, str) or not description.strip():
                errors.append(f'{base.name}: description missing')
            elif not 40 <= len(description) <= 220 or '適用於' not in description:
                errors.append(f'{base.name}: description must be 40-220 characters and include 適用於 triggers')
            if meta.get('metadata', {}).get('category') != item.get('category'):
                errors.append(f'{base.name}: SKILL.md metadata.category differs from manifest')
        except (IndexError, KeyError, TypeError, yaml.YAMLError) as exc:
            errors.append(f'{base.name}: invalid metadata: {exc}')
        for ref in re.findall(r'\]\(([^)]+)\)', text):
            if '://' not in ref and not ref.startswith('#'):
                local_ref = Path(unquote(ref.split('#')[0]))
                candidate = (base / local_ref).resolve()
                try:
                    candidate.relative_to(base.resolve())
                except ValueError:
                    errors.append(f'{base.name}: link escapes skill directory: {ref}')
                    continue
                if not candidate.is_file():
                    errors.append(f'{base.name}: missing link {ref}')
        if '../../tw_edu_' in text or 'LLM Wiki' in text:
            errors.append(f'{base.name}: nonportable reference')
        headings = re.findall(r'^## (.+?)\s*$', text, re.M)
        if headings != V5_SECTIONS:
            errors.append(f'{base.name}: sections must be exactly {V5_SECTIONS}; found {headings}')
        if 'teacher-profile.md' not in text:
            errors.append(f'{base.name}: missing profile rules')
        if item['entrypoint']:
            if not (base / item['entrypoint']).is_file():
                errors.append(f'{base.name}: missing entrypoint')
            if not list((base / 'schemas').glob('*.json')) or not list((base / 'examples').glob('*.json')):
                errors.append(f'{base.name}: missing schema or example')
            if not (base / 'scripts/edu_runtime/cli.py').is_file():
                errors.append(f'{base.name}: runtime not bundled')
        for script in (base / 'scripts').rglob('*.py'):
            try:
                ast.parse(script.read_text())
            except SyntaxError as exc:
                errors.append(f'{script}: {exc}')
    return errors

if __name__ == '__main__':
    errors = validate()
    count = len(json.loads((ROOT / 'skills-manifest.json').read_text())['skills'])
    print('\n'.join(errors) if errors else f'PASS: {count} independent Skills, metadata, resources and syntax')
    sys.exit(bool(errors))
