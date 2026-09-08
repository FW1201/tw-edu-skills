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

def validate(root=ROOT):
    manifest = json.loads((root / 'skills-manifest.json').read_text())
    records = manifest['skills']
    names = [item['name'] for item in records]
    errors = []
    actual = sorted(p.parent.name for p in root.glob('tw-edu-*/SKILL.md'))
    if len(names) != 21 or len(set(names)) != 21 or sorted(names) != actual:
        errors.append('Manifest must match exactly 21 unique installable Skills')
    for item in records:
        base = root / item['name']
        text = (base / 'SKILL.md').read_text()
        try:
            meta = yaml.safe_load(text.split('---', 2)[1])
            if meta['name'] != item['name'] or str(meta['version']) != item['version']:
                errors.append(f'{base.name}: metadata differs from manifest')
            if not isinstance(meta.get('description'), str) or not meta['description'].strip():
                errors.append(f'{base.name}: description missing')
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
    print('\n'.join(errors) if errors else 'PASS: 21 independent Skills, metadata, resources and syntax')
    sys.exit(bool(errors))
