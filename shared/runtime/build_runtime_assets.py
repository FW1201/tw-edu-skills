#!/usr/bin/env python3
"""Generate task-specific schemas/examples and self-contained runtime copies."""
from __future__ import annotations
import json, shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE={"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","additionalProperties":False,"required":["schema_version","skill","language","context","sources","content"],"properties":{"schema_version":{"const":"1.0"},"skill":{"type":"string"},"language":{"const":"zh-TW"},"context":{"type":"object","additionalProperties":False,"required":["subject","grade","topic"],"properties":{"subject":{"type":"string","minLength":1},"grade":{"type":"string","minLength":1},"topic":{"type":"string","minLength":1}}},"sources":{"type":"array","items":{"type":"object","additionalProperties":False,"required":["title","status"],"properties":{"title":{"type":"string","minLength":1},"url":{"type":"string"},"status":{"enum":["verified","user_provided","pending"]}}}},"content":{}}}
S={"type":"string","minLength":1}; POS={"type":"integer","minimum":1}; NUM={"type":"number","minimum":0}
def obj(req,props,extra=False): return {"type":"object","additionalProperties":extra,"required":req,"properties":props}
def arr(item,minn=1): return {"type":"array","minItems":minn,"items":item}
def base(skill,content):
    x=json.loads(json.dumps(BASE)); x["properties"]["skill"]={"const":skill}; x["properties"]["content"]=content
    if skill=="tw-edu-mini-app":
        x["properties"]["content"]["allOf"]=[{"if":{"properties":{"mode":{"const":m}}},"then":{"required":[field]}} for m,field in [("quiz","questions"),("flashcard","cards"),("lottery","entries"),("timer","seconds")]]
    if skill=="tw-edu-research-viz": x["properties"]["content"]["allOf"]=[{"if":{"properties":{"type":{"const":"prisma"}}},"then":{"required":["prisma"]}},{"if":{"properties":{"type":{"const":"simple_diagram"}}},"then":{"required":["nodes"]}}]
    if skill=="tw-edu-slides-creator":
        item=x["properties"]["content"]["properties"]["slides"]["items"]
        item["allOf"]=[{"if":{"properties":{"type":{"const":t}}},"then":{"required":[field]}} for t,field in [("text","body"),("table","table"),("chart","chart"),("image","image")]]
    return x
def envelope(skill,content): return {"schema_version":"1.0","skill":skill,"language":"zh-TW","context":{"subject":"國語文","grade":"國中八年級","topic":"環境觀察"},"sources":[{"title":"教師提供教材","status":"user_provided"}],"content":content}

generic_fields={"title":S,"purpose":S,"sections":arr(obj(["heading","body"],{"heading":S,"body":S})),"activities":arr(obj(["name","instructions"],{"name":S,"instructions":S,"materials":arr(S)})),"notes":S}
skills={
"tw-edu-lesson-plan-108":obj(["title","total_minutes","objectives","activities","assessments"],{"title":S,"total_minutes":POS,"objectives":arr(obj(["id","description"],{"id":S,"description":S})),"activities":arr(obj(["id","title","minutes","instructions","objective_ids"],{"id":S,"title":S,"minutes":POS,"instructions":S,"objective_ids":arr(S)})),"assessments":arr(obj(["id","method","criteria","objective_ids"],{"id":S,"method":S,"criteria":S,"objective_ids":arr(S)})),"curriculum_codes":arr(obj(["code","description","verified"],{"code":S,"description":S,"verified":{"type":"boolean"},"verification_note":S}),0)}),
"tw-edu-curriculum-mapper":obj(["title","units"],{"title":S,"units":arr(obj(["name","weeks","periods","goals","codes","assessments"],{"name":S,"weeks":S,"periods":POS,"goals":arr(S),"codes":arr(obj(["code","description","verified"],{"code":S,"description":S,"verified":{"type":"boolean"},"verification_note":S}),0),"assessments":arr(S)}))}),
"tw-edu-exam-generator":obj(["title","expected_question_count","total_points","questions"],{"title":S,"expected_question_count":POS,"total_points":{"type":"number","exclusiveMinimum":0},"questions":arr(obj(["id","type","prompt","points","answer"],{"id":S,"type":{"enum":["multiple_choice","short_answer","essay","true_false"]},"prompt":S,"points":{"type":"number","exclusiveMinimum":0},"options":arr(obj(["id","text"],{"id":S,"text":S}),2),"answer":S,"explanation":S}))}),
"tw-edu-rubric-designer":obj(["title","type","total_points","levels"],{"title":S,"type":{"enum":["analytic","holistic"]},"total_points":{"type":"number","exclusiveMinimum":0},"levels":arr(obj(["id","label","score"],{"id":S,"label":S,"score":NUM}),2),"dimensions":arr(obj(["id","name","weight","descriptions"],{"id":S,"name":S,"weight":{"type":"number","exclusiveMinimum":0},"descriptions":{"type":"object","additionalProperties":S}})),"descriptions":{"type":"object","additionalProperties":S}},),
"tw-edu-mini-app":obj(["title","mode"],{"title":S,"mode":{"enum":["quiz","flashcard","lottery","timer"]},"questions":arr(obj(["id","prompt","points","options","answer"],{"id":S,"prompt":S,"points":{"type":"number","exclusiveMinimum":0},"options":arr(obj(["id","text"],{"id":S,"text":S}),2),"answer":S})),"cards":arr(obj(["front","back"],{"front":S,"back":S})),"entries":arr(S),"seconds":POS},),
"tw-edu-research-viz":obj(["title","type"],{"title":S,"type":{"enum":["prisma","simple_diagram"]},"prisma":obj(["identified","duplicates_removed","screened","screening_excluded","full_text_assessed","full_text_excluded","included"],{k:NUM for k in ["identified","duplicates_removed","screened","screening_excluded","full_text_assessed","full_text_excluded","included"]}),"nodes":arr(obj(["id","label"],{"id":S,"label":S,"value":S}))}),
"tw-edu-slides-creator":obj(["title","slides"],{"title":S,"slides":arr(obj(["id","type","title"],{"id":POS,"type":{"enum":["text","table","chart"]},"title":S,"body":arr(S),"table":arr(arr(S),2),"chart":obj(["categories","series"],{"categories":arr(S),"series":arr(obj(["name","values"],{"name":S,"values":arr(NUM)}))}),"notes":S}))}),
"tw-edu-anti-ai-assessment":obj(["title","items"],{"title":S,"items":arr(obj(["id","assessment_item","dimensions","total_score","reason"],{"id":S,"assessment_item":S,"dimensions":arr(obj(["name","score","reason"],{"name":S,"score":NUM,"reason":S})),"total_score":NUM,"reason":S,"redesign":S}))}),
}
activity=obj(["id","title","instructions"],{"id":S,"title":S,"instructions":S,"materials":arr(S,0)})
skills.update({
"tw-edu-feedback-writer":obj(["title","students"],{"title":S,"students":arr(obj(["student_id","observations","strengths","next_steps","feedback"],{"student_id":S,"observations":arr(S),"strengths":arr(S),"next_steps":arr(S),"feedback":S}))}),
"tw-edu-learning-portfolio":obj(["title","records"],{"title":S,"records":arr(obj(["date","artifact","evidence","reflection","next_step"],{"date":S,"artifact":S,"evidence":S,"reflection":S,"next_step":S}))}),
"tw-edu-classroom-culture":obj(["title","agreements","routines","response_plan"],{"title":S,"agreements":arr(S),"routines":arr(obj(["situation","steps"],{"situation":S,"steps":arr(S)})),"response_plan":arr(obj(["trigger","teacher_action","follow_up"],{"trigger":S,"teacher_action":S,"follow_up":S}))}),
"tw-edu-differentiated":obj(["title","shared_goal","learner_groups","activities"],{"title":S,"shared_goal":S,"learner_groups":arr(obj(["id","evidence","support"],{"id":S,"evidence":S,"support":arr(S)})),"activities":arr(activity)}),
"tw-edu-formative-assessment":obj(["title","learning_target","checks","response_rules"],{"title":S,"learning_target":S,"checks":arr(obj(["id","prompt","success_criteria","evidence_capture"],{"id":S,"prompt":S,"success_criteria":arr(S),"evidence_capture":S})),"response_rules":arr(obj(["evidence","action"],{"evidence":S,"action":S}))}),
"tw-edu-interdisciplinary":obj(["title","disciplines","driving_question","discipline_contributions","activities","product"],{"title":S,"disciplines":arr(S,2),"driving_question":S,"discipline_contributions":arr(obj(["discipline","knowledge","method"],{"discipline":S,"knowledge":S,"method":S}),2),"activities":arr(activity),"product":S}),
"tw-edu-meeting-facilitator":obj(["title","participants","agenda","decisions","actions"],{"title":S,"participants":arr(S),"agenda":arr(obj(["topic","minutes","owner"],{"topic":S,"minutes":POS,"owner":S})),"decisions":arr(S,0),"actions":arr(obj(["owner","action","due"],{"owner":S,"action":S,"due":S}),0)}),
"tw-edu-parent-communication":obj(["title","recipients","purpose","message","requested_action","contact_channel"],{"title":S,"recipients":arr(S),"purpose":S,"message":S,"requested_action":S,"contact_channel":S}),
"tw-edu-pbl-designer":obj(["title","driving_question","authentic_context","milestones","final_product","assessment_criteria"],{"title":S,"driving_question":S,"authentic_context":S,"milestones":arr(obj(["id","deliverable","due","feedback"],{"id":S,"deliverable":S,"due":S,"feedback":S})),"final_product":S,"assessment_criteria":arr(S)}),
"tw-edu-school-document":obj(["title","document_type","basis","purpose","implementation","responsible_people","expected_results"],{"title":S,"document_type":{"enum":["plan","memo","report","application","curriculum"]},"basis":arr(S),"purpose":arr(S),"implementation":arr(obj(["item","details"],{"item":S,"details":S})),"responsible_people":arr(S),"expected_results":arr(S)}),
"tw-edu-worksheet-creator":obj(["title","instructions","prompts","reflection"],{"title":S,"instructions":S,"prompts":arr(obj(["id","prompt","response_space_lines"],{"id":S,"prompt":S,"response_space_lines":POS})),"reflection":S}),
})

examples={
"tw-edu-lesson-plan-108":{"title":"校園環境描寫教案（範例）","total_minutes":45,"objectives":[{"id":"O1","description":"辨識感官描寫"}],"activities":[{"id":"A1","title":"文本觀察","minutes":45,"instructions":"圈選文本中的感官詞語。","objective_ids":["O1"]}],"assessments":[{"id":"E1","method":"出口卡","criteria":"寫出一個感官句。","objective_ids":["O1"]}],"curriculum_codes":[{"code":"待確認","description":"由教師核對正式代碼","verified":False,"verification_note":"範例未連接官方課綱"}]},
"tw-edu-curriculum-mapper":{"title":"閱讀單元地圖（範例）","units":[{"name":"環境觀察","weeks":"1–2","periods":4,"goals":["辨識描寫細節"],"codes":[{"code":"待確認","description":"正式代碼由教師核對","verified":False,"verification_note":"範例未連接官方課綱"}],"assessments":["觀察紀錄"]}]},
"tw-edu-exam-generator":{"title":"閱讀理解測驗（範例）","expected_question_count":1,"total_points":10,"questions":[{"id":"Q1","type":"multiple_choice","prompt":"哪一項最符合文本主旨？","points":10,"options":[{"id":"A","text":"觀察環境"},{"id":"B","text":"計算距離"}],"answer":"A","explanation":"文本聚焦環境細節。"}]},
"tw-edu-rubric-designer":{"title":"短文評量規準（範例）","type":"analytic","total_points":10,"levels":[{"id":"L1","label":"達成","score":2},{"id":"L0","label":"待加強","score":1}],"dimensions":[{"id":"D1","name":"內容","weight":10,"descriptions":{"L1":"細節具體","L0":"細節不足"}}]},
"tw-edu-mini-app":{"title":"環境小測驗（範例）","mode":"quiz","questions":[{"id":"Q1","prompt":"哪個詞屬於聽覺描寫？","points":1,"options":[{"id":"A","text":"鳥鳴"},{"id":"B","text":"翠綠"}],"answer":"A"}]},
"tw-edu-research-viz":{"title":"文獻篩選（範例）","type":"prisma","prisma":{"identified":10,"duplicates_removed":2,"screened":8,"screening_excluded":3,"full_text_assessed":5,"full_text_excluded":2,"included":3}},
"tw-edu-slides-creator":{"title":"環境觀察簡報（範例）","slides":[{"id":1,"type":"text","title":"觀察與描寫","body":["從感官細節開始"],"notes":"請學生分享觀察。"},{"id":2,"type":"table","title":"感官整理","table":[["感官","例子"],["聽覺","鳥鳴"]],"notes":"比較不同感官。"},{"id":3,"type":"chart","title":"觀察統計","chart":{"categories":["視覺","聽覺"],"series":[{"name":"次數","values":[3,2]}]},"notes":"圖表資料為本範例。"}]},
"tw-edu-anti-ai-assessment":{"title":"評量設計檢視（範例）","items":[{"id":"I1","assessment_item":"記錄校園中的一個真實細節。","dimensions":[{"name":"現場證據","score":2,"reason":"要求可核對的課堂觀察紀錄。"}],"total_score":2,"reason":"分數描述任務設計特徵，不推定作弊。","redesign":"附上觀察時間與修訂紀錄。"}]},
}
examples.update({
"tw-edu-feedback-writer":{"title":"學習回饋（範例）","students":[{"student_id":"SAMPLE-01","observations":["能指出文本中的感官詞"],"strengths":["引用具體"],"next_steps":["補充效果說明"],"feedback":"你已能找出證據，下一步請說明這個詞帶來的感受。"}]},
"tw-edu-learning-portfolio":{"title":"學習歷程（範例）","records":[{"date":"2026-09-01","artifact":"觀察短文","evidence":"修訂前後版本","reflection":"我增加了聽覺細節。","next_step":"檢查段落銜接。"}]},
"tw-edu-classroom-culture":{"title":"班級文化（範例）","agreements":["發言前先聽完他人的理由"],"routines":[{"situation":"小組討論","steps":["確認角色","記錄共識"]}],"response_plan":[{"trigger":"討論中斷","teacher_action":"重述共同規範","follow_up":"課後檢視分工"}]},
"tw-edu-differentiated":{"title":"差異化教學（範例）","shared_goal":"以感官詞完成一段描寫","learner_groups":[{"id":"需要詞彙支持","evidence":"觀察紀錄詞彙少於三個","support":["提供感官詞卡"]}],"activities":[{"id":"A1","title":"分層描寫","instructions":"依支持卡完成短文。","materials":["詞卡"]}]},
"tw-edu-formative-assessment":{"title":"形成性評量（範例）","learning_target":"辨識並使用感官描寫","checks":[{"id":"C1","prompt":"圈出一個聽覺詞並說明效果。","success_criteria":["詞語正確","效果合理"],"evidence_capture":"出口卡"}],"response_rules":[{"evidence":"只圈詞未說明","action":"提供效果句型後再答一次"}]},
"tw-edu-interdisciplinary":{"title":"校園聲景（範例）","disciplines":["國語文","自然"],"driving_question":"如何用文字與測量呈現校園聲景？","discipline_contributions":[{"discipline":"國語文","knowledge":"感官描寫","method":"短文寫作"},{"discipline":"自然","knowledge":"聲音強弱","method":"定點觀測"}],"activities":[{"id":"A1","title":"聲景觀測","instructions":"記錄聲音與感受。","materials":["紀錄表"]}],"product":"聲景導覽頁"},
"tw-edu-meeting-facilitator":{"title":"備課會議（範例）","participants":["教師甲","教師乙"],"agenda":[{"topic":"共用評量標準","minutes":20,"owner":"教師甲"}],"decisions":["先試用一週"],"actions":[{"owner":"教師乙","action":"整理學生作品","due":"2026-09-10"}]},
"tw-edu-parent-communication":{"title":"學習近況通知（範例）","recipients":["八年一班家長"],"purpose":"說明本週觀察任務","message":"學生將完成校園觀察紀錄。","requested_action":"請提醒攜帶筆記本。","contact_channel":"班級聯絡簿"},
"tw-edu-pbl-designer":{"title":"校園環境提案（範例）","driving_question":"如何改善一處校園環境？","authentic_context":"向校務會議提出可行建議","milestones":[{"id":"M1","deliverable":"問題證據表","due":"第一週","feedback":"同儕檢核證據"}],"final_product":"三分鐘提案","assessment_criteria":["證據充分","方案可行"]},
"tw-edu-school-document":{"title":"校園觀察活動計畫（範例）","document_type":"plan","basis":["校本課程規劃"],"purpose":["培養觀察與表達能力"],"implementation":[{"item":"活動方式","details":"分組完成校園觀察紀錄"}],"responsible_people":["教學組"],"expected_results":["每組完成一份紀錄"]},
"tw-edu-worksheet-creator":{"title":"校園觀察學習單（範例）","instructions":"依序完成觀察與推論。","prompts":[{"id":"P1","prompt":"記錄一個聽到的聲音。","response_space_lines":3}],"reflection":"哪個細節最能支持你的感受？"},
})

wrappers={
"tw-edu-anti-ai-assessment":"generate_anti_ai_report.py","tw-edu-classroom-culture":"generate_classroom.py","tw-edu-curriculum-mapper":"generate_curriculum_map.py","tw-edu-differentiated":"generate_differentiated.py","tw-edu-exam-generator":"generate_exam.py","tw-edu-feedback-writer":"generate_feedback.py","tw-edu-formative-assessment":"generate_formative.py","tw-edu-interdisciplinary":"generate_interdisciplinary.py","tw-edu-learning-portfolio":"generate_portfolio.py","tw-edu-lesson-plan-108":"generate_lesson_plan.py","tw-edu-meeting-facilitator":"generate_meeting.py","tw-edu-mini-app":"generate_mini_app.py","tw-edu-parent-communication":"generate_parent_comm.py","tw-edu-pbl-designer":"generate_pbl.py","tw-edu-research-viz":"generate_prisma.py","tw-edu-rubric-designer":"generate_rubric.py","tw-edu-school-document":"generate_school_doc.py","tw-edu-slides-creator":"generate_slides.py","tw-edu-worksheet-creator":"generate_worksheet.py"}
slide_props = skills['tw-edu-slides-creator']['properties']
slide_props['mode'] = {'enum': ['editable', 'image'], 'default': 'editable'}
slide_item = slide_props['slides']['items']
slide_item['properties']['type']['enum'].append('image')
slide_item['properties']['image'] = S
skills['tw-edu-mini-app']['properties']['questions']['items']['properties']['explanation'] = S
skills['tw-edu-rubric-designer']['allOf'] = [
    {'if': {'properties': {'type': {'const': mode}}}, 'then': {'required': [field]}}
    for mode, field in [('analytic', 'dimensions'), ('holistic', 'descriptions')]]
for field in skills['tw-edu-research-viz']['properties']['prisma']['properties']:
    skills['tw-edu-research-viz']['properties']['prisma']['properties'][field] = {'type': 'integer', 'minimum': 0}
for skill,schema in skills.items():
    root=ROOT/skill; (root/"schemas").mkdir(exist_ok=True); (root/"examples").mkdir(exist_ok=True); (root/"scripts").mkdir(exist_ok=True)
    (root/"schemas"/"input.schema.json").write_text(json.dumps(base(skill,schema),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (root/"examples"/"example.json").write_text(json.dumps(envelope(skill,examples[skill]),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    target=root/"scripts"/"edu_runtime"; shutil.rmtree(target,ignore_errors=True); shutil.copytree(ROOT/"shared/runtime/edu_runtime",target)
    wrapper=root/"scripts"/wrappers[skill]
    wrapper.write_text(f'''#!/usr/bin/env python3\nfrom edu_runtime.cli import main\nif __name__ == "__main__":\n    raise SystemExit(main("{skill}"))\n''',encoding="utf-8")
