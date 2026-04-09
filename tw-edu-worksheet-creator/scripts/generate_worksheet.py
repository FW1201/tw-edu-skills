#!/usr/bin/env python3
"""素養導向學習單生成腳本"""
import argparse, sys
sys.path.insert(0, '.')
from tw_edu_doc_utils import *

def add_worksheet_header(doc, subject, grade, topic, purpose_label):
    tbl = doc.add_table(rows=2, cols=4)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(2.5), Cm(5), Cm(2.5), Cm(7)]):
        tbl.columns[j].width = w
    pairs = [('科目', subject), ('年級/班級', f'{grade}　　年　　班'),
             ('姓名', '　　　　　　'), ('學習主題', topic)]
    for j, (k, v) in enumerate(pairs):
        header_cell(tbl.rows[0].cells[j] if j < 4 else tbl.rows[1].cells[j-4], k)
        data_cell(tbl.rows[0].cells[j] if j < 4 else tbl.rows[1].cells[j-4], v, row_idx=j)
    r2 = tbl.rows[1]
    header_cell(r2.cells[0], '目的')
    data_cell(r2.cells[1], purpose_label, row_idx=1)
    header_cell(r2.cells[2], '日期')
    data_cell(r2.cells[3], '　　年　　月　　日', row_idx=1)
    doc.add_paragraph()

def add_prereading(doc, topic):
    section_heading(doc, '◎ 課前準備：啟動先備知識', level=2)
    tbl = doc.add_table(rows=3, cols=2)
    tbl.style = 'Table Grid'
    tbl.columns[0].width = Cm(8); tbl.columns[1].width = Cm(9)
    header_cell(tbl.rows[0].cells[0], f'我對「{topic}」的聯想')
    header_cell(tbl.rows[0].cells[1], '我的預測：閱讀後我可能會學到…')
    for j in range(2):
        data_cell(tbl.rows[1].cells[j], '', row_idx=1)
        tbl.rows[1].height = Cm(2.5)
    merged = tbl.rows[2].cells[0].merge(tbl.rows[2].cells[1])
    data_cell(merged, f'看到標題《{topic}》，我的第一個問題是：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿', row_idx=2)
    tbl.rows[2].height = Cm(1.2)
    doc.add_paragraph()

def add_three_level_questions(doc, topic):
    section_heading(doc, '◎ 三層次提問：深度閱讀理解', level=2)
    levels = [
        ('字面層次（文中找得到答案）', BLUE_MID,
         f'1. 文章中，作者描述了哪些關於「{topic}」的具體細節？\n   答：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿\n'
         f'2. 文章的結構是如何安排的？請依序列出各段的主要內容。\n   答：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿'),
        ('推論層次（文章沒有直說，需要推理）', GOLD,
         f'3. 作者透過「{topic}」想表達什麼深層情感或意義？\n   答：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿\n'
         '4. 文章使用了哪些寫作技巧？這些技巧有什麼效果？\n   答：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿'),
        ('評鑑層次（跳脫文章，連結自身）', GREEN,
         f'5. 你同意作者對「{topic}」的詮釋嗎？請說明理由。\n   答：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿\n'
         f'6. 學習《{topic}》後，你對哪件事有了新的理解或想法？\n   答：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿'),
    ]
    for level, color, qs in levels:
        tbl = doc.add_table(rows=2, cols=1)
        tbl.style = 'Table Grid'
        tbl.columns[0].width = Cm(17)
        header_cell(tbl.rows[0].cells[0], f'▶ {level}', bg=color)
        tbl.rows[0].height = Cm(0.8)
        data_cell(tbl.rows[1].cells[0], qs, row_idx=1)
        tbl.rows[1].height = Cm(3.5)
        doc.add_paragraph()

def add_concept_map(doc, topic):
    section_heading(doc, '◎ 概念整理：心智圖/概念圖', level=2)
    tbl = doc.add_table(rows=5, cols=5)
    tbl.style = 'Table Grid'
    for j in range(5): tbl.columns[j].width = Cm(3.4)

    # 中心格
    center = tbl.rows[2].cells[2]
    header_cell(center, f'核心概念\n《{topic}》', bg=BLUE_DEEP)
    # 四個擴展格
    positions = [(0,2),(2,0),(2,4),(4,2)]
    labels = ['主題一', '主題二', '主題三', '主題四']
    for (r,c), label in zip(positions, labels):
        header_cell(tbl.rows[r].cells[c], label, bg=BLUE_MID)
    # 詳細格
    detail_pos = [(1,1),(1,3),(3,1),(3,3)]
    for r,c in detail_pos:
        data_cell(tbl.rows[r].cells[c], '詳細說明\n＿＿＿＿＿', row_idx=r)
    # 其餘空格
    for r in range(5):
        for c in range(5):
            cell = tbl.rows[r].cells[c]
            if not cell.paragraphs[0].runs:
                set_cell_bg(cell, RGBColor(0xF5,0xF5,0xF5))
                set_cell_border(cell, color='CCCCCC')
    for r in range(5): tbl.rows[r].height = Cm(1.5)
    doc.add_paragraph()

def add_writing_scaffold(doc, topic):
    section_heading(doc, '◎ 仿作/創作鷹架', level=2)
    p = doc.add_paragraph()
    r = p.add_run(f'【任務】模仿課文的寫作技巧，以「{topic}」為發想，寫一段 80-120 字的短文。')
    r.font.size = Pt(11); r.bold = True; r.font.name = '標楷體'; r.font.color.rgb = BLUE_DEEP
    set_east_asia_font(r)
    tips = ['（提示 1）先想好你要描寫的主角和場景是什麼',
            '（提示 2）選 3 個精準動詞描寫動作，讓動作說話',
            '（提示 3）加入一個細節感受（視覺/聽覺/嗅覺/觸覺）']
    for tip in tips:
        p2 = doc.add_paragraph()
        r2 = p2.add_run(tip)
        r2.font.size = Pt(10); r2.font.name = '標楷體'
        r2.font.color.rgb = RGBColor(0x56,0x65,0x73)
        set_east_asia_font(r2)
        p2.paragraph_format.left_indent = Cm(0.5)
    doc.add_paragraph()
    for _ in range(8):
        p3 = doc.add_paragraph()
        r3 = p3.add_run('　')
        pPr = p3._p.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        bot = OxmlElement('w:bottom')
        bot.set(qn('w:val'), 'single'); bot.set(qn('w:sz'), '4')
        bot.set(qn('w:color'), 'AAAAAA')
        pBdr.append(bot); pPr.append(pBdr)
        p3.paragraph_format.space_after = Pt(4)
    doc.add_paragraph()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject',    default='國語文')
    parser.add_argument('--grade',      default='國中八年級')
    parser.add_argument('--topic',      default='背影')
    parser.add_argument('--purpose',    default='inclass',
                        choices=['preview','inclass','review','homework'])
    parser.add_argument('--activities', default='prereading,questions,concept,writing')
    parser.add_argument('--output',     default='學習單.docx')
    args = parser.parse_args()

    purpose_map = {'preview':'課前預習','inclass':'課堂學習',
                   'review':'課後複習','homework':'回家作業'}
    acts = [a.strip() for a in args.activities.split(',')]

    doc = new_doc_a4()
    add_header_footer(doc, f'學習單｜{args.subject}｜{args.topic}')

    # 大標題
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f'《{args.topic}》素養導向學習單')
    r.bold = True; r.font.size = Pt(18); r.font.name = '標楷體'
    r.font.color.rgb = BLUE_DEEP; set_east_asia_font(r)
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(6)

    add_worksheet_header(doc, args.subject, args.grade, args.topic,
                         purpose_map.get(args.purpose,'課堂學習'))
    if 'prereading' in acts: add_prereading(doc, args.topic)
    if 'questions'  in acts: add_three_level_questions(doc, args.topic)
    if 'concept'    in acts: add_concept_map(doc, args.topic)
    if 'writing'    in acts: add_writing_scaffold(doc, args.topic)

    doc.save(args.output)
    print(f'✓ 學習單已儲存：{args.output}')

if __name__ == '__main__':
    main()
