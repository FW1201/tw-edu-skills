#!/usr/bin/env python3
"""Convert anonymous response CSV to the standard evidence content; no grading guesses."""
import argparse,csv,json
from pathlib import Path
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--csv',type=Path,required=True);p.add_argument('--items',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 try:
  d=json.loads(a.items.read_text());ids={x['id'] for x in d['content']['items']}
  with a.csv.open(encoding='utf-8-sig',newline='') as f:
   reader=csv.DictReader(f)
   if not reader.fieldnames or set(reader.fieldnames)!={'student_id',*ids} or len(reader.fieldnames)!=len(ids)+1:raise ValueError('CSV needs student_id and exactly one column per item')
   rows=[]
   for row in reader:
    if None in row or any(v is None for v in row.values()) or not row['student_id'].strip():raise ValueError('malformed CSV row')
    rows.append({'student_id':row['student_id'].strip(),'answers':{k:row[k].strip() or None for k in ids}})
  from edu_runtime.learning_evidence import analyze
  d['content']['responses']=rows;analyze(d['content']);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 except (ValueError,KeyError,TypeError,OSError) as e:p.exit(2,str(e)+'\n')
