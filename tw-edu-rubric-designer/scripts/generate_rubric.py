#!/usr/bin/env python3
"""評量規準生成腳本"""
import argparse, sys
sys.path.insert(0, '.')
from tw_edu_doc_utils import *

LEVELS = ["傑出 (4)", "精熟 (3)", "基礎 (2)", "待加強 (1)"]
LEVEL_COLORS = [GREEN, BLUE_MID, GOLD, ORANGE]

DEFAULT_DIMS = {
    "作文": ["內容充實度", "組織結構", "語言表達", "修辭技巧", "標點符號"],
    "口頭報告": ["內容準備", "口語表達", "肢體語言", "時間掌控", "問答應對"],
    "閱讀理解": ["字面理解", "推論思考", "評鑑創造", "文本引用"],
}

def add_analytic_rubric(doc, task, dimensions, subject, grade):
    section_heading(doc, f'《{task}》分析式評量規準')
    p = doc.add_paragraph()
    r = p.add_run(f'科目：{subject}｜年級：{grade}｜任務：{task}')
    r.font.size = Pt(11); r.font.name = '標楷體'
    r.font.color.rgb = DARK_TEXT
    set_east_asia_font(r)
    doc.add_paragraph()

    cols = len(LEVELS) + 2
    tbl = doc.add_table(rows=len(dimensions)+2, cols=cols)
    tbl.style = 'Table Grid'
    widths = [Cm(1.5), Cm(3)] + [Cm(3.5)] * len(LEVELS)
    for j, w in enumerate(widths):
        tbl.columns[j].width = w

    # 表頭
    header_cell(tbl.rows[0].cells[0], '向度', bg=BLUE_DEEP)
    header_cell(tbl.rows[0].cells[1], '說明', bg=BLUE_DEEP)
    for j, (lvl, color) in enumerate(zip(LEVELS, LEVEL_COLORS), 2):
        header_cell(tbl.rows[0].cells[j], lvl, bg=color)

    # 各向度
    dim_descs = {
        "內容充實度": "文章主題是否明確、論點是否充分、舉例是否具體",
        "組織結構": "文章是否有清晰的開頭、中間、結尾，段落銜接是否流暢",
        "語言表達": "用詞是否恰當、句子是否通順、表達是否清晰",
        "修辭技巧": "是否運用比喻、排比等修辭增強表達效果",
        "標點符號": "標點符號使用是否正確",
    }
    level_descs = {
        "傑出 (4)": "完全達到，表現超越預期",
        "精熟 (3)": "符合要求，表現穩定",
        "基礎 (2)": "部分達到，仍有進步空間",
        "待加強 (1)": "尚未達到，需要加強指導",
    }
    for i, dim in enumerate(dimensions, 1):
        row = tbl.rows[i]
        data_cell(row.cells[0], str(i), row_idx=i, center=True)
        data_cell(row.cells[1], f'{dim}\n{dim_descs.get(dim, "")}', row_idx=i)
        for j, lvl in enumerate(LEVELS, 2):
            data_cell(row.cells[j], level_descs.get(lvl, ''), row_idx=i)

    # 總分列
    last_row = tbl.rows[-1]
    header_cell(last_row.cells[0], '總分', bg=BLUE_DEEP)
    header_cell(last_row.cells[1], f'滿分 {len(dimensions)*4} 分', bg=BLUE_DEEP)
    for j, lvl in enumerate(LEVELS, 2):
        header_cell(last_row.cells[j], f'{len(dimensions)*(5-j)} 分', bg=LEVEL_COLORS[j-2])
    doc.add_paragraph()

def add_self_peer_eval(doc):
    section_heading(doc, '學生自評 / 同儕評量區', level=2)
    tbl = doc.add_table(rows=3, cols=3)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(3.5), Cm(8), Cm(5.5)]):
        tbl.columns[j].width = w
    header_cell(tbl.rows[0].cells[0], '評量人')
    header_cell(tbl.rows[0].cells[1], '最欣賞之處')
    header_cell(tbl.rows[0].cells[2], '建議改進方向')
    for i, label in enumerate(['自評', '同儕評量'], 1):
        data_cell(tbl.rows[i].cells[0], label, row_idx=i, center=True)
        data_cell(tbl.rows[i].cells[1], '', row_idx=i)
        data_cell(tbl.rows[i].cells[2], '', row_idx=i)
        tbl.rows[i].height = Cm(2.5)
    doc.add_paragraph()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task',       default='議論文寫作')
    parser.add_argument('--subject',    default='國語文')
    parser.add_argument('--grade',      default='高中一年級')
    parser.add_argument('--type',       default='analytic', choices=['holistic','analytic'])
    parser.add_argument('--dimensions', default='')
    parser.add_argument('--output',     default='評量規準.docx')
    args = parser.parse_args()

    dims_raw = args.dimensions
    if dims_raw:
        dims = [d.strip() for d in dims_raw.split(',') if d.strip()]
    else:
        for key in DEFAULT_DIMS:
            if key in args.task:
                dims = DEFAULT_DIMS[key]; break
        else:
            dims = ["內容充實度", "組織結構", "語言表達", "修辭技巧", "標點符號"]

    doc = new_doc_a4()
    add_header_footer(doc, f'評量規準｜{args.task}｜{args.subject}｜{args.grade}')
    cover_page(doc, f'評量規準\nRubric',
               f'《{args.task}》｜{args.subject}｜{args.grade}',
               {'科目': args.subject, '年級': args.grade,
                '任務名稱': args.task, '日期': str(date.today()),
                '評量類型': '分析式（Analytic）', '等第說明': '4等第制'})
    add_analytic_rubric(doc, args.task, dims, args.subject, args.grade)
    add_self_peer_eval(doc)
    doc.save(args.output)
    print(f'✓ 評量規準已儲存：{args.output}')

if __name__ == '__main__':
    main()
