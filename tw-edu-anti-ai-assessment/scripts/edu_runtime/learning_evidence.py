"""Observed classroom responses only; no fixed ability or causal labels."""
from collections import Counter

def analyze(c):
    items=c['items'];responses=c['responses'];ids=[x['id'] for x in items];students=[x['student_id'] for x in responses]
    if not items or not responses or len(ids)!=len(set(ids)) or len(students)!=len(set(students)):raise ValueError('nonempty, unique item/student IDs required')
    if any(set(r['answers'])-set(ids) for r in responses):raise ValueError('unknown response item')
    n=len(responses);reports=[];targets={};student_observations={s:[] for s in students}
    for item in items:
        key=item['answer'];status=item['key_status'];options=item.get('options',[])
        if len(options)!=len(set(options)):raise ValueError('duplicate options')
        if status=='verified' and (not isinstance(key,str) or not key.strip() or (options and key not in options)):raise ValueError('verified answer must be an allowed option')
        answers=[r['answers'].get(item['id']) for r in responses]
        if any(a is not None and (not isinstance(a,str) or not a.strip() or (options and a not in options)) for a in answers):raise ValueError('invalid response option')
        missing=sum(a is None for a in answers);counts=Counter(a for a in answers if a is not None);answered=n-missing
        correct=sum(a==key for a in answers) if status=='verified' else None
        report={'item_id':item['id'],'target':item['target'],'key_status':status,'class_n':n,'answered_n':answered,'missing_n':missing,'option_counts':dict(counts),'correct_n':correct,'accuracy_all_students':correct/n if correct is not None else None,'accuracy_answered':correct/answered if correct is not None and answered else None,'discrimination':'not_computed: sample/design not established','possible_causes':['需要學生解釋或作品才能區分概念、讀題與策略；選項分布不自動證明迷思。']}
        reports.append(report)
        t=targets.setdefault(item['target'],{'verified_item_ids':[],'pending_item_ids':[],'correct_responses':0,'possible_responses':0,'missing_responses':0})
        if status=='verified':t['verified_item_ids'].append(item['id']);t['correct_responses']+=correct;t['possible_responses']+=n;t['missing_responses']+=missing
        else:t['pending_item_ids'].append(item['id'])
        for r,a in zip(responses,answers):
            student_observations[r['student_id']].append({'item_id':item['id'],'observed_answer':a,'status':'missing' if a is None else 'ungraded' if status!='verified' else 'correct' if a==key else 'needs_followup'})
    for t in targets.values():t['accuracy_all_responses']=t['correct_responses']/t['possible_responses'] if t['possible_responses'] else None
    return {'class_n':n,'items':reports,'targets':targets,'student_observations':student_observations,'limitations':['題目品質與作答情境影響判讀；未作能力診斷或因果分析。','未回答記缺答；全班與已答分母分開；答案未核實不計正確率。']}
