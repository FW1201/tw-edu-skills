#!/usr/bin/env python3
"""Query bundled curriculum snapshots without a Harness dependency."""
import argparse,json,re,unicodedata
from pathlib import Path
DATA=Path(__file__).resolve().parents[1]/'references/curriculum'
KINDS={'competency':'competencies','performance':'performance','content':'content'}
def normalize(code):
 code=unicodedata.normalize('NFKC',code).strip().replace(' ','')
 m=re.fullmatch(r'(.+?)-(I|II|III|IV|V)-(\d+)',code)
 if m:code=f"{m[1]}-{dict(I='Ⅰ',II='Ⅱ',III='Ⅲ',IV='Ⅳ',V='Ⅴ')[m[2]]}-{m[3]}"
 return code

def query(domain,code=None,kind=None,keyword=None,limit=20):
 manifest=json.loads((DATA/'snapshot-manifest.json').read_text());payloads=[json.loads((DATA/f).read_text()) for f in manifest['files']]
 payload=next((p for p in payloads if p['domain']==domain),None)
 if payload is None:raise ValueError('domain not in snapshot; available: '+', '.join(p['domain'] for p in payloads))
 matches=[]
 for k,bucket in KINDS.items():
  if kind and kind!=k:continue
  for item in payload[bucket].values():
   if code and normalize(item['code'])!=normalize(code):continue
   if keyword and keyword not in item['description']:continue
   matches.append(item)
 status='not_found_in_snapshot' if not matches else 'ambiguous' if code and len(matches)>1 else 'found_in_snapshot'
 return {'status':status,'domain':domain,'query_code':code,'snapshot_date':manifest['snapshot_date'],'official_index':manifest['official_index'],'origin_commit':manifest['origin_commit'],'verification_scope':manifest['verification_scope'],'total_matches':len(matches),'matches':matches[:limit]}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--domain',required=True);p.add_argument('--code');p.add_argument('--kind',choices=KINDS);p.add_argument('--keyword');p.add_argument('--limit',type=int,default=20);a=p.parse_args()
 try:
  if a.limit<1:raise ValueError('limit must be positive')
  if not a.code and not a.keyword:raise ValueError('provide --code or --keyword')
  print(json.dumps(query(a.domain,a.code,a.kind,a.keyword,a.limit),ensure_ascii=False,indent=2))
 except (ValueError,OSError,KeyError) as e:p.exit(2,str(e)+'\n')
