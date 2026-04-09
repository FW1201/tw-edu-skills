#!/usr/bin/env python3
"""試卷與答案卷生成腳本"""
import argparse, sys
sys.path.insert(0, '.')
from tw_edu_doc_utils import *

def add_exam_header(doc, subject, grade, exam_range, total):
    section_heading(doc, '作答注意事項', level=2)
    notes = [
        '1. 請在答案卷或答案格內作答，在試卷上作答不予計分。',
        '2. 請保持答案卷整潔，不得折疊或塗污。',
        f'3. 本試卷共 {total} 分，請注意時間分配。',
        '4. 選擇題每題只能選一個答案，多選或未選均不給分。',
    ]
    for note in notes:
        p = doc.add_paragraph()
        r = p.add_run(note)
        r.font.size = Pt(11); r.font.name = '標楷體'
        r.font.color.rgb = DARK_TEXT
        set_east_asia_font(r)
    doc.add_paragraph()

def add_choice_section(doc, subject, grade, exam_range, count=20, pts=2):
    section_heading(doc, f'壹、選擇題（每題 {pts} 分，共 {count*pts} 分）')
    p = doc.add_paragraph()
    r = p.add_run('（請選出最適當的答案，每題只能選一個）')
    r.font.size = Pt(11); r.font.name = '標楷體'; r.font.color.rgb = BLUE_MID
    set_east_asia_font(r)
    doc.add_paragraph()

    sample_questions = [
        (f'下列關於「{exam_range}」的說明，何者正確？',
         ['(A) 選項甲', '(B) 選項乙', '(C) 選項丙', '(D) 選項丁'], 'A'),
        ('下列詞語中，何者詞性與其他三者不同？',
         ['(A) 蹣跚', '(B) 頹唐', '(C) 禍不單行', '(D) 狼狽'], 'C'),
        ('「禍不單行」的字面意義最接近下列何者？',
         ['(A) 禍從天降', '(B) 壞事接連發生', '(C) 一人犯罪累及他人', '(D) 行事謹慎以免惹禍'], 'B'),
    ]
    for i in range(min(count, len(sample_questions))):
        q = sample_questions[i % len(sample_questions)]
        num_p = doc.add_paragraph()
        num_r = num_p.add_run(f'{i+1}. {q[0]}')
        num_r.font.size = Pt(11); num_r.font.name = '標楷體'
        num_r.font.color.rgb = DARK_TEXT
        set_east_asia_font(num_r)
        num_p.paragraph_format.space_before = Pt(4)

        opt_p = doc.add_paragraph()
        opt_r = opt_p.add_run('　　'.join(q[1]))
        opt_r.font.size = Pt(11); opt_r.font.name = '標楷體'
        opt_r.font.color.rgb = RGBColor(0x34, 0x49, 0x5E)
        set_east_asia_font(opt_r)
        opt_p.paragraph_format.left_indent = Cm(0.5)
        opt_p.paragraph_format.space_after = Pt(6)

    doc.add_paragraph()

def add_fill_section(doc, exam_range, count=10, pts=2):
    section_heading(doc, f'貳、填充題（每格 {pts} 分，共 {count*pts} 分）')
    p = doc.add_paragraph()
    r = p.add_run('（請將正確答案填入格線上）')
    r.font.size = Pt(11); r.font.name = '標楷體'; r.font.color.rgb = BLUE_MID
    set_east_asia_font(r)
    doc.add_paragraph()

    for i in range(1, count+1):
        p = doc.add_paragraph()
        r = p.add_run(f'{i}. 請填入與「{exam_range}」相關的正確詞語：＿＿＿＿＿＿＿＿')
        r.font.size = Pt(11); r.font.name = '標楷體'
        r.font.color.rgb = DARK_TEXT
        set_east_asia_font(r)
        p.paragraph_format.space_after = Pt(8)
    doc.add_paragraph()

def add_short_answer_section(doc, exam_range, count=4, pts=10):
    section_heading(doc, f'參、問答題（每題 {pts} 分，共 {count*pts} 分）')
    doc.add_paragraph()
    questions = [
        f'請說明《{exam_range}》的主要主題，並舉出文中具體的例子加以說明。（至少 100 字）',
        f'請分析《{exam_range}》的篇章結構，說明各段落的功能與彼此的關聯。',
        '請比較本課文與延伸閱讀文章，說明兩者在表達方式上的異同。',
        '假設你是文中的主角，你會如何面對文章中的情境？請結合個人經驗說明。（至少 80 字）',
    ]
    for i, q in enumerate(questions[:count], 1):
        p = doc.add_paragraph()
        r = p.add_run(f'{i}. {q}')
        r.font.size = Pt(11); r.font.name = '標楷體'
        r.font.color.rgb = DARK_TEXT
        set_east_asia_font(r)
        p.paragraph_format.space_before = Pt(4)
        # 作答空格
        for _ in range(6):
            line_p = doc.add_paragraph()
            line_r = line_p.add_run('　' * 30)
            line_r.font.size = Pt(12)
            pPr = line_p._p.get_or_add_pPr()
            pBdr = OxmlElement('w:pBdr')
            bot = OxmlElement('w:bottom')
            bot.set(qn('w:val'), 'single')
            bot.set(qn('w:sz'), '4')
            bot.set(qn('w:color'), 'AAAAAA')
            pBdr.append(bot)
            pPr.append(pBdr)
        doc.add_paragraph()

def add_answer_key(doc, subject, grade, exam_range):
    doc.add_page_break()
    section_heading(doc, f'【答案卷】{subject}｜{grade}')
    p = doc.add_paragraph()
    r = p.add_run(f'考試範圍：{exam_range}')
    r.font.size = Pt(11); r.font.name = '標楷體'; r.font.color.rgb = DARK_TEXT
    set_east_asia_font(r)
    doc.add_paragraph()

    section_heading(doc, '壹、選擇題答案', level=2)
    tbl = doc.add_table(rows=5, cols=5)
    tbl.style = 'Table Grid'
    for j in range(5):
        tbl.columns[j].width = Cm(3.4)

    sample_ans = ['A','C','B','D','A','B','C','A','D','B',
                  'C','A','B','D','C','A','B','C','D','A']
    for i in range(5):
        for j in range(4):
            idx = i * 4 + j
            header_cell(tbl.rows[i].cells[j*1], '', bg=BLUE_LIGHT)  # placeholder
        row = tbl.rows[i]
        for j in range(4):
            q_num = i*4+j+1
            if q_num <= 20:
                cell = row.cells[j]
                set_cell_bg(cell, BLUE_LIGHT if i%2==0 else GRAY_LIGHT)
                set_cell_border(cell)
                cell_write(cell, f'{q_num}. ({sample_ans[q_num-1]})', center=True)

    doc.add_paragraph()
    section_heading(doc, '評分建議與補救方向', level=2)
    for note in [
        '• 選擇題得分 < 60%：建議複習字詞辨析與基礎閱讀理解',
        '• 填充題得分 < 60%：建議重新背誦關鍵字詞',
        '• 問答題得分 < 60%：加強段落寫作與引用文本能力',
    ]:
        p = doc.add_paragraph()
        r = p.add_run(note)
        r.font.size = Pt(11); r.font.name = '標楷體'; r.font.color.rgb = DARK_TEXT
        set_east_asia_font(r)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject',  default='國語文')
    parser.add_argument('--grade',    default='國中九年級')
    parser.add_argument('--range',    default='背影')
    parser.add_argument('--types',    default='choice:40,fill:20,short:40')
    parser.add_argument('--total',    type=int, default=100)
    parser.add_argument('--output',   default='試卷.docx')
    args = parser.parse_args()

    doc = new_doc_a4()
    add_header_footer(doc, f'{args.subject}試卷｜{args.grade}｜{args.range}')

    cover_page(doc, '定期評量試卷',
               f'{args.subject}｜{args.grade}',
               {'科目': args.subject, '年級': args.grade,
                '考試範圍': args.range, '總分': f'{args.total} 分',
                '班級': '　　年　　班', '姓名': '　　　　　　',
                '座號': '　　　　', '得分': '　　　　'})

    add_exam_header(doc, args.subject, args.grade, args.range, args.total)
    add_choice_section(doc, args.subject, args.grade, args.range)
    add_fill_section(doc, args.range)
    add_short_answer_section(doc, args.range)
    add_answer_key(doc, args.subject, args.grade, args.range)

    doc.save(args.output)
    print(f'✓ 試卷已儲存：{args.output}')

if __name__ == '__main__':
    main()
