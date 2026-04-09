#!/usr/bin/env python3
"""跨領域課程設計文件生成腳本"""
import argparse, sys
sys.path.insert(0, '.')
from tw_edu_doc_utils import *

def add_overview_table(doc, question, subjects, grade, weeks):
    section_heading(doc, '跨領域課程設計總覽')
    tbl = doc.add_table(rows=3, cols=4)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(3), Cm(5.5), Cm(3), Cm(5.5)]): tbl.columns[j].width = w
    info = [
        ('核心問題', question), ('參與科目', '、'.join(subjects)),
        ('年級', grade), ('學習週數', f'{weeks} 週'),
    ]
    for i in range(2):
        for j in range(2):
            idx = i*2+j
            header_cell(tbl.rows[i].cells[j*2], info[idx][0])
            data_cell(tbl.rows[i].cells[j*2+1], info[idx][1], row_idx=i)
    merged = tbl.rows[2].cells[0].merge(tbl.rows[2].cells[3])
    header_cell(merged, '課程理念說明', bg=BLUE_DEEP)
    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run(
        f'本跨領域課程以「{question}」為核心探究問題，整合 {" 、 ".join(subjects)} 等領域，'
        f'引導學生在真實情境中運用跨科知識解決問題，呼應 108 課綱「彈性學習課程」與「跨領域學習」精神。'
    )
    r.font.size = Pt(11); r.font.name = '標楷體'; r.font.color.rgb = DARK_TEXT
    set_east_asia_font(r); p.paragraph_format.line_spacing = Pt(20)
    doc.add_paragraph()

def add_subject_contribution(doc, question, subjects):
    section_heading(doc, '跨科學習地圖：各科貢獻矩陣')
    p = doc.add_paragraph()
    r = p.add_run('▸ 每個科目在此跨領域課程中的獨特貢獻與學習重點')
    r.font.size = Pt(10); r.font.color.rgb = BLUE_MID; r.font.name = '標楷體'
    set_east_asia_font(r)
    doc.add_paragraph()

    contrib_map = {
        '國語文': ('語文理解與表達', '閱讀相關文本、撰寫報告與口頭發表'),
        '社會': ('社會脈絡分析', '探討議題的歷史、地理、公民面向'),
        '自然': ('科學探究方法', '資料蒐集、實驗設計、科學解釋'),
        '數學': ('數量分析', '統計資料、圖表製作、數據解讀'),
        '英語': ('國際視野', '閱讀英文資料、進行英語簡報'),
        '藝術': ('創意呈現', '視覺設計、藝術表達成果'),
        '資訊': ('數位工具應用', '使用科技輔助研究與呈現'),
        '健體': ('身心健康連結', '探討議題的健康與體適能面向'),
        '綜合': ('生涯與服務', '連結生活情境、服務學習設計'),
    }

    tbl = doc.add_table(rows=len(subjects)+1, cols=4)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(3), Cm(4), Cm(5.5), Cm(4.5)]): tbl.columns[j].width = w
    for j, h in enumerate(['科目', '主要知識技能', '在本課程的貢獻', '學習表現代碼']): header_cell(tbl.rows[0].cells[j], h)
    for i, subj in enumerate(subjects, 1):
        skill, contrib = contrib_map.get(subj, ('各科知識', '依實際課程設計'))
        data_cell(tbl.rows[i].cells[0], subj, row_idx=i, center=True)
        data_cell(tbl.rows[i].cells[1], skill, row_idx=i)
        data_cell(tbl.rows[i].cells[2], contrib, row_idx=i)
        data_cell(tbl.rows[i].cells[3], '（請填入）', row_idx=i, center=True)
        tbl.rows[i].height = Cm(1.3)
    doc.add_paragraph()

def add_activity_sequence(doc, question, subjects, weeks):
    section_heading(doc, '學習活動序列（時間軸）')
    phase_num = min(weeks, 5)
    phase_labels = ['啟動探究', '深度研究', '跨科整合', '成品設計', '發表反思'][:phase_num]
    week_per = max(1, weeks // phase_num)

    tbl = doc.add_table(rows=phase_num+1, cols=5)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(2), Cm(3), Cm(5), Cm(4.5), Cm(2.5)]): tbl.columns[j].width = w
    for j, h in enumerate(['週次', '階段', '主要活動', '各科學習重點', '里程碑']): header_cell(tbl.rows[0].cells[j], h)

    activities = [
        (f'第1-{week_per}週', '啟動探究',
         f'• 提出核心問題：「{question[:20]}...」\n• 進行問題分析，拆解為子問題\n• 組成跨科學習小組',
         '各科教師說明各自的探究角度', '問題分析完成'),
        (f'第{week_per+1}-{week_per*2}週', '深度研究',
         '• 各組依分工蒐集資料\n• 進行田野調查、訪談或實驗\n• 中期報告（口頭10分鐘）',
         '各科教師提供資源與指導', '中期報告通過'),
        (f'第{week_per*2+1}-{weeks-1}週', '整合設計',
         f'• 整合各科研究成果\n• 設計最終成品\n• 同儕回饋與修訂',
         '跨科教師聯合指導', '成品草稿完成'),
        (f'第{weeks}週', '發表反思',
         '• 正式成果發表\n• 同儕與教師評量\n• 個人學習反思',
         '評量規準說明', '完成發表'),
        ('彈性', '補充活動', '依學習進度調整', '各科教師協商', '——'),
    ]
    for i, (week, phase, act, sci, mile) in enumerate(activities[:phase_num], 1):
        data_cell(tbl.rows[i].cells[0], week, row_idx=i, center=True)
        header_cell(tbl.rows[i].cells[1], phase, bg=BLUE_MID)
        data_cell(tbl.rows[i].cells[2], act, row_idx=i)
        data_cell(tbl.rows[i].cells[3], sci, row_idx=i)
        data_cell(tbl.rows[i].cells[4], mile, row_idx=i, center=True)
        tbl.rows[i].height = Cm(2.5)
    doc.add_paragraph()

def add_authentic_assessment(doc, question):
    section_heading(doc, '真實性評量設計')
    tbl = doc.add_table(rows=5, cols=2)
    tbl.style = 'Table Grid'
    tbl.columns[0].width = Cm(4); tbl.columns[1].width = Cm(13)
    rows_data = [
        ('最終成品形式', '（教師依課程決定：簡報/報告/影片/展覽/提案/社區行動等）'),
        ('評量向度', '• 內容深度（30%）：研究是否深入、有依據\n• 跨科整合（30%）：是否有效連結各科知識\n• 溝通表達（20%）：是否清楚呈現想法\n• 協作過程（20%）：小組合作是否有效'),
        ('形成性評量節點', '• 第1週：問題分析單（診斷先備知識）\n• 中期：進度報告（口頭回饋）\n• 發表前：同儕評量（草稿互評）'),
        ('反思評量', '個人學習反思日誌：記錄每週學習收穫與困惑\n最終反思：「這個課程讓我最大的改變是______」'),
    ]
    header_cell(tbl.rows[0].cells[0], '評量項目', bg=BLUE_DEEP)
    header_cell(tbl.rows[0].cells[1], '說明', bg=BLUE_DEEP)
    for i, (label, content) in enumerate(rows_data, 1):
        header_cell(tbl.rows[i].cells[0], label, bg=BLUE_MID)
        data_cell(tbl.rows[i].cells[1], content, row_idx=i)
        tbl.rows[i].height = Cm(2.0)
    doc.add_paragraph()

def add_implementation_notes(doc, subjects):
    section_heading(doc, '實施注意事項與跨科協作建議')
    notes = [
        ('排課建議', f'建議採「協同教學」或「相鄰課節」排課，以利跨科教師協作。'
                     f'每2週至少安排一次跨科教師共同備課（30-60分鐘）。'),
        ('教師分工', f'建議指定一位「課程協調教師」統整進度。'
                     f'各科教師({" 、 ".join(subjects)})明確分工，避免重複教學。'),
        ('評量整合', '跨領域成品建議採「聯合評量」，各科教師共同評分，'
                     '確保評量面向能反映跨科學習成果。'),
        ('差異化支援', '提供不同程度學生的鷹架選擇：基礎（更多引導框架）、'
                       '標準（適度自主）、進階（開放探究）。'),
        ('家長溝通', '在課程開始前向家長說明跨領域課程的目標與評量方式，'
                     '減少「這節課要上什麼」的疑慮。'),
    ]
    for label, content in notes:
        p = doc.add_paragraph()
        r = p.add_run(f'▸ {label}：')
        r.bold = True; r.font.size = Pt(11); r.font.name = '標楷體'
        r.font.color.rgb = BLUE_DEEP; set_east_asia_font(r)
        p2 = doc.add_paragraph()
        r2 = p2.add_run(f'　　{content}')
        r2.font.size = Pt(11); r2.font.name = '標楷體'; r2.font.color.rgb = DARK_TEXT
        set_east_asia_font(r2); p2.paragraph_format.space_after = Pt(8)
    doc.add_paragraph()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--question', default='如果城市消失了，我們如何重建一個永續的家園？')
    parser.add_argument('--subjects', default='社會,自然,國語文,藝術')
    parser.add_argument('--grade',    default='國中八年級')
    parser.add_argument('--weeks',    type=int, default=6)
    parser.add_argument('--output',   default='跨領域課程設計.docx')
    args = parser.parse_args()

    subjects = [s.strip() for s in args.subjects.split(',') if s.strip()]
    doc = new_doc_a4()
    add_header_footer(doc, f'跨領域課程｜{args.grade}｜{"/".join(subjects)}')
    cover_page(doc, '跨領域課程設計方案',
               args.question,
               {'核心問題': args.question[:22]+'…', '參與科目': '、'.join(subjects),
                '年級': args.grade, '週數': f'{args.weeks} 週',
                '建立日期': str(date.today()), '課程類型': '108課綱彈性學習課程'})

    add_overview_table(doc, args.question, subjects, args.grade, args.weeks)
    add_subject_contribution(doc, args.question, subjects)
    add_activity_sequence(doc, args.question, subjects, args.weeks)
    add_authentic_assessment(doc, args.question)
    add_implementation_notes(doc, subjects)
    doc.save(args.output)
    print(f'✓ 跨領域課程設計已儲存：{args.output}')

if __name__ == '__main__':
    main()
