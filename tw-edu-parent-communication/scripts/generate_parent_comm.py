#!/usr/bin/env python3
"""親師溝通文件生成腳本"""
import argparse, sys
sys.path.insert(0, '.')
from tw_edu_doc_utils import *
from datetime import date

TEMPLATES = {
    'newsletter': {
        'title': '班級通訊',
        'greeting': '親愛的家長您好：',
        'closing': '敬請家長多加留意，如有疑問歡迎與老師聯繫。\n敬祝　闔家平安',
    },
    'activity': {
        'title': '活動通知單',
        'greeting': '親愛的家長您好：',
        'closing': '感謝您的支持與配合，如有任何問題，請隨時與班導師聯繫。\n敬祝　時祺',
    },
    'care': {
        'title': '關懷信函',
        'greeting': '尊敬的家長您好：',
        'closing': '家校合作是孩子最好的後盾，謝謝您一直以來的信任與支持。\n敬上',
    },
    'behavior': {
        'title': '行為紀錄溝通單',
        'greeting': '尊敬的家長您好：',
        'closing': '衷心希望透過家校合作，共同支持孩子的成長。\n期待您的回覆，謝謝。',
    },
    'grade': {
        'title': '成績說明函',
        'greeting': '親愛的家長您好：',
        'closing': '如對成績或學習狀況有任何疑問，歡迎預約面談。\n敬祝　學習進步',
    },
}

def add_letter(doc, comm_type, content, teacher, class_name):
    tmpl = TEMPLATES.get(comm_type, TEMPLATES['newsletter'])
    today = date.today()
    roc_year = today.year - 1911
    date_str = f'民國 {roc_year} 年 {today.month} 月 {today.day} 日'

    # 信頭
    tbl = doc.add_table(rows=2, cols=3)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(4), Cm(9), Cm(4)]): tbl.columns[j].width = w
    header_cell(tbl.rows[0].cells[0], '班級', bg=BLUE_DEEP)
    data_cell(tbl.rows[0].cells[1], class_name, row_idx=0, center=True)
    header_cell(tbl.rows[0].cells[2], '日期', bg=BLUE_DEEP)
    header_cell(tbl.rows[1].cells[0], '文件性質', bg=BLUE_DEEP)
    data_cell(tbl.rows[1].cells[1], tmpl['title'], row_idx=1, center=True)
    data_cell(tbl.rows[1].cells[2], date_str, row_idx=1, center=True)
    doc.add_paragraph()

    # 稱謂
    p = doc.add_paragraph()
    r = p.add_run(tmpl['greeting'])
    r.font.size = Pt(13); r.bold = True; r.font.name = '標楷體'
    r.font.color.rgb = BLUE_DEEP; set_east_asia_font(r)
    p.paragraph_format.space_after = Pt(6)

    # 正文
    p2 = doc.add_paragraph()
    body = content if content else (
        f'　　本班近期將進行相關教學活動，以下為重要事項說明，'
        f'請家長詳閱並配合辦理。\n\n一、事項說明：\n　　（請教師填入具體內容）\n\n'
        f'二、家長配合事項：\n　　（請教師填入需要家長配合的事項）\n\n'
        f'三、注意事項：\n　　如有任何疑問，請於聯絡簿或以電話聯繫老師。'
    )
    r2 = p2.add_run(body)
    r2.font.size = Pt(12); r2.font.name = '標楷體'; r2.font.color.rgb = DARK_TEXT
    set_east_asia_font(r2)
    p2.paragraph_format.line_spacing = Pt(22)
    p2.paragraph_format.space_after = Pt(12)

    # 結語
    p3 = doc.add_paragraph()
    r3 = p3.add_run(tmpl['closing'])
    r3.font.size = Pt(12); r3.font.name = '標楷體'; r3.font.color.rgb = DARK_TEXT
    set_east_asia_font(r3)
    p3.paragraph_format.space_before = Pt(6)

    # 署名
    doc.add_paragraph()
    p4 = doc.add_paragraph()
    p4.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r4 = p4.add_run(f'{class_name} {teacher} 老師　敬上')
    r4.font.size = Pt(12); r4.font.name = '標楷體'; r4.font.color.rgb = DARK_TEXT
    set_east_asia_font(r4)

    # 回條虛線（如需要）
    if comm_type in ('activity', 'behavior'):
        doc.add_paragraph()
        p5 = doc.add_paragraph()
        r5 = p5.add_run('- - - - - - - - - - - - ✂ 請沿虛線裁下回交老師 - - - - - - - - - - - -')
        r5.font.size = Pt(10); r5.font.color.rgb = RGBColor(0x99,0x99,0x99)
        r5.font.name = '標楷體'; set_east_asia_font(r5)
        p5.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p6 = doc.add_paragraph()
        r6 = p6.add_run(f'□ 我已閱讀上述通知，並了解相關事項。\n'
                        f'家長簽名：＿＿＿＿＿＿　日期：＿＿ 月 ＿＿ 日')
        r6.font.size = Pt(12); r6.font.name = '標楷體'; r6.font.color.rgb = DARK_TEXT
        set_east_asia_font(r6)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type',       default='newsletter',
                        choices=list(TEMPLATES.keys()))
    parser.add_argument('--content',    default='')
    parser.add_argument('--teacher',    default='OOO')
    parser.add_argument('--class_name', default='七年一班')
    parser.add_argument('--output',     default='親師溝通.docx')
    args = parser.parse_args()

    doc = new_doc_a4()
    tmpl = TEMPLATES.get(args.type, TEMPLATES['newsletter'])
    add_header_footer(doc, f'{tmpl["title"]}｜{args.class_name}｜{args.teacher}老師')

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(tmpl['title'])
    r.bold = True; r.font.size = Pt(20); r.font.name = '標楷體'
    r.font.color.rgb = BLUE_DEEP; set_east_asia_font(r)
    p.paragraph_format.space_after = Pt(12)

    add_letter(doc, args.type, args.content, args.teacher, args.class_name)
    doc.save(args.output)
    print(f'✓ 親師溝通文件已儲存：{args.output}')

if __name__ == '__main__':
    main()
