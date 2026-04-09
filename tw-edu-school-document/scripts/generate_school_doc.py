#!/usr/bin/env python3
"""校園行政文書生成腳本"""
import argparse, sys
sys.path.insert(0, '.')
from tw_edu_doc_utils import *

def add_plan(doc, subject, content, author, school):
    today = date.today(); roc = today.year-1911
    section_heading(doc, '計畫書')
    fields = [
        ('計畫名稱', subject), ('主辦單位/人員', author),
        ('所屬學校', school), ('計畫期程', f'民國 {roc} 年 {today.month} 月起'),
    ]
    tbl = doc.add_table(rows=2, cols=4)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(3), Cm(5.5), Cm(3), Cm(5.5)]): tbl.columns[j].width = w
    header_cell(tbl.rows[0].cells[0], '計畫名稱')
    data_cell(tbl.rows[0].cells[1], subject, row_idx=0)
    header_cell(tbl.rows[0].cells[2], '主辦單位/人員')
    data_cell(tbl.rows[0].cells[3], author, row_idx=0)
    header_cell(tbl.rows[1].cells[0], '所屬學校')
    data_cell(tbl.rows[1].cells[1], school, row_idx=1)
    header_cell(tbl.rows[1].cells[2], '計畫期程')
    data_cell(tbl.rows[1].cells[3], f'民國 {roc} 年 {today.month} 月起', row_idx=1)
    doc.add_paragraph()

    sections = [
        ('一、依據', '依據教育部相關規定及本校年度行事暨教學計畫辦理。'),
        ('二、目的', f'為_{subject}_，特擬訂本計畫。'),
        ('三、辦理時間', f'民國 {roc} 年 {today.month} 月 {today.day} 日'),
        ('四、辦理地點', '（請填入地點）'),
        ('五、參加對象', '（請填入對象）'),
        ('六、活動內容', content if content else '（請填入活動/計畫內容細節）'),
        ('七、預期效益', '（請填入預期達成的具體成效）'),
        ('八、經費概算', '（請填入經費來源與用途）'),
        ('九、注意事項', '（請填入相關注意事項）'),
        ('十、本計畫奉核後實施，修正時亦同。', ''),
    ]
    for title, body in sections:
        p = doc.add_paragraph()
        r = p.add_run(title)
        r.bold = True; r.font.size = Pt(12); r.font.name = '標楷體'
        r.font.color.rgb = BLUE_DEEP; set_east_asia_font(r)
        if body:
            p2 = doc.add_paragraph()
            r2 = p2.add_run(f'　　{body}')
            r2.font.size = Pt(12); r2.font.name = '標楷體'; r2.font.color.rgb = DARK_TEXT
            set_east_asia_font(r2)
            p2.paragraph_format.space_after = Pt(4)
    doc.add_paragraph()

    # 核示欄
    tbl2 = doc.add_table(rows=2, cols=4)
    tbl2.style = 'Table Grid'
    for j, w in enumerate([Cm(4.5)]*4): tbl2.columns[j].width = w
    for j, h in enumerate(['承辦人', '組長', '主任', '校長']):
        header_cell(tbl2.rows[0].cells[j], h)
        data_cell(tbl2.rows[1].cells[j], '', row_idx=1, center=True)
        tbl2.rows[1].height = Cm(2.0)

def add_memo(doc, subject, content, author, school):
    section_heading(doc, '簽呈')
    today = date.today(); roc = today.year-1911
    p = doc.add_paragraph()
    r = p.add_run(f'主旨：{subject}，請 核示。')
    r.font.size = Pt(13); r.bold = True; r.font.name = '標楷體'
    r.font.color.rgb = DARK_TEXT; set_east_asia_font(r)
    p.paragraph_format.space_after = Pt(8)

    for label, body in [('說明：', content if content else '一、緣起：（請填入背景說明）\n二、現況：（請填入目前情形）\n三、建議事項：（請填入具體建議）'),
                        ('擬辦：', '如蒙 核示，即依核定辦理。')]:
        p2 = doc.add_paragraph()
        r2 = p2.add_run(label)
        r2.bold = True; r2.font.size = Pt(12); r2.font.name = '標楷體'
        r2.font.color.rgb = BLUE_DEEP; set_east_asia_font(r2)
        p3 = doc.add_paragraph()
        r3 = p3.add_run(f'　　{body}')
        r3.font.size = Pt(12); r3.font.name = '標楷體'; r3.font.color.rgb = DARK_TEXT
        set_east_asia_font(r3); p3.paragraph_format.space_after = Pt(6)
    doc.add_paragraph()
    p4 = doc.add_paragraph()
    p4.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r4 = p4.add_run(f'承辦人：{author}\n{school}\n民國 {roc} 年 {today.month} 月 {today.day} 日')
    r4.font.size = Pt(12); r4.font.name = '標楷體'; r4.font.color.rgb = DARK_TEXT
    set_east_asia_font(r4)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type',    default='plan',
                        choices=['memo','plan','report','application','curriculum'])
    parser.add_argument('--subject', default='計畫書名稱')
    parser.add_argument('--content', default='')
    parser.add_argument('--author',  default='教師姓名')
    parser.add_argument('--school',  default='學校名稱')
    parser.add_argument('--output',  default='行政文書.docx')
    args = parser.parse_args()

    doc = new_doc_a4()
    add_header_footer(doc, f'行政文書｜{args.school}')
    cover_page(doc, args.subject, f'{args.school}｜{args.author}',
               {'文件類型': args.type, '撰寫人員': args.author,
                '所屬學校': args.school, '日期': str(date.today())})

    if args.type == 'plan': add_plan(doc, args.subject, args.content, args.author, args.school)
    elif args.type == 'memo': add_memo(doc, args.subject, args.content, args.author, args.school)
    else: add_plan(doc, args.subject, args.content, args.author, args.school)

    doc.save(args.output); print(f'✓ 行政文書已儲存：{args.output}')
if __name__ == '__main__': main()
