#!/usr/bin/env python3
"""Verify bundled data integrity and all generated competency descriptions."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def verify():
 base=ROOT/'tw-edu-lesson-plan-108/references';data=base/'curriculum';manifest=json.loads((data/'snapshot-manifest.json').read_text());count=0;competencies=[]
 assert {p.name for p in data.glob('*.json')}==set(manifest['files'])|{'snapshot-manifest.json'}
 for file,sha in manifest['files'].items():
  path=data/file;assert hashlib.sha256(path.read_bytes()).hexdigest()==sha,file
  payload=json.loads(path.read_text());domain=payload['domain'];seen=set()
  for bucket in ['competencies','performance','content']:
   assert len(payload[bucket])==manifest['counts'][domain][bucket]
   for code,item in payload[bucket].items():
    assert code==item['code'] and item['domain']==domain and item['description'].strip(),(file,code)
    assert (bucket,code) not in seen;seen.add((bucket,code));count+=1
    if bucket=='competencies':competencies.append((code,item['description']))
 table=(base/'108_core_competencies.md').read_text()
 actual=[line for line in table.splitlines() if line.startswith('| `')]
 expected=['| `'+code+'` | '+description.replace('|','\\|')+' |' for code,description in competencies]
 assert actual==expected,'Generated competency table differs from data snapshot'
 print(f'PASS {len(manifest["files"])} domain files / {count} snapshot records / {len(competencies)} exact competency rows')
if __name__=='__main__':verify()
