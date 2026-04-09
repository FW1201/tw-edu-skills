#!/usr/bin/env python3
"""
抗 AI 評量矯正報告生成腳本
產出完整的 .docx 矯正報告
"""
import argparse, sys
from datetime import date
sys.path.insert(0, '.')
from tw_edu_doc_utils import *

# ── 色彩常數 ──────────────────────────────────────────────
RED_SOFT   = RGBColor(0xA9, 0x3A, 0x26)
ORANGE     = RGBColor(0xCA, 0x6F, 0x1E)
YELLOW_B   = RGBColor(0x9A, 0x7D, 0x0A)
GREEN      = RGBColor(0x1E, 0x84, 0x49)
RED_BG     = RGBColor(0xFD, 0xED, 0xEC)
ORANGE_BG  = RGBColor(0xFD, 0xEB, 0xD0)
YELLOW_BG  = RGBColor(0xFE, 0xF9, 0xE7)
GREEN_BG   = RGBColor(0xEA, 0xF9, 0xE4)

RISK_LABELS = {
    'P0': ('🔴 極高風險', RED_SOFT,   RED_BG),
    'P1': ('🟠 高風險',   ORANGE,     ORANGE_BG),
    'P2': ('🟡 中風險',   YELLOW_B,   YELLOW_BG),
    'P3': ('🟢 低風險',   GREEN,      GREEN_BG),
}

# ── 五維度評分計算 ──────────────────────────────────────
def calc_risk(item):
    score = (item.get('d1',0) + item.get('d2',0) +
             item.get('d3',0) + item.get('d4',0) + item.get('d5',0))
    if   score <= 5:  return 'P0', score
    elif score <= 10: return 'P1', score
    elif score <= 14: return 'P2', score
    elif score <= 18: return 'P3', score
    else:             return 'OK', score

# ── 範例評量資料 ──────────────────────────────────────────
SAMPLE_ITEMS = [
    {
        'id': 1, 'type': '作文', 'subject': '國語文',
        'original': '以「友誼」為題，寫一篇 300 字的記敘文，描述一次令你印象深刻的友誼故事。',
        'd1': 0, 'd2': 1, 'd3': 0, 'd4': 0, 'd5': 1,
        'ai_weakness': 'AI 可直接生成通用友誼故事；無需任何個人情境；標準記敘文格式 AI 熟練。',
        'strategies': ['個人化情境', '真實讀者', '過程文件化'],
        'corrected': (
            '想像你是班刊的主編，本期主題是「讓我一輩子忘不了的那個朋友」。\n'
            '請為班上同學寫一篇 250 字的人物特寫，要求：\n'
            '① 至少描述一個你親眼見到的具體場景（時間/地點/發生什麼事）\n'
            '② 說明這位朋友如何改變了你某個習慣或想法\n'
            '③ 結尾用一句你想說但一直沒說的話作結\n\n'
            '繳交時附上 50 字「本人聲明」：說明你寫的是真實的人和真實的場景。\n'
            '（AI 生成的內容無法附上真實個人聲明）'
        ),
        'score_before': 2, 'score_after': 15,
    },
    {
        'id': 2, 'type': '問答題', 'subject': '國語文',
        'original': '說明《背影》這篇文章的主題與作者想傳達的情感。',
        'd1': 1, 'd2': 0, 'd3': 0, 'd4': 0, 'd5': 1,
        'ai_weakness': 'AI 對《背影》有完整知識；標準主題分析格式 AI 熟練；無個人連結要求。',
        'strategies': ['本學期脈絡連結', '個人立場要求', '元認知'],
        'corrected': (
            '讀完《背影》後，在本學期我們讀過的所有文章中，選一篇你認為和《背影》\n'
            '「表達親情方式最不同」的作品，比較兩篇的寫法差異，並說明你偏好哪種，為什麼。\n'
            '（AI 無法知道你本學期讀了哪些文章；\n'
            '  要求個人偏好說明，AI 只能猜，無法確認你的真實立場）'
        ),
        'score_before': 2, 'score_after': 14,
    },
    {
        'id': 3, 'type': '選擇題', 'subject': '國語文',
        'original': '下列何者是比喻的修辭手法？\n(A)她的笑聲如鈴聲般悅耳\n(B)他跑得很快\n(C)風吹過來，好涼快\n(D)他買了一本書',
        'd1': 0, 'd2': 0, 'd3': 0, 'd4': 1, 'd5': 0,
        'ai_weakness': 'AI 正確率 100%；無情境限制；單一知識點記憶題。',
        'strategies': ['不完美設計', '本地情境'],
        'corrected': (
            '以下是班上一位同學寫的短文（已匿名處理）：\n'
            '「昨天打掃，[同學A]不小心把地圖摔到地上，整個教室都笑了。\n'
            ' 他說：『我的臉像西瓜一樣紅。』老師說他像個小偵探。」\n\n'
            '關於文中的修辭用法，下列說明何者「錯誤」？\n'
            '(A)「臉像西瓜」是比喻，以顏色相似做比較\n'
            '(B)「臉像西瓜」也暗示了尷尬的情緒\n'
            '(C)「像個小偵探」是比喻，把人比成職業\n'
            '(D)「整個教室都笑了」是夸張，全班人同時笑是不可能的\n\n'
            '（AI 無法取得班上同學的真實作品；需整合修辭知識和情境理解）'
        ),
        'score_before': 1, 'score_after': 10,
    },
    {
        'id': 4, 'type': '問答題', 'subject': '國語文',
        'original': '描述你今天早上上學路上觀察到的一個細節，並說明它讓你想到課文中的哪一個句子，以及為什麼。',
        'd1': 4, 'd2': 4, 'd3': 1, 'd4': 2, 'd5': 3,
        'ai_weakness': '無明顯弱點。AI 不知道學生今天早上看到什麼，也不知道課文的具體哪個句子有共鳴。',
        'strategies': [],
        'corrected': None,  # 不需要修改
        'score_before': 14, 'score_after': 14,
    },
]

# ── 主要生成函式 ──────────────────────────────────────────
def add_alignment_card(doc, purpose, grade, context, core_obj):
    section_heading(doc, '概念對齊確認')
    tbl = doc.add_table(rows=5, cols=2)
    tbl.style = 'Table Grid'
    tbl.columns[0].width = Cm(4)
    tbl.columns[1].width = Cm(13)
    rows_data = [
        ('📌 任務', '抗 AI 評量矯正分析'),
        ('🎯 評量目的', purpose),
        ('👤 目標對象', f'{grade}，作答情境：{context}'),
        ('🔒 核心目標', core_obj),
        ('⚠️ 分析原則', '保持學習目標，矯正 AI 可答性弱點；無法確認存在的文獻標示「查無」'),
    ]
    for i, (label, val) in enumerate(rows_data):
        header_cell(tbl.rows[i].cells[0], label, bg=BLUE_MID)
        data_cell(tbl.rows[i].cells[1], val, row_idx=i)
        tbl.rows[i].height = Cm(1.0)
    doc.add_paragraph()

def add_scan_overview(doc, items):
    section_heading(doc, '第一部分：AI 可答性全面掃描')
    tbl = doc.add_table(rows=len(items)+1, cols=7)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(1.2), Cm(1.5), Cm(4), Cm(1.5), Cm(1.5),
                            Cm(1.5), Cm(5)]):
        tbl.columns[j].width = w
    hdrs = ['#', '類型', '原題摘要', 'AI風險', '原分/20',
            '改後/20', '主要弱點']
    for j, h in enumerate(hdrs):
        header_cell(tbl.rows[0].cells[j], h)

    p0_cnt = p1_cnt = p2_cnt = p3_cnt = 0
    for i, item in enumerate(items, 1):
        risk, score = calc_risk(item)
        risk_label, risk_color, risk_bg = RISK_LABELS.get(
            risk, ('✅ 無需修改', GREEN, GREEN_BG))
        if risk == 'P0': p0_cnt += 1
        elif risk == 'P1': p1_cnt += 1
        elif risk == 'P2': p2_cnt += 1
        else: p3_cnt += 1

        row = tbl.rows[i]
        data_cell(row.cells[0], str(item['id']), row_idx=i, center=True)
        data_cell(row.cells[1], item.get('type',''), row_idx=i, center=True)
        data_cell(row.cells[2], item['original'][:40]+'…'
                  if len(item['original'])>40 else item['original'], row_idx=i)
        set_cell_bg(row.cells[3], risk_bg)
        set_cell_border(row.cells[3])
        cell_write(row.cells[3], risk_label.split(' ', 1)[-1],
                   bold=True, color=risk_color, center=True)
        data_cell(row.cells[4], str(item['score_before']), row_idx=i, center=True)
        after = item.get('score_after', item['score_before'])
        data_cell(row.cells[5], str(after), row_idx=i, center=True)
        weakness = item.get('ai_weakness', '')[:35]
        data_cell(row.cells[6], weakness, row_idx=i)
        tbl.rows[i].height = Cm(1.1)

    doc.add_paragraph()
    # 統計摘要
    p = doc.add_paragraph()
    r = p.add_run(
        f'掃描摘要：共 {len(items)} 題 ｜ '
        f'🔴 極高風險：{p0_cnt} 題 ｜ 🟠 高風險：{p1_cnt} 題 ｜ '
        f'🟡 中風險：{p2_cnt} 題 ｜ 🟢 低風險：{p3_cnt} 題'
    )
    r.bold = True; r.font.size = Pt(11); r.font.name = '標楷體'
    r.font.color.rgb = BLUE_DEEP; set_east_asia_font(r)
    doc.add_paragraph()

def add_correction_detail(doc, items):
    section_heading(doc, '第二部分：逐題矯正方案')
    for item in items:
        risk, score = calc_risk(item)
        risk_label, risk_color, risk_bg = RISK_LABELS.get(
            risk, ('✅ 低風險', GREEN, GREEN_BG))

        # 題目標題列
        p = doc.add_paragraph()
        r = p.add_run(f'題目 #{item["id"]}  ─  {item.get("type","")}  '
                      f'  {risk_label}  （{score}/20 分）')
        r.bold = True; r.font.size = Pt(12); r.font.name = '標楷體'
        r.font.color.rgb = risk_color; set_east_asia_font(r)
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)

        tbl = doc.add_table(rows=2, cols=1)
        tbl.style = 'Table Grid'
        tbl.columns[0].width = Cm(17)

        # 原題
        header_cell(tbl.rows[0].cells[0], '原題', bg=BLUE_DEEP)
        data_cell(tbl.rows[0].cells[1 if False else 0],
                  item['original'], row_idx=0)
        # 手動第二行
        tbl2 = doc.add_table(rows=3 if item.get('corrected') else 2, cols=1)
        tbl2.style = 'Table Grid'; tbl2.columns[0].width = Cm(17)

        header_cell(tbl2.rows[0].cells[0], '✗  AI 可答弱點分析', bg=risk_color)
        data_cell(tbl2.rows[0].cells[0],
                  item.get('ai_weakness', '無已知弱點'), row_idx=0)
        tbl2.rows[0].height = Cm(1.4)

        if item.get('corrected'):
            # 策略標籤
            strats = item.get('strategies', [])
            strat_text = '使用策略：' + '、'.join(strats) if strats else '見矯正後內容'
            header_cell(tbl2.rows[1].cells[0],
                        f'✓  矯正後版本  ｜  {strat_text}', bg=GREEN)
            data_cell(tbl2.rows[1].cells[0], item['corrected'], row_idx=1)
            tbl2.rows[1].height = Cm(3.5)

            # 分數對比
            before = item['score_before']; after = item.get('score_after', before)
            delta  = after - before
            header_cell(tbl2.rows[2].cells[0],
                        f'AI 可答性改變：{before}/20 → {after}/20  （+{delta} 分，'
                        f'降低 AI 作答優勢）', bg=BLUE_LIGHT)
        else:
            header_cell(tbl2.rows[1].cells[0],
                        f'✅ 此題 AI 可答性已低（{score}/20），建議保留原題不做修改',
                        bg=GREEN_BG)
            set_cell_bg(tbl2.rows[1].cells[0], GREEN_BG)
            cell_write(tbl2.rows[1].cells[0],
                       f'✅ 此題 AI 可答性已低（{score}/20），建議保留原題',
                       color=GREEN, bold=True, center=True)

        doc.add_paragraph()

def add_executive_plan(doc, items):
    section_heading(doc, '第三部分：執行建議')
    risks = [(item, calc_risk(item)[0]) for item in items]
    high_risk = [(it, r) for it, r in risks if r in ('P0', 'P1')]
    med_risk  = [(it, r) for it, r in risks if r == 'P2']
    low_risk  = [(it, r) for it, r in risks if r in ('P3', 'OK')]

    tbl = doc.add_table(rows=4, cols=2)
    tbl.style = 'Table Grid'
    tbl.columns[0].width = Cm(4); tbl.columns[1].width = Cm(13)
    plans = [
        ('🚀 立即可做\n（不改題目）',
         '1. 收作業時要求附上「過程反思卡」（草稿 + 改了什麼 + 為什麼）\n'
         '2. 抽選 2-3 位學生進行 3 分鐘口頭說明自己的答案\n'
         '3. 下次作業加入「請說明這個答案中哪一段是你自己最重要的想法」'),
        ('📝 短期改善\n（微調題目）',
         f'優先矯正 {len(high_risk)} 道高風險題目（見第二部分矯正方案）\n'
         '重點：為每道寫作題加入個人情境要求\n'
         '重點：至少一題要求引用本學期課堂共同經驗'),
        ('🔧 長期設計\n（架構調整）',
         '1. 導入「作品集」評量（多次累積，難以一次性 AI 代替）\n'
         '2. 每學期至少一次口頭報告或展示任務\n'
         '3. 考慮使用 RAFT 寫作框架設計作文題目\n'
         '4. 期末評量加入「學期成長反思」（連結多次作品，AI 難以整合）'),
    ]
    header_cell(tbl.rows[0].cells[0], '執行層次', bg=BLUE_DEEP)
    header_cell(tbl.rows[0].cells[1], '具體行動', bg=BLUE_DEEP)
    for i, (label, plan) in enumerate(plans, 1):
        colors = [BLUE_DEEP, BLUE_MID, RGBColor(0x5D,0x6D,0x7E)]
        header_cell(tbl.rows[i].cells[0], label, bg=colors[i-1])
        data_cell(tbl.rows[i].cells[1], plan, row_idx=i)
        tbl.rows[i].height = Cm(2.5)
    doc.add_paragraph()

def add_strategy_appendix(doc):
    section_heading(doc, '附錄：十大抗 AI 評量設計策略速查')
    strategies = [
        ('1. 個人化情境', '要求連結學生自己的真實經驗、班級事件、在地場景', '★★★★★'),
        ('2. 過程文件化', '不只評成品，評思考演進；要求草稿+修改紀錄+反思', '★★★★☆'),
        ('3. 本地脈絡', '使用只有本班/本校學生知道的資料', '★★★★★'),
        ('4. 即時性', '書面完成後加口頭說明；現場展示', '★★★★☆'),
        ('5. 元認知要求', '說明「你是如何得出結論的」；反思困難與解決', '★★★☆☆'),
        ('6. 真實讀者', '讓學生為真實對象寫作（同學/家長/社區）', '★★★★☆'),
        ('7. 整合式任務', '整合多個課程知識，AI 難以整合特定課程脈絡', '★★★☆☆'),
        ('8. 不完美設計', '提供有問題的範本，要求學生找出並改正', '★★★☆☆'),
        ('9. 選擇與說明', '讓學生選擇，並要求說明選擇理由', '★★★☆☆'),
        ('10. 多輪修改', '不接受一次提交；根據回饋修改並說明改了什麼', '★★★★☆'),
    ]
    tbl = doc.add_table(rows=len(strategies)+1, cols=3)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(4), Cm(9), Cm(4)]): tbl.columns[j].width = w
    for j, h in enumerate(['策略', '說明', '有效性']): header_cell(tbl.rows[0].cells[j], h)
    for i, (name, desc, eff) in enumerate(strategies, 1):
        data_cell(tbl.rows[i].cells[0], name, row_idx=i)
        data_cell(tbl.rows[i].cells[1], desc, row_idx=i)
        data_cell(tbl.rows[i].cells[2], eff, row_idx=i, center=True)
        tbl.rows[i].height = Cm(1.0)
    doc.add_paragraph()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--purpose',       default='總結性評量（期末成績）')
    parser.add_argument('--grade',         default='國中八年級')
    parser.add_argument('--context',       default='回家作業（開放環境）')
    parser.add_argument('--core_objective',default='閱讀理解與個人化表達')
    parser.add_argument('--assessment_text',default='')
    parser.add_argument('--output',        default='抗AI評量矯正報告.docx')
    args = parser.parse_args()

    doc = new_doc_a4()
    add_header_footer(doc, f'抗AI評量矯正報告 ｜ {args.grade} ｜ {args.purpose}')

    # 封面
    cover_page(doc, '抗 AI 評量矯正報告',
               f'{args.grade}｜{args.purpose}',
               {'年級': args.grade, '評量目的': args.purpose,
                '作答情境': args.context, '核心目標': args.core_objective,
                '分析日期': str(date.today()), '分析方法': '五維度 AI 可答性矩陣'})

    # 免責聲明
    p = doc.add_paragraph()
    r = p.add_run(
        '📌 分析說明：本報告使用「五維度 AI 可答性矩陣」評估每道題目，\n'
        '並在保持相同學習目標的前提下提供矯正建議。\n'
        '矯正目標不是阻止學生使用 AI，而是設計讓 AI 無法完全代替學生思考的評量。'
    )
    r.font.size = Pt(10.5); r.font.name = '標楷體'
    r.font.color.rgb = RGBColor(0x56, 0x65, 0x73)
    set_east_asia_font(r)
    doc.add_paragraph()

    add_alignment_card(doc, args.purpose, args.grade,
                       args.context, args.core_objective)
    add_scan_overview(doc, SAMPLE_ITEMS)
    add_correction_detail(doc, SAMPLE_ITEMS)
    add_executive_plan(doc, SAMPLE_ITEMS)
    add_strategy_appendix(doc)

    doc.save(args.output)
    print(f'✓ 抗 AI 評量矯正報告已儲存：{args.output}')

if __name__ == '__main__':
    main()
