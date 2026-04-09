#!/usr/bin/env python3
"""學生回饋評語生成腳本"""
import argparse, sys
sys.path.insert(0, '.')
from tw_edu_doc_utils import *

LEVEL_COLORS = {'優': GREEN, '良': BLUE_MID, '可': GOLD, '需加強': ORANGE}

SAMPLE_STUDENTS = [
    {'name':'學生甲','levels':{'內容':' 優','結構':'良','語言':'優','整體':'優'},
     'strengths':'文章結構清晰，論點具體有力，舉例生動貼切',
     'improvements':'建議在文章結尾加強結論的力道，讓讀者印象更深刻',
     'encouragement':'整體表現相當優秀，繼續保持這份用心'},
    {'name':'學生乙','levels':{'內容':'良','結構':'可','語言':'良','整體':'良'},
     'strengths':'內容有個人想法，語句通順',
     'improvements':'段落組織可以更清楚，建議先用段落主題句帶領讀者',
     'encouragement':'你的思考很有深度，多練習段落寫法就會更好'},
    {'name':'學生丙','levels':{'內容':'可','結構':'可','語言':'可','整體':'可'},
     'strengths':'有嘗試使用課文中學到的詞彙',
     'improvements':'建議先用大綱規劃文章，再動筆寫正稿',
     'encouragement':'每一次練習都是進步，老師看到你的努力'},
]

def add_feedback_table(doc, subject, grade, task, students):
    section_heading(doc, f'【{task}】學生回饋評語總表')
    p = doc.add_paragraph()
    r = p.add_run(f'{subject}｜{grade}｜共 {len(students)} 位學生')
    r.font.size = Pt(11); r.font.name = '標楷體'; r.font.color.rgb = DARK_TEXT
    set_east_asia_font(r)
    doc.add_paragraph()

    for stu in students:
        # 學生標題列
        tbl = doc.add_table(rows=5, cols=3)
        tbl.style = 'Table Grid'
        for j, w in enumerate([Cm(3), Cm(7), Cm(7)]):
            tbl.columns[j].width = w

        # 標題
        merged = tbl.rows[0].cells[0].merge(tbl.rows[0].cells[2])
        header_cell(merged, f'學生：{stu["name"]}　｜　{task}　評量回饋', bg=BLUE_DEEP)
        tbl.rows[0].height = Cm(0.9)

        # 評量等第
        levels = stu.get('levels', {})
        level_text = '　'.join([f'{k}：{v}' for k,v in levels.items()])
        merged2 = tbl.rows[1].cells[0].merge(tbl.rows[1].cells[2])
        data_cell(merged2, f'▶ 各向度等第　{level_text}', row_idx=1)
        tbl.rows[1].height = Cm(0.8)

        # 三明治回饋
        feedback_rows = [
            ('✅ 優點\n（做得好的地方）', stu.get('strengths',''), GREEN),
            ('💡 建議\n（可以改進的方向）', stu.get('improvements',''), GOLD),
            ('🌟 鼓勵\n（期待與展望）', stu.get('encouragement',''), BLUE_MID),
        ]
        for i, (label, content, color) in enumerate(feedback_rows, 2):
            header_cell(tbl.rows[i].cells[0], label, bg=color)
            merged_c = tbl.rows[i].cells[1].merge(tbl.rows[i].cells[2])
            data_cell(merged_c, content, row_idx=i)
            tbl.rows[i].height = Cm(1.6)

        doc.add_paragraph()

def add_class_summary(doc, students):
    section_heading(doc, '班級整體表現分析', level=2)
    tbl = doc.add_table(rows=5, cols=3)
    tbl.style = 'Table Grid'
    for j, w in enumerate([Cm(4), Cm(7), Cm(6)]):
        tbl.columns[j].width = w
    header_cell(tbl.rows[0].cells[0], '分析面向')
    header_cell(tbl.rows[0].cells[1], '整體觀察')
    header_cell(tbl.rows[0].cells[2], '教學調整建議')
    observations = [
        ('優秀表現', '多數學生能掌握基本寫作結構', '可提供進階延伸挑戰'),
        ('待加強面向', '部分學生段落組織仍需練習', '下節課安排段落仿寫練習'),
        ('個別差異', '學生程度落差約2個層次', '設計差異化任務供選擇'),
        ('整體建議', '建議下次考前加強段落主題句教學', '提供範例對照練習'),
    ]
    for i, (aspect, obs, suggest) in enumerate(observations, 1):
        data_cell(tbl.rows[i].cells[0], aspect, row_idx=i, center=True)
        data_cell(tbl.rows[i].cells[1], obs, row_idx=i)
        data_cell(tbl.rows[i].cells[2], suggest, row_idx=i)
    doc.add_paragraph()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task',     default='議論文寫作')
    parser.add_argument('--subject',  default='國語文')
    parser.add_argument('--grade',    default='高中一年級')
    parser.add_argument('--students', default='')
    parser.add_argument('--output',   default='學生評語.docx')
    args = parser.parse_args()

    doc = new_doc_a4()
    add_header_footer(doc, f'學生回饋評語｜{args.task}｜{args.grade}')
    cover_page(doc, '學生作業回饋評語',
               f'{args.task}｜{args.subject}｜{args.grade}',
               {'科目': args.subject, '年級': args.grade,
                '任務名稱': args.task, '學生人數': f'{len(SAMPLE_STUDENTS)} 人',
                '批改日期': str(date.today()), '評量方式': '三明治回饋法'})
    add_feedback_table(doc, args.subject, args.grade, args.task, SAMPLE_STUDENTS)
    add_class_summary(doc, SAMPLE_STUDENTS)
    doc.save(args.output)
    print(f'✓ 學生評語已儲存：{args.output}')

if __name__ == '__main__':
    main()
