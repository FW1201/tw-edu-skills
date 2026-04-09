#!/usr/bin/env python3
"""班級經營文件生成腳本"""
import argparse, sys
sys.path.insert(0, '.')
from tw_edu_doc_utils import *

def add_class_rules(doc, grade):
    section_heading(doc, '班級公約（由學生共同制定）')
    p = doc.add_paragraph()
    r = p.add_run('★ 班級公約應由全班師生共同討論制定，以下為討論框架，非最終版本')
    r.font.size = Pt(10); r.font.color.rgb = GOLD; r.font.name = '標楷體'
    set_east_asia_font(r)
    doc.add_paragraph()

    areas = [
        ('尊重與傾聽', ['在別人說話時，我們認真聆聽，不打斷他人',
                       '用正向的語言與同學和老師溝通',
                       '尊重每個人的不同想法和背景']),
        ('學習態度', ['準時到校，準備好學習所需的材料',
                     '課堂中保持專注，遇到不懂的地方主動發問',
                     '認真完成作業，遇到困難先自己嘗試']),
        ('班級責任', ['共同維護教室整潔，物品用後歸回原位',
                     '輪流負責班級日常工作（日期、黑板等）',
                     '遇到問題，先試著溝通解決，再請老師協助']),
        ('科技使用', ['手機在課堂中收起，依老師指示使用',
                     '合法、安全地使用網路資源',
                     '不拍攝、傳送他人照片，保護同學隱私']),
    ]
    for area_name, rules in areas:
        section_heading(doc, f'▸ {area_name}', level=2)
        for i, rule in enumerate(rules, 1):
            p2 = doc.add_paragraph()
            r2 = p2.add_run(f'  {i}. {rule}')
            r2.font.size = Pt(11); r2.font.name = '標楷體'; r2.font.color.rgb = DARK_TEXT
            set_east_asia_font(r2)
            p2.paragraph_format.space_after = Pt(3)
        doc.add_paragraph()

    # 簽名區
    tbl = doc.add_table(rows=2, cols=3)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(5.67), Cm(5.67), Cm(5.66)]):
        tbl.columns[j].width = w
    for j, h in enumerate(['全班學生簽名', '班導師簽名', '家長代表簽名']):
        header_cell(tbl.rows[0].cells[j], h)
        data_cell(tbl.rows[1].cells[j], '（集體簽名或蓋章）', row_idx=1, center=True)
        tbl.rows[1].height = Cm(2.5)
    doc.add_paragraph()

def add_pbs_plan(doc, grade, challenge):
    section_heading(doc, '積極行為支持（PBS）計畫')
    tbl = doc.add_table(rows=4, cols=2)
    tbl.style = 'Table Grid'
    tbl.columns[0].width = Cm(4); tbl.columns[1].width = Cm(13)

    rows_data = [
        ('預防層次\n（改變環境）', '• 安排座位：考量同儕互動，避免衝突組合\n'
         '• 課程安排：高投入活動穿插於靜態學習之間\n'
         '• 環境布置：減少視覺干擾，建立清楚的區域標示\n'
         f'• 針對「{challenge}」：_______________'),
        ('教導層次\n（建立替代行為）', '• 明確教導期望行為（不僅僅說「不要」，要說「應該」）\n'
         '• 使用角色扮演練習適當行為\n'
         '• 建立班級語言：同意的手勢、需要幫助的信號\n'
         f'• 針對「{challenge}」：_______________'),
        ('增強層次\n（正向鼓勵）', '• 捕捉良好行為立即給予具體正向回饋\n'
         '• 班級增強系統：___（印花/點數/班幣）\n'
         '• 個人增強計畫（適用特殊需求學生）\n'
         '• 避免過多懲罰性手段'),
    ]
    header_cell(tbl.rows[0].cells[0], '層次', bg=BLUE_DEEP)
    header_cell(tbl.rows[0].cells[1], '具體做法', bg=BLUE_DEEP)
    for i, (level, action) in enumerate(rows_data, 1):
        header_cell(tbl.rows[i].cells[0], level, bg=BLUE_MID)
        data_cell(tbl.rows[i].cells[1], action, row_idx=i)
        tbl.rows[i].height = Cm(3.5)
    doc.add_paragraph()

def add_weekly_log(doc):
    section_heading(doc, '導師週記記錄表')
    tbl = doc.add_table(rows=7, cols=3)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(3), Cm(7), Cm(7)]): tbl.columns[j].width = w
    header_cell(tbl.rows[0].cells[0], '日期')
    header_cell(tbl.rows[0].cells[1], '班級觀察與重要事件')
    header_cell(tbl.rows[0].cells[2], '個別輔導記錄 / 跟進行動')
    days = ['週一', '週二', '週三', '週四', '週五']
    for i, day in enumerate(days, 1):
        data_cell(tbl.rows[i].cells[0], day, row_idx=i, center=True)
        data_cell(tbl.rows[i].cells[1], '', row_idx=i)
        data_cell(tbl.rows[i].cells[2], '', row_idx=i)
        tbl.rows[i].height = Cm(1.5)
    merged = tbl.rows[6].cells[0].merge(tbl.rows[6].cells[2])
    header_cell(merged, '本週省思與下週重點')
    tbl.rows[6].height = Cm(2.0)
    doc.add_paragraph()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type',      default='all',
                        choices=['rules','pbs','weekly','meeting','all'])
    parser.add_argument('--grade',     default='八年級')
    parser.add_argument('--challenge', default='上課分心、手機使用')
    parser.add_argument('--output',    default='班級經營.docx')
    args = parser.parse_args()

    doc = new_doc_a4()
    add_header_footer(doc, f'班級經營工具｜{args.grade}')
    cover_page(doc, '班級經營工具包',
               f'{args.grade}｜{args.challenge}',
               {'年級': args.grade, '主要挑戰': args.challenge, '日期': str(date.today())})

    if args.type in ('rules','all'): add_class_rules(doc, args.grade)
    if args.type in ('pbs','all'): add_pbs_plan(doc, args.grade, args.challenge)
    if args.type in ('weekly','all'): add_weekly_log(doc)
    doc.save(args.output)
    print(f'✓ 班級經營文件已儲存：{args.output}')

if __name__ == '__main__':
    main()
