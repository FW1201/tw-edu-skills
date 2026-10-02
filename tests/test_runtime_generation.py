from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
PY=Path(sys.executable)
GENERATORS={
"tw-edu-learning-evidence-analyzer":"generate_evidence.py", "tw-edu-material-reviewer":"generate_review.py",
"tw-edu-anti-ai-assessment":"generate_anti_ai_report.py","tw-edu-classroom-culture":"generate_classroom.py","tw-edu-curriculum-mapper":"generate_curriculum_map.py","tw-edu-differentiated":"generate_differentiated.py","tw-edu-exam-generator":"generate_exam.py","tw-edu-feedback-writer":"generate_feedback.py","tw-edu-formative-assessment":"generate_formative.py","tw-edu-interdisciplinary":"generate_interdisciplinary.py","tw-edu-learning-portfolio":"generate_portfolio.py","tw-edu-lesson-plan-108":"generate_lesson_plan.py","tw-edu-meeting-facilitator":"generate_meeting.py","tw-edu-mini-app":"generate_mini_app.py","tw-edu-parent-communication":"generate_parent_comm.py","tw-edu-pbl-designer":"generate_pbl.py","tw-edu-research-viz":"generate_prisma.py","tw-edu-rubric-designer":"generate_rubric.py","tw-edu-school-document":"generate_school_doc.py","tw-edu-slides-creator":"generate_slides.py","tw-edu-worksheet-creator":"generate_worksheet.py"}
EXT={"tw-edu-curriculum-mapper":".xlsx","tw-edu-mini-app":".html","tw-edu-research-viz":".png","tw-edu-slides-creator":".pptx"}
def invoke(skill,*args,cwd=None):
    env=os.environ.copy(); env.setdefault("MPLCONFIGDIR","/private/tmp/tw-edu-mpl"); env.setdefault("XDG_CACHE_HOME","/private/tmp/tw-edu-cache")
    return subprocess.run([str(PY),str(ROOT/skill/"scripts"/GENERATORS[skill]),*map(str,args)],cwd=cwd,text=True,capture_output=True,env=env)

@pytest.mark.parametrize("skill",GENERATORS)
def test_every_generator_example_and_arbitrary_cwd(skill,tmp_path):
    out=tmp_path/("result"+EXT.get(skill,".docx")); r=invoke(skill,"--example","--output",out,cwd=tmp_path)
    assert r.returncode==0,r.stderr
    if skill=="tw-edu-exam-generator":
        assert (tmp_path/"result-student.docx").exists() and (tmp_path/"result-teacher.docx").exists()
    else: assert out.exists()

@pytest.mark.parametrize("skill",GENERATORS)
def test_bad_input_creates_no_output(skill,tmp_path):
    bad=tmp_path/"bad.json"; bad.write_text('{}'); out=tmp_path/("bad"+EXT.get(skill,".docx"))
    r=invoke(skill,"--input",bad,"--output",out); assert r.returncode!=0; assert not out.exists()

def test_exam_student_has_no_answers(tmp_path):
    from docx import Document
    out=tmp_path/"exam.docx"; r=invoke("tw-edu-exam-generator","--example","--output",out); assert r.returncode==0
    student="\n".join(p.text for p in Document(tmp_path/"exam-student.docx").paragraphs)
    teacher="\n".join(p.text for p in Document(tmp_path/"exam-teacher.docx").paragraphs)
    assert "答案：A" not in student and "答案：A" in teacher

def test_lesson_bad_minutes_no_output(tmp_path):
    skill="tw-edu-lesson-plan-108"; data=json.loads((ROOT/skill/"examples/example.json").read_text()); data["content"]["total_minutes"]=99
    inp=tmp_path/"x.json"; inp.write_text(json.dumps(data)); out=tmp_path/"x.docx"; r=invoke(skill,"--input",inp,"--output",out)
    assert r.returncode!=0 and not out.exists()

def test_input_content_changes_output(tmp_path):
    from docx import Document
    skill="tw-edu-feedback-writer"; data=json.loads((ROOT/skill/"examples/example.json").read_text()); data["context"]={"subject":"數學","grade":"高中二年級","topic":"二次函數"}; data["content"]["students"][0]["observations"]=["學生能由圖形判讀頂點"]
    inp=tmp_path/"x.json"; inp.write_text(json.dumps(data,ensure_ascii=False)); out=tmp_path/"x.docx"; assert invoke(skill,"--input",inp,"--output",out).returncode==0
    doc=Document(out); text="\n".join([*(p.text for p in doc.paragraphs),*(cell.text for table in doc.tables for row in table.rows for cell in row.cells)])
    assert "學生能由圖形判讀頂點" in text and "高中二年級" in text

def test_task_specific_schemas_are_not_generic_blocks():
    expected={"tw-edu-feedback-writer":"students","tw-edu-learning-portfolio":"records","tw-edu-parent-communication":"recipients","tw-edu-formative-assessment":"checks","tw-edu-worksheet-creator":"prompts"}
    for skill,field in expected.items():
        schema=json.loads((ROOT/skill/"schemas/input.schema.json").read_text()); required=schema["properties"]["content"]["required"]
        assert field in required and "sections" not in required
