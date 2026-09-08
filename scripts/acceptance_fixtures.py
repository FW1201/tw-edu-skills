"""Generate explicit samples for visual/browser acceptance; never real student data."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'output/acceptance'
DEST.mkdir(parents=True, exist_ok=True)
manifest = json.loads((ROOT / 'skills-manifest.json').read_text())
for item in manifest['skills']:
    if not item['entrypoint']: continue
    output = DEST / (item['name'] + '.' + item['format'])
    if output.exists(): continue
    if item['name'] == 'tw-edu-exam-generator' and (DEST / (item['name'] + '-student.docx')).exists(): continue
    subprocess.run([sys.executable, str(ROOT / item['name'] / item['entrypoint']), '--example', '--output', str(output)], check=True)
for mode in ['quiz', 'flashcard', 'lottery', 'timer']:
    data = json.loads((ROOT / 'tw-edu-mini-app/examples/example.json').read_text())
    if mode != 'quiz':
        data['content'] = {'title': '瀏覽器驗收（範例）', 'mode': mode}
        data['content'].update({'cards':[{'front':'<img src=x onerror=alert(1)>','back':'後面'}]} if mode == 'flashcard' else {'entries':['甲','乙']} if mode == 'lottery' else {'seconds':3})
    source, output = DEST / ('mini-' + mode + '.json'), DEST / ('mini-' + mode + '.html')
    if output.exists(): continue
    source.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    subprocess.run([sys.executable, str(ROOT / 'tw-edu-mini-app/scripts/generate_mini_app.py'), '--input', str(source), '--output', str(output)], check=True)
