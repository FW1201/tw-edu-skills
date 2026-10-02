#!/usr/bin/env python3
"""Sync physical Skill copies from canonical shared sources."""
import argparse
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def desired_files():
    manifest = json.loads((ROOT / 'skills-manifest.json').read_text())
    rows = '\n'.join(f"| `{s['name']}` | {s['title']} | {s['format']} |" for s in manifest['skills'])
    readme = ROOT / 'README.md'
    if readme.exists():
        content = readme.read_text()
        start, end = '<!-- inventory:start -->', '<!-- inventory:end -->'
        if start in content and end in content:
            prefix, tail = content.split(start, 1)
            _, suffix = tail.split(end, 1)
            yield readme, (prefix + start + '\n| Skill | 用途 | 主要輸出 |\n|---|---|---|\n' + rows + '\n' + end + suffix).encode()
    reference = ['# 技能參考', '', '由 skills-manifest.json 與各技能 schema 產生。共 23 個獨立 Skills。', '', '| Skill | 用途 | 輸入內容 | 輸出 |', '|---|---|---|---|']
    for skill in manifest['skills']:
        schema = ROOT / skill['name'] / 'schemas/input.schema.json'
        required = ', '.join(json.loads(schema.read_text())['properties']['content'].get('required', [])) if schema.exists() else '由 Agent 讀取來源／偏好，產出 Markdown'
        reference.append(f"| [{skill['name']}](../{skill['name']}/SKILL.md) | {skill['purpose']} | {required} | {skill['format']} |")
    reference.extend(['', '## 共同輸入', '', 'schema_version=1.0、skill、language=zh-TW、context（subject、grade、topic）、sources、content。各技能 schema 與 example.json 是具體欄位定義。', '', 'CLI：--input JSON、--output PATH、--validate-only、--example。正式模式驗證失敗即停止，不產生成品。', '', '驗收核對輸入與成品，學生卷不含答案；圖片簡報非文字可編輯，預設 editable。尚待來源查證、Office 視覺及宿主實測項目見 ACCEPTANCE-v4.md。', ''])
    yield ROOT / 'docs/skill-reference.md', '\n'.join(reference).encode()
    for skill in manifest['skills']:
        base = ROOT / skill['name']
        for src in (ROOT / 'shared/references').glob('*.md'):
            yield base / 'references/common' / src.name, src.read_bytes()
        yield base / 'requirements.txt', ('\n'.join(skill['dependencies']) + '\n').encode()
        if skill['entrypoint']:
            for src in (ROOT / 'shared/runtime/edu_runtime').rglob('*'):
                if src.is_file() and '__pycache__' not in src.parts and src.suffix != '.pyc':
                    yield base / 'scripts/edu_runtime' / src.relative_to(ROOT / 'shared/runtime/edu_runtime'), src.read_bytes()

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
