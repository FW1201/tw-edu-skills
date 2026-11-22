"""Declarative DOCX layouts for v5 skills.

Each section is (key, heading, kind, spec):
  text   - a string paragraph
  list   - list of strings as bullets
  table  - list of objects; spec = [(field, header, weight), ...]
  fields - one object as a two-column table; spec = [(field, label), ...]
  group  - object whose fields are lists; spec = [(field, subheading), ...]
Missing optional keys are skipped. Nested keys use dotted paths.
"""
from __future__ import annotations

from .docstyle import add_table


def _get(data, path):
    for part in path.split('.'):
        if not isinstance(data, dict) or part not in data: return None
        data = data[part]
    return data


def _fmt(value):
    if value is None: return ''
    if isinstance(value, bool): return '是' if value else '否'
    if isinstance(value, list): return '\n'.join(_fmt(v) for v in value)
    if isinstance(value, dict): return '；'.join(f'{k}：{_fmt(v)}' for k, v in value.items())
    if isinstance(value, float) and value.is_integer(): return str(int(value))
    return str(value)


def render(doc, d, layout):
    c = d['content']
    for key, heading, kind, spec in layout:
        value = _get(c, key)
        if value in (None, [], {}): continue
        doc.add_heading(heading, 1)
        if kind == 'text': doc.add_paragraph(_fmt(value))
        elif kind == 'list':
            for item in value: doc.add_paragraph(_fmt(item), style='List Bullet')
        elif kind == 'table':
            add_table(doc, [h for _, h, _ in spec], [[_fmt(row.get(f)) for f, _, _ in spec] for row in value], [w for _, _, w in spec])
        elif kind == 'fields':
            add_table(doc, ['項目', '內容'], [[label, _fmt(value.get(f))] for f, label in spec if f in value], [1, 4])
        elif kind == 'group':
            for f, sub in spec:
                if value.get(f):
                    doc.add_heading(sub, 2)
                    for item in value[f]: doc.add_paragraph(_fmt(item), style='List Bullet')


def _horizon_sorted(items, order):
    return sorted(items, key=lambda x: order.index(x['horizon']) if x['horizon'] in order else 99)


LAYOUTS = {
'tw-edu-homeroom-operations': [
    ('period', '適用期間', 'text', None), ('class_profile', '班級概況（匿名）', 'text', None),
    ('boundaries', '權責分流', 'group', [('admin_procedures', '行政程序（依學校權責單位）'), ('class_decisions', '班級慣例（導師與學生共同決定）')]),
    ('routines', '例行程序', 'table', [('name', '程序', 2), ('owner', '負責', 1), ('when', '時機', 1), ('steps', '步驟', 4), ('check', '檢核方式', 2)]),
    ('roles', '幹部與職務', 'table', [('role', '職務', 2), ('tasks', '任務', 3), ('authority', '權限', 2), ('rotation', '輪替', 1), ('support', '教師支持', 2)]),
    ('attendance', '出缺勤與預警', 'fields', [('daily_check', '每日確認'), ('follow_up', '缺席追蹤'), ('alert_threshold', '預警門檻'), ('notify', '通報與通知對象'), ('basis', '依據')]),
    ('communication', '親師溝通管道', 'table', [('channel', '管道', 1), ('purpose', '用途', 3), ('frequency', '頻率', 1), ('privacy_rule', '隱私規則', 3)]),
    ('device_agreement', '載具與手機約定', 'list', None),
    ('timeline', '時間軸', 'table', [('when', '時間', 1), ('tasks', '工作', 5)]),
    ('handover', '交接包', 'fields', [('strengths', '班級優勢'), ('ongoing_supports', '持續中的支持'), ('records_location', '紀錄位置'), ('privacy_note', '隱私說明')]),
    ('pending', '待確認事項', 'list', None)],
'tw-edu-behavior-support': [
    ('student_alias', '學生代碼', 'text', None), ('behavior_definition', '目標行為（可觀察描述）', 'text', None),
    ('strengths', '學生優勢', 'list', None),
    ('baseline', '基線資料', 'fields', [('period', '觀察期間'), ('frequency', '頻率／強度'), ('settings', '發生情境')]),
    ('abc_records', 'ABC 紀錄', 'table', [('when', '時間', 1), ('antecedent', '前事 A', 3), ('behavior', '行為 B', 3), ('consequence', '後果 C', 3)]),
    ('function_hypotheses', '功能假設（待驗證）', 'table', [('id', '編號', 1), ('function', '可能功能', 2), ('statement', '假設敘述', 4), ('evidence_for', '支持證據', 3), ('evidence_against', '反向證據', 3), ('status', '狀態', 1)]),
    ('support_tier', '支持層級', 'text', None),
    ('prevention', '前事調整（預防）', 'list', None),
    ('replacement_behavior', '替代行為教學', 'fields', [('behavior', '替代行為'), ('teaching_steps', '教學步驟'), ('reinforcement', '增強方式')]),
    ('response_plan', '行為發生時的回應', 'table', [('situation', '情況', 2), ('teacher_response', '教師回應', 4)]),
    ('review', '資料蒐集與再檢核', 'fields', [('method', '方法'), ('owner', '負責'), ('review_date', '檢核日期')]),
    ('stop_conditions', '停止、調整或轉介條件', 'list', None),
    ('collaboration', '協作分工', 'table', [('who', '角色', 1), ('role', '負責內容', 4)]),
    ('safety_check', '安全檢核', 'fields', [('red_flags_present', '有無紅旗'), ('note', '說明')])],
'tw-edu-incident-response': [
    ('incident_type', '事件類型', 'text', None),
    ('facts', '中性事實紀錄', 'table', [('time', '時間', 1), ('location', '地點', 1), ('description', '經過（不含評價）', 5), ('source', '資訊來源', 1)]),
    ('red_flags', '紅旗篩檢', 'fields', [('bullying', '疑似霸凌'), ('gender_equity', '疑似校園性別事件'), ('child_protection', '兒少保護'), ('self_harm_or_violence', '自傷或傷人'), ('campus_safety', '校安事件'), ('notes', '說明')]),
    ('immediate_safety', '立即安全措施', 'list', None),
    ('reporting', '通報與交接', 'table', [('route', '通報途徑', 2), ('recipient', '對象', 2), ('deadline', '時限', 1), ('basis', '依據', 2), ('status', '狀態', 1)]),
    ('not_alone', '導師不可獨自決定的事項', 'list', None),
    ('restorative', '修復式對話', 'fields', [('eligible', '是否適用'), ('reason', '理由'), ('steps', '步驟')]),
    ('communication', '溝通安排', 'table', [('party', '對象', 1), ('channel', '管道', 1), ('boundary', '可說明範圍', 4)]),
    ('follow_up', '後續追蹤', 'table', [('action', '行動', 4), ('owner', '負責', 1), ('due', '期限', 1)]),
    ('case_status', '目前狀態', 'text', None)],
'tw-edu-student-guidance-advice': [
    ('student_alias', '學生代碼', 'text', None),
    ('profile', '學生概況', 'fields', [('grade_band', '年段'), ('context', '背景脈絡'), ('strengths', '優勢'), ('known_supports', '既有支持')]),
    ('timeline', '時間序事件', 'table', [('date', '時間', 1), ('event', '事件', 5), ('source', '來源', 1)]),
    ('teacher_view', '教師看法（原文）', 'text', None),
    ('analysis', '三欄區分', 'group', [('facts', '已知事實'), ('teacher_interpretations', '教師詮釋'), ('ai_inferences', 'AI 推論（待驗證）')]),
    ('patterns', '模式', 'list', None), ('turning_points', '轉折點', 'list', None),
    ('protective_factors', '保護因子', 'list', None), ('risk_factors', '風險因子', 'list', None),
    ('hypotheses', '需求假設（互斥解釋）', 'table', [('id', '編號', 1), ('explanation', '解釋', 4), ('supporting', '支持', 3), ('contradicting', '不支持', 3), ('check', '如何查證', 3)]),
    ('red_flag_screen', '紅旗篩檢', 'fields', [('triggered', '是否觸發'), ('flags', '項目'), ('action', '處置')]),
    ('actions', '分層建議行動', 'table', [('horizon', '時程', 1), ('action', '行動', 4), ('owner', '負責', 1), ('observe', '觀察指標', 3)]),
    ('referral', '轉介判斷', 'fields', [('recommended', '建議轉介'), ('to', '對象'), ('reason', '理由')]),
    ('monitoring', '持續觀察指標', 'list', None), ('limits', '本分析限制', 'list', None)],
'tw-edu-guidance-collaboration': [
    ('mode', '協作類型', 'text', None), ('student_alias', '學生代碼', 'text', None),
    ('concern', '關切需求', 'text', None), ('observation_period', '觀察期間', 'text', None),
    ('teacher_actions', '導師已採取的措施', 'table', [('action', '措施', 3), ('period', '期間', 1), ('result', '結果', 3)]),
    ('evidence', '觀察證據', 'table', [('type', '類型', 1), ('summary', '摘要', 4), ('source', '來源', 1)]),
    ('student_strengths', '學生優勢', 'list', None), ('requested_support', '期待支持', 'list', None),
    ('class_adjustments', '班級融合調整', 'table', [('area', '面向', 1), ('adjustment', '調整', 5)]),
    ('meeting_agenda', '會議議程（導師提案）', 'list', None), ('questions_for_team', '請團隊協助釐清', 'list', None),
    ('information_sharing', '資料分享評估', 'table', [('item', '資料', 2), ('share_with', '對象', 2), ('reason', '理由', 3), ('level', '層級', 1)]),
    ('privacy_notes', '隱私與同意', 'list', None),
    ('follow_up', '後續分工', 'table', [('action', '行動', 4), ('owner', '負責', 1), ('due', '期限', 1)])],
'tw-edu-lesson-design-brainstorm': [
    ('topic_input', '起點議題', 'text', None), ('learners', '學習者', 'text', None), ('constraints', '條件限制', 'list', None),
    ('divergence', '發散', 'group', [('student_connections', '學生經驗連結'), ('authentic_contexts', '真實情境'), ('interdisciplinary_angles', '跨領域角度'), ('issues', '議題融入'), ('essential_questions', '核心問題')]),
    ('selected', '收斂選擇', 'fields', [('angle', '切入點'), ('rationale', '理由'), ('set_aside', '暫不採用')]),
    ('big_idea', '大概念', 'text', None),
    ('learning_focus', '學習重點與查核', 'table', [('domain', '領域', 1), ('kind', '類型', 1), ('code', '代碼', 1), ('description', '內容', 4), ('verified', '已查核', 1), ('verification_note', '查核說明', 2)]),
    ('evidence', '評量證據', 'table', [('task', '表現任務', 3), ('criteria', '成功準則', 3)]),
    ('activity_outline', '活動雛形', 'table', [('phase', '階段', 1), ('idea', '構想', 5), ('minutes', '分鐘', 1)]),
    ('open_questions', '待決定事項', 'list', None), ('next_skill', '建議接續', 'text', None)],
'tw-edu-school-curriculum-plan': [
    ('school_type', '學校類型', 'text', None), ('plan_type', '計畫類型', 'text', None),
    ('vision', '學校願景', 'text', None), ('student_image', '學生圖像', 'list', None),
    ('goals', '課程目標', 'table', [('id', '編號', 1), ('goal', '目標', 4), ('image_links', '對應學生圖像', 2)]),
    ('structure', '課程架構', 'table', [('grade', '年級', 1), ('course', '課程', 2), ('category', '類別', 2), ('periods_per_week', '週節數', 1), ('weeks', '週數', 1), ('goal_ids', '對應目標', 1)]),
    ('required_periods', '規定節數（輸入提供）', 'table', [('grade', '年級', 1), ('periods_per_week', '週節數', 1), ('source', '依據', 4)]),
    ('units', '單元規劃', 'table', [('course', '課程', 2), ('unit', '單元', 2), ('weeks', '週次', 1), ('learning_focus', '學習重點', 3), ('assessment', '評量', 2), ('issues', '議題', 1)]),
    ('review_process', '審議與備查流程', 'list', None), ('local_format_note', '縣市格式說明', 'text', None)],
'tw-edu-open-lesson': [
    ('stage', '階段', 'text', None),
    ('lesson_info', '授課資訊', 'fields', [('teacher_role', '授課教師'), ('class_info', '班級'), ('unit', '單元'), ('date', '日期')]),
    ('prep', '共同備課', 'fields', [('learning_goals', '學習目標'), ('student_prior', '學生先備'), ('observation_focus', '觀察焦點'), ('evidence_to_collect', '要蒐集的學習證據')]),
    ('prep.observers', '觀課分工', 'table', [('observer', '觀課者', 1), ('focus', '焦點', 3), ('position', '位置', 1)]),
    ('observations', '低推論觀察紀錄', 'table', [('time', '時間', 1), ('target', '對象', 1), ('behavior', '行為／對話', 5), ('artifact', '作品位置', 2), ('observer', '紀錄者', 1)]),
    ('debrief', '議課', 'group', [('facts', '事實'), ('interpretations', '詮釋'), ('learning_evidence', '學生學習證據'), ('next_trial', '下一輪試作')]),
    ('debrief.teacher_reflection', '授課教師省思', 'text', None),
    ('records_privacy', '紀錄與隱私', 'text', None)],
'tw-edu-school-affairs-meeting': [
    ('role', '我的角色', 'text', None), ('stage', '目前階段', 'text', None),
    ('notice', '通知內容', 'fields', [('received_date', '收到日期'), ('document', '文件'), ('stated_purpose', '載明目的'), ('deadline', '期限')]),
    ('deadlines', '時程與期限', 'table', [('item', '事項', 3), ('date', '日期', 1), ('basis', '依據', 3)]),
    ('rights_checklist', '程序權利檢核', 'table', [('item', '項目', 4), ('basis', '依據', 2), ('status', '狀態', 1)]),
    ('timeline', '事實時間序', 'table', [('date', '時間', 1), ('event', '事件', 5), ('source', '來源', 2)]),
    ('allegations', '檢舉事項與我的說明', 'table', [('id', '編號', 1), ('summary', '通知所載', 3), ('my_account', '我的事實說明', 4), ('evidence_available', '可提出資料', 2), ('evidence_to_request', '待申請資料', 2)]),
    ('statement_draft.opening', '陳述意見書：開頭', 'text', None),
    ('statement_draft.by_allegation', '陳述意見書：逐項說明', 'table', [('allegation_id', '事項', 1), ('statement', '說明', 6)]),
    ('statement_draft.context', '陳述意見書：教學脈絡', 'text', None),
    ('statement_draft.closing', '陳述意見書：結語', 'text', None),
    ('interview_prep', '訪談準備', 'table', [('likely_question', '可能問題', 3), ('answer_points', '事實要點', 4), ('cautions', '注意', 2)]),
    ('support_people', '陪同與支持', 'table', [('who', '人員', 2), ('role', '角色', 1)]),
    ('wellbeing_note', '照顧自己', 'text', None), ('limitations', '限制與提醒', 'list', None)],
'tw-edu-teacher-wellbeing': [
    ('situation', '目前處境', 'text', None),
    ('stressors', '壓力來源', 'table', [('source', '類型', 1), ('description', '描述', 5)]),
    ('signals', '身心訊號', 'list', None),
    ('risk_screen', '安全檢核', 'fields', [('self_harm_thoughts', '有傷害自己的念頭'), ('unable_to_function', '已難以維持日常'), ('note', '說明')]),
    ('strengths', '可依靠的力量', 'list', None), ('coping_now', '現在可以做的事', 'list', None),
    ('resources', '支持資源', 'table', [('resource', '資源', 2), ('access', '如何取得', 3), ('note', '備註', 2)]),
    ('boundaries', '工作界線', 'list', None),
    ('scripts', '溝通腳本', 'table', [('situation', '情境', 2), ('script', '可以這樣說', 5)]),
    ('records_habits', '保護性紀錄習慣', 'list', None),
    ('plan', '行動計畫', 'table', [('horizon', '時程', 1), ('action', '行動', 5)]),
    ('follow_up', '回顧時間', 'text', None)],
'tw-edu-classroom-culture': [
    ('norms', '班級規範三層', 'group', [('safety_floor', '安全底線（不交付表決）'), ('shared_agreements', '共同協議'), ('choices', '可選擇事項')]),
    ('rituals', '可預期的儀式', 'table', [('moment', '時機', 1), ('practice', '做法', 5)]),
    ('routines', '日常程序', 'table', [('situation', '情境', 2), ('steps', '步驟', 5)]),
    ('relationship_practices', '關係經營', 'list', None),
    ('class_activities', '班級活動', 'table', [('name', '活動', 2), ('purpose', '目的', 3), ('frequency', '頻率', 1)]),
    ('student_voice', '學生參與方式', 'list', None),
    ('repair_paths', '修復路徑', 'table', [('situation', '情況', 2), ('steps', '步驟', 5)]),
    ('response_plan', '事件回應計畫', 'table', [('trigger', '觸發情況', 2), ('teacher_action', '教師行動', 3), ('follow_up', '後續追蹤', 3)])],
'tw-edu-parent-communication': [
    ('send_status', '狀態', 'text', None),
    ('audience', '對象範圍', 'text', None), ('channel', '溝通管道', 'text', None), ('sensitivity', '敏感程度', 'text', None),
    ('recipients', '收件對象', 'list', None), ('purpose', '溝通目的', 'text', None),
    ('facts', '已知事實', 'list', None), ('concerns', '教師關切（推論）', 'list', None),
    ('message', '訊息內容', 'text', None), ('requested_action', '期待配合事項', 'text', None),
    ('meeting_plan', '會談或班親會安排', 'fields', [('date', '日期'), ('agenda', '流程'), ('roles', '分工')]),
    ('contact_channel', '聯絡管道', 'text', None), ('pending', '待確認事項', 'list', None)],
'tw-edu-school-document': [
    ('document_type', '文件類型', 'text', None), ('approval_status', '核定狀態', 'text', None),
    ('basis', '依據', 'list', None), ('purpose', '目的', 'list', None),
    ('implementation', '實施方式', 'table', [('item', '項目', 2), ('details', '內容', 5)]),
    ('schedule', '期程', 'table', [('date', '日期', 1), ('item', '工作', 4)]),
    ('responsible_people', '權責分工', 'list', None),
    ('budget', '經費概算', 'table', [('item', '項目', 2), ('amount', '金額（新臺幣元）', 1), ('unit', '單位說明', 1), ('basis', '計算依據', 3)]),
    ('total_budget', '經費合計（新臺幣元）', 'text', None), ('funding_source', '經費來源', 'text', None),
    ('expected_results', '預期成果', 'list', None),
    ('results', '成果與證據', 'table', [('indicator', '指標', 2), ('target', '目標', 1), ('actual', '實際', 1), ('evidence', '證據', 3)]),
    ('pending', '待確認事項', 'list', None)],
'tw-edu-meeting-facilitator': [
    ('record_status', '紀錄狀態', 'text', None), ('meeting_type', '會議類型', 'text', None),
    ('date', '日期', 'text', None), ('duration_minutes', '會議時長（分鐘）', 'text', None),
    ('participants', '出席人員', 'list', None),
    ('agenda', '議程', 'table', [('kind', '類別', 1), ('topic', '議題', 4), ('minutes', '分鐘', 1), ('owner', '負責', 1)]),
    ('reports', '報告事項', 'table', [('unit', '單位', 1), ('summary', '報告摘要', 4), ('decision', '決定', 2)]),
    ('discussions', '討論事項', 'table', [('case_no', '案次', 1), ('proposer', '提案', 1), ('cause', '案由', 3), ('explanation', '說明', 3), ('resolution', '決議', 3), ('status', '狀態', 1)]),
    ('actions', '執行追蹤', 'table', [('action', '事項', 4), ('owner', '執行單位', 1), ('due', '期限', 1)])],
}
