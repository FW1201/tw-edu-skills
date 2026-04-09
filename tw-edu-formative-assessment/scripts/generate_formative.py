#!/usr/bin/env python3
"""形成性評量工具生成腳本"""
import argparse, sys
sys.path.insert(0, '.')
from tw_edu_doc_utils import *

def add_exit_ticket(doc, subject, grade, topic, copies=4):
    section_heading(doc, f'出口票（Exit Ticket）— {topic}')
    p = doc.add_paragraph()
    r = p.add_run('★ 一頁排版 4 份，請沿虛線裁切後發給學生')
    r.font.size = Pt(10); r.font.color.rgb = GOLD; r.font.name = '標楷體'
    set_east_asia_font(r)
    doc.add_paragraph()

    for _ in range(copies):
        tbl = doc.add_table(rows=5, cols=2)
        tbl.style = 'Table Grid'
        tbl.columns[0].width = Cm(9); tbl.columns[1].width = Cm(8)
        # 標題列
        merged = tbl.rows[0].cells[0].merge(tbl.rows[0].cells[1])
        header_cell(merged, f'出口票｜{subject}｜{grade}｜{topic}', bg=BLUE_DEEP)
        tbl.rows[0].height = Cm(0.8)
        # 基本資料
        merged2 = tbl.rows[1].cells[0].merge(tbl.rows[1].cells[1])
        data_cell(merged2, '班級：＿＿  座號：＿＿  姓名：＿＿＿＿＿＿  日期：＿＿/＿＿', row_idx=1)
        tbl.rows[1].height = Cm(0.8)
        # 問題區
        items = [
            ('今天學到最重要的一件事是：', '還有一個問題想問老師：'),
            ('我對這個主題的理解程度（請圈選）：\n★☆☆ 還不懂　★★☆ 有點懂　★★★ 完全懂',
             '下節課我想繼續了解：'),
        ]
        for i, (q1, q2) in enumerate(items[:2]):
            data_cell(tbl.rows[i+2].cells[0], q1, row_idx=i+2)
            data_cell(tbl.rows[i+2].cells[1], q2, row_idx=i+2)
            tbl.rows[i+2].height = Cm(1.8)
        # 分隔線
        merged3 = tbl.rows[4].cells[0].merge(tbl.rows[4].cells[1])
        set_cell_bg(merged3, BLUE_LIGHT)
        cell_write(merged3, '- - - - - - - - - - - - - 請沿虛線裁切 - - - - - - - - - - - - -',
                   size=9, color=RGBColor(0x99,0x99,0x99), center=True)
        tbl.rows[4].height = Cm(0.4)
    doc.add_paragraph()

def add_kwl_table(doc, subject, grade, topic):
    section_heading(doc, f'KWL 學習記錄表 — {topic}')
    tbl = doc.add_table(rows=8, cols=3)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(5.5), Cm(6), Cm(5.5)]):
        tbl.columns[j].width = w

    header_cell(tbl.rows[0].cells[0], 'K — 我已經知道', bg=GREEN)
    header_cell(tbl.rows[0].cells[1], 'W — 我想要知道', bg=GOLD)
    header_cell(tbl.rows[0].cells[2], 'L — 我學到了', bg=BLUE_MID)

    sub_hdrs = ['（課前填寫）', '（課前填寫）', '（課後填寫）']
    for j, sh in enumerate(sub_hdrs):
        data_cell(tbl.rows[1].cells[j], sh, row_idx=1, center=True)
        tbl.rows[1].height = Cm(0.7)

    for i in range(2, 8):
        for j in range(3):
            data_cell(tbl.rows[i].cells[j], '', row_idx=i)
            tbl.rows[i].height = Cm(1.2)

    # 班級姓名
    p = doc.add_paragraph()
    r = p.add_run(f'班級：＿＿  座號：＿＿  姓名：＿＿＿＿　科目：{subject}　主題：{topic}')
    r.font.size = Pt(10); r.font.name = '標楷體'; r.font.color.rgb = DARK_TEXT
    set_east_asia_font(r)
    doc.add_paragraph()

def add_self_check(doc, subject, grade, topic):
    section_heading(doc, f'學習理解自我檢核表 — {topic}')
    items = [
        f'我能說出《{topic}》的主要內容',
        '我能解釋關鍵概念的意義',
        '我能舉出具體例子說明所學內容',
        '我能將所學與生活經驗連結',
        '我仍有疑問，需要請教老師或同學',
    ]
    tbl = doc.add_table(rows=len(items)+1, cols=5)
    tbl.style = 'Table Grid'
    col_w = [Cm(8), Cm(2.2), Cm(2.2), Cm(2.2), Cm(2.4)]
    for j, w in enumerate(col_w): tbl.columns[j].width = w
    hdrs = ['學習指標', '完全做到 ✓✓', '大致做到 ✓', '還在努力 △', '不確定 ?']
    for j, h in enumerate(hdrs): header_cell(tbl.rows[0].cells[j], h)
    for i, item in enumerate(items, 1):
        data_cell(tbl.rows[i].cells[0], f'{i}. {item}', row_idx=i)
        for j in range(1, 5):
            data_cell(tbl.rows[i].cells[j], '', row_idx=i, center=True)
        tbl.rows[i].height = Cm(1.0)
    # 反思區
    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run('✏ 本次學習最大的收穫：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿')
    r.font.size = Pt(11); r.font.name = '標楷體'; r.font.color.rgb = DARK_TEXT
    set_east_asia_font(r)
    p2 = doc.add_paragraph()
    r2 = p2.add_run('✏ 我還想了解的問題：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿')
    r2.font.size = Pt(11); r2.font.name = '標楷體'; r2.font.color.rgb = DARK_TEXT
    set_east_asia_font(r2)
    doc.add_paragraph()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', default='國語文')
    parser.add_argument('--grade',   default='國中八年級')
    parser.add_argument('--topic',   default='背影')
    parser.add_argument('--type',    default='exit_ticket',
                        choices=['exit_ticket','kwl','self_check','all'])
    parser.add_argument('--output',  default='形成性評量.docx')
    args = parser.parse_args()

    doc = new_doc_a4()
    add_header_footer(doc, f'形成性評量｜{args.subject}｜{args.topic}')
    cover_page(doc, '形成性評量工具包',
               f'{args.topic}｜{args.subject}｜{args.grade}',
               {'科目': args.subject, '年級': args.grade,
                '主題': args.topic, '日期': str(date.today())})

    if args.type in ('exit_ticket', 'all'):
        add_exit_ticket(doc, args.subject, args.grade, args.topic)
    if args.type in ('kwl', 'all'):
        add_kwl_table(doc, args.subject, args.grade, args.topic)
    if args.type in ('self_check', 'all'):
        add_self_check(doc, args.subject, args.grade, args.topic)

    doc.save(args.output)
    print(f'✓ 形成性評量工具已儲存：{args.output}')

if __name__ == '__main__':
    main()
