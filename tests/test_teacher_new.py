import json,sys,subprocess,copy
from pathlib import Path
import pytest
from docx import Document
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'shared/runtime'))
from edu_runtime.learning_evidence import analyze

def data():return {'title':'實際資料','items':[{'id':'Q1','target':'概念','answer':'A','options':['A','B'],'key_status':'verified'},{'id':'Q2','target':'概念','answer':'B','options':['A','B'],'key_status':'ambiguous'}],'responses':[{'student_id':'S1','answers':{'Q1':'A','Q2':'B'}},{'student_id':'S2','answers':{'Q1':None,'Q2':'A'}},{'student_id':'S3','answers':{'Q1':'B'}}]}
def test_denominators_pending_answers_and_observations():
 r=analyze(data());q=r['items'][0];assert q['correct_n']==1 and q['accuracy_all_students']==pytest.approx(1/3) and q['accuracy_answered']==.5 and q['missing_n']==1
 assert r['items'][1]['correct_n'] is None and r['targets']['概念']['possible_responses']==3
 assert r['student_observations']['S2'][0]['status']=='missing'
@pytest.mark.parametrize('defect',['duplicate_student','unknown_item','invalid_answer'])
def test_bad_raw_data(defect):
 d=data()
 if defect=='duplicate_student':d['responses'][1]['student_id']='S1'
 if defect=='unknown_item':d['responses'][0]['answers']['Q3']='A'
 if defect=='invalid_answer':d['responses'][0]['answers']['Q1']='C'
 with pytest.raises(ValueError):analyze(d)

def invoke(skill,d,tmp_path):
 src=tmp_path/'input.json';src.write_text(json.dumps(d,ensure_ascii=False));out=tmp_path/'out.docx';script='generate_evidence.py' if skill.endswith('analyzer') else 'generate_review.py';r=subprocess.run([sys.executable,str(ROOT/skill/'scripts'/script),'--input',str(src),'--output',str(out)],cwd=tmp_path,capture_output=True,text=True);return r,out

def test_analysis_real_content_in_docx(tmp_path):
 skill='tw-edu-learning-evidence-analyzer';d=json.loads((ROOT/skill/'examples/example.json').read_text());d['content']=data();r,out=invoke(skill,d,tmp_path);assert r.returncode==0,r.stderr
 counts=json.loads(out.with_suffix('.analysis.json').read_text());assert counts['class_n']==3 and counts['items'][0]['correct_n']==1
 doc=Document(out);assert '概念' in '\n'.join(cell.text for table in doc.tables for row in table.rows for cell in row.cells)
@pytest.mark.parametrize('defect',['unlocated','unknown_severity'])
def test_reviewer_unlocated_or_fake_certainty_rejected(tmp_path,defect):
 skill='tw-edu-material-reviewer';d=json.loads((ROOT/skill/'examples/example.json').read_text())
 if defect=='unlocated':d['content']['findings'][0]['quote']='未出現的字'
 else:d['content']['findings'][0]['status']='unknown'
 r,out=invoke(skill,d,tmp_path);assert r.returncode==2 and not out.exists()

def test_csv_import_missing_and_duplicate_ids(tmp_path):
 skill='tw-edu-learning-evidence-analyzer';d=json.loads((ROOT/skill/'examples/example.json').read_text());src=tmp_path/'items.json';src.write_text(json.dumps(d));csv=tmp_path/'responses.csv';csv.write_text('student_id,Q1\nS1,A\nS2,\n');out=tmp_path/'merged.json';cmd=[sys.executable,str(ROOT/skill/'scripts/import_responses.py'),'--csv',str(csv),'--items',str(src),'--output',str(out)]
 r=subprocess.run(cmd,cwd=tmp_path,capture_output=True,text=True);assert r.returncode==0,r.stderr;merged=json.loads(out.read_text());assert merged['content']['responses'][1]['answers']['Q1'] is None
 csv.write_text('student_id,Q1\nS1,A\nS1,B\n');out.unlink();r=subprocess.run(cmd,cwd=tmp_path,capture_output=True,text=True);assert r.returncode==2 and not out.exists()
