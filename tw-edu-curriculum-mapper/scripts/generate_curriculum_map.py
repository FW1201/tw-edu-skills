#!/usr/bin/env python3
"""課程地圖 Excel 生成腳本"""
import argparse
from openpyxl import Workbook
from openpyxl.styles import (PatternFill, Font, Alignment, Border, Side,
                              GradientFill)
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

# 色彩
C_DEEP_BLUE  = "1A5276"
C_MID_BLUE   = "2471A3"
C_LIGHT_BLUE = "EBF5FB"
C_ALT_ROW    = "F8F9FA"
C_HEADER_TXT = "FFFFFF"
C_GOLD       = "D4AC0D"
C_GREEN      = "1E8449"
C_ORANGE     = "CA6F1E"
C_GRAY       = "566573"

def hdr_font(size=11, bold=True, color=C_HEADER_TXT):
    return Font(name='微軟正黑體', size=size, bold=bold, color=color)

def body_font(size=11, bold=False, color="1C2A35"):
    return Font(name='微軟正黑體', size=size, bold=bold, color=color)

def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def thin_border():
    s = Side(style='thin', color="2471A3")
    return Border(left=s, right=s, top=s, bottom=s)

def center_align(wrap=True):
    return Alignment(horizontal='center', vertical='center', wrap_text=wrap)

def left_align(wrap=True):
    return Alignment(horizontal='left', vertical='center', wrap_text=wrap)

def style_header(cell, text, bg=C_MID_BLUE, size=11):
    cell.value = text
    cell.font = hdr_font(size=size)
    cell.fill = fill(bg)
    cell.alignment = center_align()
    cell.border = thin_border()

def style_data(cell, text, row_idx=0, center=False):
    cell.value = text
    bg = C_LIGHT_BLUE if row_idx % 2 == 0 else C_ALT_ROW
    cell.fill = fill(bg)
    cell.font = body_font()
    cell.alignment = center_align() if center else left_align()
    cell.border = thin_border()


def create_overview_sheet(wb, subject, grade, semester, units):
    ws = wb.active
    ws.title = "學期課程總覽"

    # 標題列
    ws.merge_cells("A1:H1")
    title_cell = ws["A1"]
    title_cell.value = f"{grade}｜{subject}｜{semester}學期課程地圖"
    title_cell.font = Font(name='微軟正黑體', size=16, bold=True, color=C_DEEP_BLUE)
    title_cell.fill = fill("D6EAF8")
    title_cell.alignment = center_align()
    ws.row_dimensions[1].height = 36

    # 表頭
    headers = ["週次", "單元名稱", "教學主題/重點", "節數", "核心素養", "學習表現", "評量方式", "重大議題"]
    col_widths = [6, 18, 28, 6, 22, 22, 16, 14]
    for j, (h, w) in enumerate(zip(headers, col_widths), 1):
        cell = ws.cell(row=2, column=j)
        style_header(cell, h, bg=C_DEEP_BLUE)
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.row_dimensions[2].height = 22

    # 資料列（範例）
    week = 1
    for i, unit in enumerate(units):
        row = i + 3
        sample_data = [
            f"{week}–{week+1}",
            unit,
            f"《{unit}》核心概念與技能教學",
            "4",
            "語-J-B1：閱讀理解與表達",
            "5-Ⅳ-2：分析篇章結構",
            "學習單、口頭問答",
            "品德教育（品）",
        ]
        for j, text in enumerate(sample_data, 1):
            style_data(ws.cell(row=row, column=j), text, row_idx=i,
                       center=(j in [1, 4]))
        ws.row_dimensions[row].height = 30
        week += 2

    # 凍結首兩列
    ws.freeze_panes = "A3"
    ws.auto_filter.ref = f"A2:H{2 + len(units)}"


def create_performance_sheet(wb, units):
    ws = wb.create_sheet("學習表現對應")
    ws.merge_cells("A1:F1")
    c = ws["A1"]
    c.value = "學習表現對應表"
    c.font = Font(name='微軟正黑體', size=14, bold=True, color=C_DEEP_BLUE)
    c.fill = fill("D6EAF8")
    c.alignment = center_align()
    ws.row_dimensions[1].height = 32

    headers = ["單元名稱", "學習表現代碼", "說明", "布魯姆層次", "評量方式", "備註"]
    col_widths = [18, 14, 32, 12, 18, 14]
    for j, (h, w) in enumerate(zip(headers, col_widths), 1):
        style_header(ws.cell(row=2, column=j), h, bg=C_MID_BLUE)
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.row_dimensions[2].height = 22

    bloom_levels = ["C1 記憶", "C2 理解", "C3 應用", "C4 分析", "C5 評鑑", "C6 創造"]
    sample_perf = ["5-Ⅳ-1", "5-Ⅳ-2", "6-Ⅳ-1"]
    sample_desc = ["閱讀並理解多元文本", "分析篇章結構與寫作手法", "依文體撰寫作文"]

    row = 3
    for i, unit in enumerate(units):
        for k in range(min(2, len(sample_perf))):
            data = [unit if k == 0 else "", sample_perf[k % 3],
                    sample_desc[k % 3], bloom_levels[k+1],
                    "學習單、口頭", ""]
            for j, text in enumerate(data, 1):
                style_data(ws.cell(row=row, column=j), text, row_idx=i)
            ws.row_dimensions[row].height = 22
            row += 1

    ws.freeze_panes = "A3"


def create_content_sheet(wb, units):
    ws = wb.create_sheet("學習內容對應")
    ws.merge_cells("A1:E1")
    c = ws["A1"]
    c.value = "學習內容對應表"
    c.font = Font(name='微軟正黑體', size=14, bold=True, color=C_DEEP_BLUE)
    c.fill = fill("D6EAF8")
    c.alignment = center_align()
    ws.row_dimensions[1].height = 32

    headers = ["單元名稱", "學習內容代碼", "說明", "教學材料/媒材", "備註"]
    col_widths = [18, 14, 32, 22, 14]
    for j, (h, w) in enumerate(zip(headers, col_widths), 1):
        style_header(ws.cell(row=2, column=j), h, bg=C_MID_BLUE)
        ws.column_dimensions[get_column_letter(j)].width = w

    sample_cont = [("Ac-Ⅳ-3", "記敘文的時間、空間、人物情節"),
                   ("Ca-Ⅳ-1", "修辭技巧運用")]
    row = 3
    for i, unit in enumerate(units):
        for k, (code, desc) in enumerate(sample_cont):
            data = [unit if k == 0 else "", code, desc, "教科書、補充教材", ""]
            for j, text in enumerate(data, 1):
                style_data(ws.cell(row=row, column=j), text, row_idx=i)
            ws.row_dimensions[row].height = 22
            row += 1
    ws.freeze_panes = "A3"


def create_crossdomain_sheet(wb, units, subject):
    ws = wb.create_sheet("跨域連結矩陣")
    related = ["英語", "社會", "自然", "藝術", "健體", "資訊", "綜合"]

    ws.merge_cells(f"A1:{get_column_letter(len(related)+1)}1")
    c = ws["A1"]
    c.value = f"{subject}跨域連結矩陣"
    c.font = Font(name='微軟正黑體', size=14, bold=True, color=C_DEEP_BLUE)
    c.fill = fill("D6EAF8")
    c.alignment = center_align()
    ws.row_dimensions[1].height = 32

    # 表頭
    style_header(ws.cell(row=2, column=1), "單元名稱", bg=C_DEEP_BLUE)
    ws.column_dimensions["A"].width = 20
    for j, subj in enumerate(related, 2):
        style_header(ws.cell(row=2, column=j), subj, bg=C_DEEP_BLUE)
        ws.column_dimensions[get_column_letter(j)].width = 10
    ws.row_dimensions[2].height = 22

    symbols = {"強": ("●", "1A5276"), "中": ("◎", "D4AC0D"), "": ("", C_ALT_ROW)}
    import random
    random.seed(42)
    for i, unit in enumerate(units):
        row = i + 3
        style_data(ws.cell(row=row, column=1), unit, row_idx=i)
        for j in range(2, len(related) + 2):
            level = random.choice(["強", "中", "中", ""])
            sym, color = symbols.get(level, ("", C_ALT_ROW))
            cell = ws.cell(row=row, column=j)
            bg = C_LIGHT_BLUE if i % 2 == 0 else C_ALT_ROW
            cell.value = sym
            cell.fill = fill(bg)
            cell.font = Font(name='微軟正黑體', size=12, bold=(level=="強"), color=color)
            cell.alignment = center_align()
            cell.border = thin_border()
        ws.row_dimensions[row].height = 22

    # 圖例
    legend_row = len(units) + 4
    ws.cell(row=legend_row, column=1).value = "圖例："
    ws.cell(row=legend_row, column=1).font = body_font(bold=True)
    ws.cell(row=legend_row, column=2).value = "● 強連結"
    ws.cell(row=legend_row, column=2).font = Font(name='微軟正黑體', size=11, color="1A5276")
    ws.cell(row=legend_row, column=3).value = "◎ 中等連結"
    ws.cell(row=legend_row, column=3).font = Font(name='微軟正黑體', size=11, color="D4AC0D")

    ws.freeze_panes = "B3"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject',  default='國語文')
    parser.add_argument('--grade',    default='國中八年級')
    parser.add_argument('--semester', default='上')
    parser.add_argument('--units',    default='第一課,第二課,第三課,第四課,第五課,第六課')
    parser.add_argument('--output',   default='課程地圖.xlsx')
    args = parser.parse_args()

    units = [u.strip() for u in args.units.split(',') if u.strip()]

    wb = Workbook()
    create_overview_sheet(wb, args.subject, args.grade, args.semester, units)
    create_performance_sheet(wb, units)
    create_content_sheet(wb, units)
    create_crossdomain_sheet(wb, units, args.subject)

    wb.save(args.output)
    print(f"✓ 課程地圖已儲存：{args.output}")

if __name__ == '__main__':
    main()
