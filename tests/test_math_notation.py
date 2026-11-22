import json
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

from test_runtime_generation import ROOT, invoke

NS = {"m":"http://schemas.openxmlformats.org/officeDocument/2006/math", "w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

def document(path):
    with ZipFile(path) as archive:
        return ET.fromstring(archive.read("word/document.xml"))

def test_fraction_and_radical_nesting_and_inline_export(tmp_path):
    skill = "tw-edu-math-composing"
    source=json.loads((ROOT/skill/"examples/example.json").read_text())
    source["content"]["layout"]={"mode":"single"}
    source["content"]["items"]=[
        {"id":"A1","prompt":"原長 3/4 公尺，剪去 1/4 公尺。","answer":"答案為 3√2。",
         "formula":{"latex":r"\frac{\sqrt{3}}2","parts":[{"frac":[{"rad":"3"},"2"]}]}},
        {"id":"A2","prompt":"比較根式範圍。",
         "formula":{"latex":r"\sqrt{\frac32}","parts":[{"rad":{"frac":["3","2"]}}]}},
        {"id":"A3","prompt":"7/8 日登記，參考 https://example.org/3/4。"},
    ]
    path=tmp_path/"input.json";path.write_text(json.dumps(source,ensure_ascii=False))
    result=invoke(skill,"--input",path,"--output",tmp_path/"math.docx")
    assert result.returncode==0,result.stderr
    student=document(tmp_path/"math-student.docx")
    teacher=document(tmp_path/"math-teacher.docx")
    assert student.find(".//m:f/m:num/m:rad/m:e/m:r/m:t",NS).text=="3"
    assert student.find(".//m:rad/m:e/m:f/m:den/m:r/m:t",NS).text=="2"
    inline=next(p for p in student.findall(".//w:p",NS) if "原長" in "".join(p.itertext()))
    assert len(inline.findall("./m:oMath/m:f",NS))==2
    assert "7/8 日" in "".join(student.itertext()) and "https://example.org/3/4" in "".join(student.itertext())
    assert "答案為" not in "".join(student.itertext()) and "答案為" in "".join(teacher.itertext())
    assert len(teacher.findall(".//m:rad",NS))==len(student.findall(".//m:rad",NS))+1

def test_math_worksheet_inline_objects(tmp_path):
    skill="tw-edu-worksheet-creator"
    source=json.loads((ROOT/skill/"examples/example.json").read_text())
    source["context"]["subject"]="數學"
    source["content"]["prompts"][0].update(prompt="原長 3/4 公尺，剪去 1/4 公尺。")
    path=tmp_path/"worksheet.json";path.write_text(json.dumps(source,ensure_ascii=False))
    result=invoke(skill,"--input",path,"--output",tmp_path/"worksheet.docx")
    assert result.returncode==0,result.stderr
    xml=document(tmp_path/"worksheet.docx")
    assert len(xml.findall(".//m:f",NS))==2
    assert "3/4" not in "".join(xml.itertext())


def test_graph_label_exports_its_radical_and_fraction_strokes(tmp_path):
    import subprocess
    import sys

    skill = ROOT/"tw-edu-math-composing"
    source={"version":1,"title":"根式圖例","stage":"高中","purpose":"數學圖文","items":[{
        "id":"F1","prompt":"根式圖例","figure":{"size":[200,100],"alt":"根號三除以二",
            "math_labels":[[15,45,[{"op":"sin"},"(120°) = ",{"frac":[{"rad":"3"},"2"]}]]]}}]}
    path=tmp_path/"graph.json";path.write_text(json.dumps(source,ensure_ascii=False))
    output=tmp_path/"svg"
    result=subprocess.run([sys.executable,str(skill/"scripts/compose.py"),str(path),
                           "--figures-only","--output",str(output)],capture_output=True,text=True)
    assert result.returncode == 0,result.stderr
    svg=ET.parse(output/"F1.svg")
    ns={"s":"http://www.w3.org/2000/svg"}
    assert [x.text for x in svg.findall(".//s:text",ns)] == ["sin","(120°) = ","3","2"]
    lines=svg.findall(".//s:polyline",ns)
    assert sorted(len(line.get("points").split()) for line in lines)==[2,5]
