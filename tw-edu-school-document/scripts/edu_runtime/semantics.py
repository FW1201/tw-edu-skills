"""v5 semantic gates: rules that JSON Schema cannot express.

check(skill, data) raises ValueError for errors that must block output and
returns advisories (warnings) that are written to the validation report.
"""
from __future__ import annotations

import re
from typing import Any

ALIAS = re.compile(r'^(學生|個案|同學|生)?[A-Za-z0-9甲乙丙丁戊己庚辛壬癸\-]{1,6}$')
PUNITIVE = ['體罰', '罰站', '罰跪', '罰跑', '半蹲', '公開羞辱', '當眾', '連坐', '全班一起罰', '罰錢', '罰款', '不准吃飯', '不准上廁所', '不准喝水', '剝奪下課', '關在']
DIAGNOSIS = ['過動症', 'ADHD', '自閉症', '亞斯伯格', '憂鬱症', '躁鬱症', '人格障礙', '學習障礙', '對立反抗症', '思覺失調', '焦慮症']
LABELS = ['懶惰', '笨', '沒救', '壞孩子', '問題學生', '不受教', '屢勸不聽', '冥頑', '朽木', '劣根性', '過動兒']
GRADE_WORDS = ['甲等', '乙等', '丙等', '丁等', '優等', '等第', '操行成績']
EVALUATIVE = ['很好', '不錯', '很棒', '認真', '不認真', '優秀', '差勁', '混亂', '失控', '懶散', '表現佳', '表現差', '效果好', '效果不佳', '成功', '失敗']
ACCUSATORY = ['誣告', '惡意', '說謊', '造謠', '亂告', '濫訴', '報復']
OUTDATED_TERMS = ['惠請', '為要', '為荷', '實紉公誼', '乙案', '乙份', '似屬可行', '鑒核示遵']
CRISIS = ['1925', '1995', '1980', '113', '119', '110', '安心專線', '生命線', '張老師', '教師支持中心', '醫療', '急診']
PLACEHOLDER = '〔待確認'


def _texts(value: Any):
    if isinstance(value, str): yield value
    elif isinstance(value, dict):
        for v in value.values(): yield from _texts(v)
    elif isinstance(value, list):
        for v in value: yield from _texts(v)


NEGATIONS = ('不', '勿', '禁', '避免', '無', '非', '未', '嚴禁', '不得', '不可', '不要', '不能')


def _affirmed(text: str, word: str) -> bool:
    start = text.find(word)
    while start != -1:
        before = text[max(0, start - 4):start]
        if not any(before.endswith(n) or n in before[-3:] for n in NEGATIONS): return True
        start = text.find(word, start + 1)
    return False


def _hits(value: Any, words) -> list[str]:
    found = []
    for text in _texts(value):
        found += [w for w in words if w not in found and _affirmed(text, w)]
    return found


def _alias(value: str, field='student_alias') -> None:
    if not ALIAS.match(value):
        raise ValueError(f'{field} must be an anonymous code such as 學生A or S03, not a name: {value}')


def _unique(items, field, label):
    values = [x[field] for x in items]
    if len(values) != len(set(values)): raise ValueError(f'duplicate {label}')


def _no(value, words, label):
    found = _hits(value, words)
    if found: raise ValueError(f'{label}: {"、".join(found)}')


def check(skill: str, d: dict) -> list[str]:
    c = d['content']; adv: list[str] = []
    rule = RULES.get(skill)
    if rule: rule(c, adv)
    return adv


def _homeroom(c, adv):
    if c['period'] == '學期末交接' and 'handover' not in c: raise ValueError('學期末交接 requires handover')
    if 'roles' in c: _unique(c['roles'], 'role', 'role')
    _unique(c['routines'], 'name', 'routine name')
    if 'handover' in c: adv.append('交接資料僅含必要資訊；輔導與特教資料依原單位規定轉銜，不放入一般交接包')


def _behavior(c, adv):
    _alias(c['student_alias'])
    _unique(c['function_hypotheses'], 'id', 'hypothesis id')
    _no([c['prevention'], c['response_plan']], PUNITIVE, 'response must not use corporal, shaming or collective punishment')
    _no([c['behavior_definition'], c['function_hypotheses']], DIAGNOSIS, 'describe observable behaviour; do not diagnose')
    if c['safety_check']['red_flags_present'] and c['support_tier'] not in {'專業轉介', '行政協助'}:
        raise ValueError('red flags require support_tier 專業轉介 or 行政協助 and the incident-response route')
    if c['replacement_behavior']['behavior'].strip() == c['behavior_definition'].strip():
        raise ValueError('replacement behaviour must differ from the target behaviour')


FLAGS = {'bullying': '疑似霸凌', 'gender_equity': '疑似校園性別事件', 'child_protection': '兒少保護', 'self_harm_or_violence': '自傷或傷人', 'campus_safety': '校安事件'}


def _incident(c, adv):
    flags = [FLAGS[k] for k in FLAGS if c['red_flags'][k]]
    if flags:
        if not [r for r in c.get('reporting', []) if r['status'] != '不適用']:
            raise ValueError(f'red flags ({"、".join(flags)}) require at least one reporting route')
        if not c['not_alone']: raise ValueError('red flags require listing what the teacher must not decide alone')
        if c['case_status'] == '已結案': raise ValueError('a red-flag case cannot be closed by the teacher record')
        if c.get('restorative', {}).get('eligible'):
            raise ValueError('teacher-led mediation cannot replace the formal procedure when red flags are present')
        if any(r['status'] == '待通報' for r in c.get('reporting', [])):
            adv.append('仍有待通報項目：法定時限自知悉起算，請立即交學校權責人員')
    elif c.get('restorative', {}).get('eligible') and not c['restorative']['steps']:
        raise ValueError('eligible restorative process needs steps')
    _no(c['facts'], LABELS, 'facts must be neutral; remove labels')


def _guidance_advice(c, adv):
    _alias(c['student_alias'])
    _unique(c['hypotheses'], 'id', 'hypothesis id')
    _no([c['analysis']['ai_inferences'], [h['explanation'] for h in c['hypotheses']]], DIAGNOSIS, 'AI inference must not diagnose')
    _no([c['analysis'], c['patterns']], LABELS, 'remove labelling words')
    screen = c['red_flag_screen']
    if screen['triggered']:
        if not screen['flags']: raise ValueError('triggered red-flag screen must name the flags')
        if not c['referral']['recommended']: raise ValueError('triggered red flags require referral')
        if not any(a['horizon'] == '現在' for a in c['actions']): raise ValueError('triggered red flags require an action now')
    adv.append('本分析是教師專業判斷的輔助，不是診斷或輔導紀錄；正式輔導資料依學校規定保存')


def _collab(c, adv):
    _alias(c['student_alias'])
    _no(c['concern'], DIAGNOSIS, 'teacher concern should describe needs, not diagnose')
    if c['mode'] == 'IEP會議準備' and not (c.get('meeting_agenda') and c.get('class_adjustments')):
        raise ValueError('IEP會議準備 requires meeting_agenda and class_adjustments')
    if c['mode'] == '輔導轉介' and not [x for x in c['information_sharing'] if x['level'] != '不分享']:
        raise ValueError('referral must identify the minimum information to share')


DOWNWARD_ONLY = ['希照辦', '希查照', '請照辦', '希切實照辦', '請轉行照辦']


def _official(c, adv):
    body = [c['subject'], c['explanation'], c['proposal']]
    # 錯誤: rules stated in the 文書處理手冊; 警告 (advisory): textbook conventions the manual leaves open.
    if '\n' in c['subject'] or re.search(r'(^|[。；，])\s*[一二三四五六七八九十]、|（[一二三四五六七八九十]）|\([一二三四五六七八九十]\)', c['subject']):
        raise ValueError('主旨 must be one paragraph without item numbering (手冊第16點第3款)')
    direction, kind = c['direction'], c['doc_type']
    if direction in {'平行', '下行', '對人民'} and _hits(body, ['鈞']):
        raise ValueError('「鈞」只用於有隸屬關係之上級機關 (手冊第18點第3款)')
    if direction == '上行':
        wrong = _hits(body, DOWNWARD_ONLY)
        if wrong: adv.append('警告：上行文出現下行期望語（' + '、'.join(wrong) + '）')
        if c['proposal_label'] == '辦法': adv.append('警告：上行文第三段宜改用「建議」「請求」或「擬辦」（手冊第16點第3款第3目允許改用段名）')
        if '請查照' in c['subject']: adv.append('警告：有隸屬關係之上行文期望語宜用「請鑒核」「請核備」「請備查」等')
    if direction in {'平行', '對人民'}:
        wrong = _hits(body, ['希照辦', '希查照', '請鑒核'])
        if wrong: adv.append('警告：平行文或對人民不宜使用' + '、'.join(wrong))
    if direction == '下行':
        wrong = _hits(body, ['請鑒核', '請核備'])
        if wrong: adv.append('警告：下行文不宜使用上行期望語（' + '、'.join(wrong) + '）')
    if kind == '簽':
        if direction != '校內': raise ValueError('簽 is an internal document; set direction 校內')
        if c['proposal_label'] != '擬辦' or not c['proposal']: raise ValueError('簽 requires 擬辦 with concrete proposals')
    elif kind == '公告':
        if not c.get('basis') or c['proposal_label'] != '公告事項': raise ValueError('公告 uses 主旨／依據／公告事項')
    elif kind == '開會通知單':
        if 'meeting' not in c: raise ValueError('開會通知單 requires meeting details')
    else:
        if not c.get('recipient') and kind in {'函', '書函'}: raise ValueError(f'{kind} requires recipient (受文者)')
    if c['handling'] == '簽稿併陳' and kind != '簽': adv.append('簽稿併陳需同時備妥簽與稿，請另產生對應的簽')
    if re.search(r'請 (鑒|核|查|備)', ' '.join(_texts(body))): raise ValueError('挪抬已廢止：期望語不空格')
    outdated = _hits(body, OUTDATED_TERMS)
    if outdated: adv.append('過時用語建議修改：' + '、'.join(outdated))
    for field in ('date', 'doc_number'):
        if field in c and PLACEHOLDER in c[field]: adv.append(f'{field} 尚待確認，正式發文前由承辦人補上')
    if c['mode'] == '修改' and not c.get('review_findings'): raise ValueError('修改 mode requires review_findings')
    adv.append('本文件為草稿；簽核、用印與發文由學校依權責辦理，生成不代表已核定或已發文')


def _brainstorm(c, adv):
    for code in c['learning_focus']:
        if not code['verified'] and not code.get('verification_note'):
            raise ValueError('unverified curriculum code requires verification_note')
    if c['selected']['angle'] not in ' '.join(_texts(c['divergence'])):
        adv.append('選定切入點未出現在發散清單中，請確認是否為新提出的角度')


def _curriculum_plan(c, adv):
    _unique(c['goals'], 'id', 'goal id')
    ids = {g['id'] for g in c['goals']}; used = set()
    for row in c['structure']:
        if not set(row['goal_ids']) <= ids: raise ValueError(f"unknown goal id in {row['course']}")
        used |= set(row['goal_ids'])
    if used != ids: raise ValueError(f'every goal needs a course; unused: {sorted(ids - used)}')
    courses = {r['course'] for r in c['structure']}
    for unit in c['units']:
        if unit['course'] not in courses: raise ValueError(f"unit course not in structure: {unit['course']}")
    for req in c.get('required_periods', []):
        total = sum(r['periods_per_week'] for r in c['structure'] if r['grade'] == req['grade'])
        if abs(total - req['periods_per_week']) > 1e-9:
            raise ValueError(f"{req['grade']} weekly periods {total} differ from required {req['periods_per_week']}")
    adv.append('節數與格式依當年度主管機關規定與縣市備查格式確認')


def _open_lesson(c, adv):
    stage = c['stage']
    if stage in {'共同備課', '三階段完整'} and 'prep' not in c: raise ValueError(f'{stage} requires prep')
    if stage in {'觀課', '三階段完整'} and not c.get('observations'): raise ValueError(f'{stage} requires observations')
    if stage in {'議課', '三階段完整'} and 'debrief' not in c: raise ValueError(f'{stage} requires debrief')
    _no([[o['behavior'] for o in c.get('observations', [])], c.get('debrief', {}).get('facts', [])], EVALUATIVE, 'observation records must be low-inference; move judgements to interpretations')


def _conduct(c, adv):
    for s in c['students']:
        _alias(s['student_id'], 'student_id')
        _unique(s['evidence'], 'id', f"evidence id for {s['student_id']}")
        ids = {e['id'] for e in s['evidence']}
        if not set(s['evidence_ids']) <= ids: raise ValueError(f"{s['student_id']} comment cites unknown evidence")
        _no([s['comment'], s['suggestion'], s.get('parent_version', '')], LABELS, f"{s['student_id']} comment contains labelling words")
        _no([s['comment'], s.get('parent_version', '')], GRADE_WORDS, f"{s['student_id']} 日常生活表現不作綜合評價或等第")


def _affairs(c, adv):
    _unique(c['allegations'], 'id', 'allegation id')
    ids = {a['id'] for a in c['allegations']}
    if 'statement_draft' in c:
        covered = [x['allegation_id'] for x in c['statement_draft']['by_allegation']]
        if not set(covered) <= ids: raise ValueError('statement refers to unknown allegation')
        if set(covered) != ids: raise ValueError(f'statement must respond to every allegation; missing: {sorted(ids - set(covered))}')
    if len([p for p in c.get('support_people', []) if p['role'] == '輔佐人']) > 2: raise ValueError('輔佐人 cannot exceed 2 persons')
    if c['stage'] == '調查訪談' and not c.get('interview_prep'): raise ValueError('調查訪談 stage requires interview_prep')
    tone = _hits(c.get('statement_draft', {}), ACCUSATORY)
    if tone: adv.append('陳述稿含指控性用語（' + '、'.join(tone) + '），建議改為事實與證據陳述')
    adv.append('本文件是準備草稿，不是法律意見；正式陳述前建議諮詢教師會或律師')


def _wellbeing(c, adv):
    risk = c['risk_screen']
    if risk['self_harm_thoughts'] or risk['unable_to_function']:
        if not _hits(c['resources'], CRISIS): raise ValueError('risk signals require an immediate crisis or professional resource')
        if not any(p['horizon'] == '現在' for p in c['plan']): raise ValueError('risk signals require an action now')
    adv.append('本支持計畫不取代專業諮商或醫療；使用教師支持中心等服務依法不得因此受差別待遇')


def _culture(c, adv):
    _no([c['response_plan'], c['repair_paths'], c['norms']], PUNITIVE, 'class responses must not use corporal, shaming or collective punishment')


def _parent(c, adv):
    if c['audience'] == '全班家長' and c['sensitivity'] != '一般': raise ValueError('individual or sensitive matters cannot be sent to all parents')
    if c['channel'] == '公告' and c['sensitivity'] != '一般': raise ValueError('公告 is only for general class information')
    if c['sensitivity'] == '正式程序' and c['channel'] not in {'行政協調', '書面通知', '面談'}: raise ValueError('正式程序 matters go through administration, written notice or meeting')
    if c['send_status'] == '已發送': adv.append('send_status 為已發送：請確認實際發送紀錄，本工具不會發送訊息')


def _school_doc(c, adv):
    if 'budget' in c or 'total_budget' in c:
        if 'budget' not in c or 'total_budget' not in c: raise ValueError('budget items and total_budget must be provided together')
        if abs(sum(x['amount'] for x in c['budget']) - c['total_budget']) > 1e-6: raise ValueError('budget items do not sum to total_budget')
    if c['document_type'] == '成果報告' and not c.get('results'): raise ValueError('成果報告 requires results with evidence')
    if c['document_type'] == '補助申請計畫' and 'budget' not in c: raise ValueError('補助申請計畫 requires a budget')
    if c['approval_status'] != '已核定': adv.append('文件為草稿或簽核中，不得以已核定名義對外使用')


def _meeting(c, adv):
    if sum(x['minutes'] for x in c['agenda']) != c['duration_minutes']: raise ValueError('agenda minutes must equal duration_minutes')
    for item in c.get('discussions', []):
        pending = item['status'] == '待決議'
        if pending != item['resolution'].startswith('〔待會議決議'):
            raise ValueError(f"discussion {item['case_no']}: 待決議 must use resolution 〔待會議決議〕 and decided items need real resolutions")
    if c['record_status'] == '議程草案' and any(x['status'] != '待決議' for x in c.get('discussions', [])):
        raise ValueError('議程草案 cannot contain decided resolutions')


def _lesson(c, adv):
    if 'learning_focus' in c and not c.get('curriculum_codes'):
        adv.append('已列學習重點但未附課綱代碼查核，請以 lookup_curriculum.py 回查')


RULES = {
    'tw-edu-homeroom-operations': _homeroom, 'tw-edu-behavior-support': _behavior, 'tw-edu-incident-response': _incident,
    'tw-edu-student-guidance-advice': _guidance_advice, 'tw-edu-guidance-collaboration': _collab, 'tw-edu-official-document': _official,
    'tw-edu-lesson-design-brainstorm': _brainstorm, 'tw-edu-school-curriculum-plan': _curriculum_plan, 'tw-edu-open-lesson': _open_lesson,
    'tw-edu-conduct-comments': _conduct, 'tw-edu-school-affairs-meeting': _affairs, 'tw-edu-teacher-wellbeing': _wellbeing,
    'tw-edu-classroom-culture': _culture, 'tw-edu-parent-communication': _parent, 'tw-edu-school-document': _school_doc,
    'tw-edu-meeting-facilitator': _meeting, 'tw-edu-lesson-plan-108': _lesson,
}
