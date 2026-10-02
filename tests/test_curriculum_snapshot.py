import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SCRIPT=ROOT/'tw-edu-lesson-plan-108/scripts/lookup_curriculum.py'
def run(tmp_path,domain,code):
 result=subprocess.run([sys.executable,str(SCRIPT),'--domain',domain,'--code',code],cwd=tmp_path,text=True,capture_output=True,check=True)
 return json.loads(result.stdout)
def test_domain_collisions_and_independent_lookup(tmp_path):
 chinese=run(tmp_path,'國語文','1-II-1');english=run(tmp_path,'英語文','1-Ⅱ-1')
 assert chinese['status']=='found_in_snapshot' and english['status']=='found_in_snapshot'
 assert chinese['matches'][0]['description']!=english['matches'][0]['description']
 assert run(tmp_path,'國語文','語-J-A1')['status']=='not_found_in_snapshot'
 assert run(tmp_path,'國語文','國S-U-A1')['status']=='found_in_snapshot'
def test_bundled_snapshot_and_generated_rows():
 subprocess.run([sys.executable,str(ROOT/'scripts/verify_curriculum_snapshot.py')],check=True)
