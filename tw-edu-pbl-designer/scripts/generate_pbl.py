#!/usr/bin/env python3
"""PBL 專題式學習設計腳本"""
import argparse, sys
sys.path.insert(0, '.')
from tw_edu_doc_utils import *

def add_overview(doc, question, subject, grade, weeks, product):
    section_heading(doc, 'PBL 專題設計總覽')
    tbl = doc.add_table(rows=4, cols=4)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(3), Cm(5.5), Cm(3), Cm(5.5)]): tbl.columns[j].width = w
    info = [('驅動問題', question), ('科目/年級', f'{subject}｜{grade}'),
            ('學習週數', f'{weeks} 週'), ('最終成品', product)]
    for i in range(2):
        for j in range(2):
            idx = i*2+j
            header_cell(tbl.rows[i].cells[j*2], info[idx][0])
            data_cell(tbl.rows[i].cells[j*2+1], info[idx][1], row_idx=i)
    merged1 = tbl.rows[2].cells[0].merge(tbl.rows[2].cells[3])
    header_cell(merged1, '核心知識與21世紀技能', bg=BLUE_DEEP)
    merged2 = tbl.rows[3].cells[0].merge(tbl.rows[3].cells[3])
    data_cell(merged2, '批判性思考、溝通表達、協作合作、創造力（4C）\n'
              '對應核心素養：（請依108課綱填入）', row_idx=3)
    tbl.rows[3].height = Cm(1.5)
    doc.add_paragraph()

def add_timeline(doc, weeks, product):
    section_heading(doc, '學習進度時間表')
    phases = []
    if weeks <= 3:
        phases = [
          (f'第1週', '啟動與問題探究', '驅動問題提出、小組分工、背景知識蒐集'),
          (f'第2週', '深度研究與設計', '資料分析、草稿設計、形成性評量回饋'),
          (f'第{weeks}週', f'完成{product}與發表', '成品製作、排演/演練、正式發表'),
        ]
    else:
        mid = weeks // 2
        phases = [
          (f'第1-2週', '啟動階段', '驅動問題提出、小組組成、任務分析、資源盤點'),
          (f'第3-{mid}週', '探究階段', '深度研究、資料蒐集分析、概念建立、中期成果分享'),
          (f'第{mid+1}-{weeks-1}週', '設計製作階段', f'{product}設計、製作、反覆修訂'),
          (f'第{weeks}週', '發表評量階段', '正式發表、同儕評量、反思回饋'),
        ]

    tbl = doc.add_table(rows=len(phases)+1, cols=3)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(3.5), Cm(5), Cm(8.5)]): tbl.columns[j].width = w
    for j, h in enumerate(['時程', '里程碑', '活動說明']): header_cell(tbl.rows[0].cells[j], h)
    for i, (time, mile, desc) in enumerate(phases, 1):
        data_cell(tbl.rows[i].cells[0], time, row_idx=i, center=True)
        header_cell(tbl.rows[i].cells[1], mile, bg=BLUE_MID)
        data_cell(tbl.rows[i].cells[2], desc, row_idx=i)
        tbl.rows[i].height = Cm(1.4)
    doc.add_paragraph()

def add_scaffold_design(doc):
    section_heading(doc, '鷹架設計規劃')
    items = [
        ('知識鷹架', '學生需要先學習哪些基礎知識才能進行專題？', '前導課程、閱讀材料、影片資源'),
        ('技能鷹架', '學生需要哪些技能才能完成成品？', '工具操作教學、寫作指導、簡報技巧'),
        ('流程鷹架', '如何引導學生的研究與設計過程？', '研究計畫表、進度追蹤表、定期 check-in'),
        ('評量鷹架', '如何幫助學生了解優秀成品的標準？', '評量規準說明、範例分析、同儕回饋機制'),
    ]
    tbl = doc.add_table(rows=len(items)+1, cols=3)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(3.5), Cm(7), Cm(6.5)]): tbl.columns[j].width = w
    for j, h in enumerate(['鷹架類型', '問題/目標', '具體做法']): header_cell(tbl.rows[0].cells[j], h)
    for i, (sc_type, goal, method) in enumerate(items, 1):
        header_cell(tbl.rows[i].cells[0], sc_type, bg=BLUE_MID)
        data_cell(tbl.rows[i].cells[1], goal, row_idx=i)
        data_cell(tbl.rows[i].cells[2], method, row_idx=i)
        tbl.rows[i].height = Cm(1.4)
    doc.add_paragraph()

def add_group_template(doc):
    section_heading(doc, '小組任務分工框架')
    roles = [
        ('專案經理', '掌握整體進度，協調組員，確保準時完成各里程碑'),
        ('首席研究員', '負責主要資料蒐集與整理，確保研究深度'),
        ('設計/創作負責人', f'主導最終成品的設計與製作'),
        ('溝通與發表負責人', '負責簡報製作與對外溝通、口頭發表'),
        ('品質把關', '檢核成品品質，對照評量規準，提出改進建議'),
    ]
    tbl = doc.add_table(rows=len(roles)+1, cols=3)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(4), Cm(7.5), Cm(5.5)]): tbl.columns[j].width = w
    for j, h in enumerate(['角色名稱', '主要職責', '組員姓名']): header_cell(tbl.rows[0].cells[j], h)
    for i, (role, duty) in enumerate(roles, 1):
        header_cell(tbl.rows[i].cells[0], role, bg=BLUE_MID)
        data_cell(tbl.rows[i].cells[1], duty, row_idx=i)
        data_cell(tbl.rows[i].cells[2], '', row_idx=i)
        tbl.rows[i].height = Cm(1.2)
    doc.add_paragraph()

def add_final_rubric(doc, product):
    section_heading(doc, f'最終成品評量規準：{product}')
    dimensions = [
        ('內容深度', f'{product}的內容是否充實、有依據，展現對驅動問題的深度理解'),
        ('創意與設計', '成品的呈現方式是否具有創意，設計是否清晰吸引'),
        ('溝通表達', '發表時是否清楚表達想法，能夠回應觀眾問題'),
        ('協作過程', '小組合作是否良好，每位成員是否有實質貢獻'),
        ('反思與成長', '能否清楚說明學習過程中的挑戰與收穫'),
    ]
    levels = ['傑出(4)', '精熟(3)', '基礎(2)', '待加強(1)']
    tbl = doc.add_table(rows=len(dimensions)+1, cols=len(levels)+1)
    tbl.style = 'Table Grid'
    col_widths = [Cm(3.5)] + [Cm(3.4)] * len(levels)
    for j, w in enumerate(col_widths): tbl.columns[j].width = w
    header_cell(tbl.rows[0].cells[0], '評量向度', bg=BLUE_DEEP)
    level_colors = [GREEN, BLUE_MID, GOLD, ORANGE]
    for j, (lvl, color) in enumerate(zip(levels, level_colors), 1):
        header_cell(tbl.rows[0].cells[j], lvl, bg=color)
    for i, (dim, desc) in enumerate(dimensions, 1):
        header_cell(tbl.rows[i].cells[0], dim, bg=BLUE_MID)
        data_cell(tbl.rows[i].cells[1], '完全達到，有亮點表現', row_idx=i)
        data_cell(tbl.rows[i].cells[2], '符合期待，表現穩定', row_idx=i)
        data_cell(tbl.rows[i].cells[3], '部分達到，仍有不足', row_idx=i)
        data_cell(tbl.rows[i].cells[4], '尚未達到，需指導', row_idx=i)
        tbl.rows[i].height = Cm(1.3)
    doc.add_paragraph()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--question', default='如果你是市長，你會如何解決城市中的垃圾問題？')
    parser.add_argument('--subject',  default='社會')
    parser.add_argument('--grade',    default='國中八年級')
    parser.add_argument('--weeks',    type=int, default=4)
    parser.add_argument('--product',  default='政策提案簡報')
    parser.add_argument('--output',   default='PBL設計方案.docx')
    args = parser.parse_args()

    doc = new_doc_a4()
    add_header_footer(doc, f'PBL設計｜{args.subject}｜{args.grade}')
    cover_page(doc, '專題式學習（PBL）設計方案',
               args.question,
               {'驅動問題': args.question[:20]+'…', '科目': args.subject,
                '年級': args.grade, '週數': f'{args.weeks} 週',
                '最終成品': args.product, '建立日期': str(date.today())})
    add_overview(doc, args.question, args.subject, args.grade, args.weeks, args.product)
    add_timeline(doc, args.weeks, args.product)
    add_scaffold_design(doc)
    add_group_template(doc)
    add_final_rubric(doc, args.product)
    doc.save(args.output)
    print(f'✓ PBL 設計方案已儲存：{args.output}')

if __name__ == '__main__':
    main()
