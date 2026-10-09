#!/usr/bin/env python3
"""Sync physical Skill copies from canonical shared sources."""
import argparse
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

CATEGORIES = ['課程設計', '評量命題', '教材資源', '學生表現', '班級經營', '教育行政', '教師專業', '套組設定']
BUNDLES = {'curriculum': ROOT / 'shared/curriculum'}


def _manifest():
    return json.loads((ROOT / 'skills-manifest.json').read_text(encoding='utf-8'))


def _grouped(skills):
    for category in CATEGORIES:
        members = [s for s in skills if s.get('category') == category]
        if members:
            yield category, members


def inventory_table(skills):
    lines = []
    for category, members in _grouped(skills):
        lines += ['', f'### {category}（{len(members)}）', '', '| Skill | 用途 | 主要輸出 |', '|---|---|---|']
        lines += [f"| `{s['name']}` | {s['title']}：{s['purpose']} | {s['format']} |" for s in members]
    return '\n'.join(lines).lstrip('\n')


def desired_files():
    manifest = _manifest()
    skills = manifest['skills']
    readme = ROOT / 'README.md'
    if readme.exists():
        content = readme.read_text(encoding='utf-8')
        start, end = '<!-- inventory:start -->', '<!-- inventory:end -->'
        if start in content and end in content:
            prefix, tail = content.split(start, 1)
            _, suffix = tail.split(end, 1)
            body = f"共 {len(skills)} 個獨立 Skills，分 {len(list(_grouped(skills)))} 個面向。\n\n" + inventory_table(skills)
            yield readme, (prefix + start + '\n' + body + '\n' + end + suffix).encode()
    reference = ['# 技能參考', '', f'由 skills-manifest.json 與各技能 schema 產生。共 {len(skills)} 個獨立 Skills。', '']
    for category, members in _grouped(skills):
        reference += [f'## {category}', '', '| Skill | 用途 | 輸入內容 | 輸出 |', '|---|---|---|---|']
        for skill in members:
            schema = ROOT / skill['name'] / 'schemas/input.schema.json'
            required = ', '.join(json.loads(schema.read_text(encoding='utf-8'))['properties']['content'].get('required', [])) if schema.exists() else '由 Agent 讀取來源／偏好，產出 Markdown'
            reference.append(f"| [{skill['name']}](../{skill['name']}/SKILL.md) | {skill['purpose']} | {required} | {skill['format']} |")
        reference.append('')
    reference.extend(['## 共同輸入', '', 'schema_version=1.0、skill、language=zh-TW、context（subject、grade、topic）、sources、content。各技能 schema 與 example.json 是具體欄位定義。', '', 'CLI：--input JSON、--output PATH、--validate-only、--example。正式模式驗證失敗即停止，不產生成品。', '', '驗收核對輸入與成品，學生卷不含答案；圖片簡報非文字可編輯，預設 editable。尚待來源查證、Office 視覺及宿主實測項目見 MIGRATION-v5.md 與 eval/v5-routing-cases.md。', ''])
    yield ROOT / 'docs/skill-reference.md', '\n'.join(reference).encode()
    for skill in skills:
        base = ROOT / skill['name']
        for src in (ROOT / 'shared/references').glob('*.md'):
            yield base / 'references/common' / src.name, src.read_bytes()
        yield base / 'requirements.txt', ('\n'.join(skill['dependencies']) + '\n').encode()
        if skill['entrypoint']:
            for src in (ROOT / 'shared/runtime/edu_runtime').rglob('*'):
                if src.is_file() and '__pycache__' not in src.parts and src.suffix != '.pyc':
                    yield base / 'scripts/edu_runtime' / src.relative_to(ROOT / 'shared/runtime/edu_runtime'), src.read_bytes()
        for bundle in skill.get('bundles', []):
            source = BUNDLES[bundle]
            for src in source.rglob('*'):
                if src.is_file() and '__pycache__' not in src.parts and src.suffix != '.pyc':
                    yield base / src.relative_to(source), src.read_bytes()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    errors = []
    for target, data in desired_files():
        if target.exists() and target.read_bytes() == data:
            continue
        if args.check:
            errors.append(str(target.relative_to(ROOT)))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    if errors:
        print('Stale/missing bundled assets:\n' + '\n'.join(errors))
        return 1
    print('Bundled assets consistent' if args.check else 'Bundled assets synchronized')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
