#!/usr/bin/env python3
"""教師會議文件生成腳本"""
import argparse, sys
sys.path.insert(0, '.')
from tw_edu_doc_utils import *

def add_agenda(doc, meeting_type, topic, duration):
    type_labels = {'plc':'教師專業學習社群(PLC)','curriculum':'課程發展委員會',
                   'admin':'行政會議','lesson_study':'共同備課'}
    section_heading(doc, f'{type_labels.get(meeting_type,"教師")}會議議程')
    tbl = doc.add_table(rows=3, cols=4)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(3), Cm(5.5), Cm(3), Cm(5.5)]): tbl.columns[j].width = w
    info = [('會議主題', topic), ('會議類型', type_labels.get(meeting_type,'')),
            ('時間/地點', f'共 {duration} 分鐘'), ('主持人/記錄', '')]
    for i in range(2):
        for j in range(2):
            idx = i*2+j
            header_cell(tbl.rows[i].cells[j*2], info[idx][0])
            data_cell(tbl.rows[i].cells[j*2+1], info[idx][1], row_idx=i)
    merged = tbl.rows[2].cells[0].merge(tbl.rows[2].cells[3])
    header_cell(merged, '出席人員：（請填入）')
    doc.add_paragraph()

    section_heading(doc, '議程安排', level=2)
    items_map = {
        'plc': [('5分', '簡報/開場', '說明今日會議目標'),
                ('15分', '共同閱讀/案例分析', '聚焦討論文本或案例'),
                ('20分', '深度討論', '引導問題：（見附件）'),
                ('15分', '行動規劃', '訂定下次嘗試的教學策略'),
                ('5分', '綜合反思', '每人分享一句話')],
        'lesson_study': [('10分', '單元分析', '確認學習目標與挑戰'),
                         ('20分', '教案設計討論', '逐段討論教學步驟'),
                         ('10分', '觀課焦點設定', '確認觀課重點'),
                         ('10分', '教材準備確認', '確認學習單/教具')],
        'curriculum': [('5分', '確認議程', ''),
                       ('20分', '課程審查', '各年段課程計畫報告'),
                       ('15分', '討論與決議', ''),
                       ('10分', '行政宣達', ''),
                       ('10分', '決議確認', '')],
    }
    items = items_map.get(meeting_type, items_map['plc'])
    tbl2 = doc.add_table(rows=len(items)+1, cols=4)
    tbl2.style = 'Table Grid'
    for j, w in enumerate([Cm(2.5), Cm(4), Cm(7), Cm(3.5)]): tbl2.columns[j].width = w
    for j, h in enumerate(['時間', '議題', '說明/預期產出', '負責人']):
        header_cell(tbl2.rows[0].cells[j], h)
    for i, (t, item, desc) in enumerate(items, 1):
        for j, text in enumerate([t, item, desc, '']):
            data_cell(tbl2.rows[i].cells[j], text, row_idx=i, center=(j==0))
        tbl2.rows[i].height = Cm(1.2)
    doc.add_paragraph()

    section_heading(doc, '引導討論問題', level=2)
    questions_map = {
        'plc': [f'在「{topic}」這個主題上，你目前最大的挑戰是什麼？',
                '你曾試過哪些方法？效果如何？',
                '有什麼具體的教學策略是你想在下週嘗試的？',
                '你需要什麼樣的支持才能做到？'],
        'lesson_study': [f'學生在「{topic}」這個單元最常出現哪些困難？',
                         '這節課最重要的「學習轉折點」是什麼？',
                         '我們要如何知道學生是否真的學會了？'],
    }
    qs = questions_map.get(meeting_type, questions_map['plc'])
    for i, q in enumerate(qs, 1):
        p = doc.add_paragraph()
        r = p.add_run(f'{i}. {q}')
        r.font.size = Pt(11); r.font.name = '標楷體'; r.font.color.rgb = DARK_TEXT
        set_east_asia_font(r); p.paragraph_format.space_after = Pt(4)
    doc.add_paragraph()

def add_minutes(doc, topic):
    section_heading(doc, '會議記錄')
    tbl = doc.add_table(rows=6, cols=2)
    tbl.style = 'Table Grid'
    tbl.columns[0].width = Cm(4); tbl.columns[1].width = Cm(13)
    rows = [('討論重點一', ''), ('討論重點二', ''), ('討論重點三', ''),
            ('決議事項', ''), ('行動清單\n（負責人/期限）', '')]
    header_cell(tbl.rows[0].cells[0], '討論項目')
    header_cell(tbl.rows[0].cells[1], '內容摘要')
    for i, (label, _) in enumerate(rows, 1):
        header_cell(tbl.rows[i].cells[0], label, bg=BLUE_MID)
        data_cell(tbl.rows[i].cells[1], '', row_idx=i)
        tbl.rows[i].height = Cm(2.5)
    doc.add_paragraph()
    section_heading(doc, '下次會議', level=2)
    p = doc.add_paragraph()
    r = p.add_run('日期：＿＿＿＿　地點：＿＿＿＿　主題：＿＿＿＿＿＿＿＿＿＿')
    r.font.size = Pt(12); r.font.name = '標楷體'; r.font.color.rgb = DARK_TEXT
    set_east_asia_font(r)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type',     default='plc',
                        choices=['plc','curriculum','admin','lesson_study'])
    parser.add_argument('--topic',    default='素養導向評量設計')
    parser.add_argument('--duration', default='60')
    parser.add_argument('--mode',     default='both',
                        choices=['agenda','minutes','both'])
    parser.add_argument('--output',   default='會議文件.docx')
    args = parser.parse_args()

    doc = new_doc_a4()
    add_header_footer(doc, f'教師會議文件｜{args.topic}')
    cover_page(doc, '教師會議文件', args.topic,
               {'會議主題': args.topic, '時長': f'{args.duration} 分鐘',
                '日期': str(date.today())})
    if args.mode in ('agenda','both'): add_agenda(doc, args.type, args.topic, args.duration)
    if args.mode in ('minutes','both'): add_minutes(doc, args.topic)
    doc.save(args.output); print(f'✓ 會議文件已儲存：{args.output}')

if __name__ == '__main__': main()
