#!/usr/bin/env python3
"""學習歷程檔案輔助生成腳本"""
import argparse, sys
sys.path.insert(0, '.')
from tw_edu_doc_utils import *

def add_portfolio_framework(doc, grade, port_type):
    if port_type == 'course_result':
        section_heading(doc, '課程學習成果說明框架')
        p = doc.add_paragraph()
        r = p.add_run('⚠️ 本框架僅供參考，請學生以自己的語言真實呈現學習歷程')
        r.font.size = Pt(10); r.font.color.rgb = RED_SOFT; r.font.name = '標楷體'
        set_east_asia_font(r)
        doc.add_paragraph()

        sections = [
            ('一、課程簡介（約100字）',
             '說明這門課的學習內容與目標。\n'
             '範例：「在___課中，我學習了___，透過___活動，深入了解___。」\n'
             '請在此撰寫：\n' + '＿'*80),
            ('二、學習過程描述（約200字）',
             '具體描述你在這門課做了什麼、遇到什麼挑戰、如何克服。\n'
             '請在此撰寫：\n' + '＿'*80),
            ('三、學習成果說明（約200字）',
             '說明你的具體產出（作品、報告、實驗等）及其學習意義。\n'
             '可以附上作品截圖或重點摘錄。\n'
             '請在此撰寫：\n' + '＿'*80),
            ('四、能力成長與反思（約200字）',
             '反思這門課對你的影響：學到了什麼能力？對未來有何幫助？\n'
             '請在此撰寫：\n' + '＿'*80),
            ('五、與申請科系的連結（約100字）',
             '說明這門課與你未來志向的關聯（非必要，依情況而定）。\n'
             '請在此撰寫：\n' + '＿'*80),
        ]
        for title, desc in sections:
            section_heading(doc, title, level=2)
            tbl = doc.add_table(rows=1, cols=1)
            tbl.style = 'Table Grid'
            tbl.columns[0].width = Cm(17)
            data_cell(tbl.rows[0].cells[0], desc)
            tbl.rows[0].height = Cm(4)
            doc.add_paragraph()

    elif port_type == 'autobiography':
        section_heading(doc, '自傳撰寫框架')
        p = doc.add_paragraph()
        r = p.add_run('自傳字數建議：800-1200字｜語氣：第一人稱，真誠自然')
        r.font.size = Pt(10); r.font.color.rgb = GOLD; r.font.name = '標楷體'
        set_east_asia_font(r)
        doc.add_paragraph()

        structure = [
            ('段落一：我是誰（開場）', '用一個故事或場景引出你是誰。避免從「我叫XXX，就讀OOO」開始。'),
            ('段落二：形塑我的經歷', '哪些重要經歷（家庭/事件/人物）影響了你現在的價值觀？'),
            ('段落三：高中的學習與探索', '你在高中最投入的是什麼？有哪些具體的學習成果或經歷？'),
            ('段落四：我的特質與優勢', '你認為自己最突出的特質是什麼？用具體例子說明。'),
            ('段落五：未來的方向與期待', '你為什麼選擇這個科系？你希望在大學做什麼？'),
        ]
        for title, guide in structure:
            section_heading(doc, title, level=2)
            p2 = doc.add_paragraph()
            r2 = p2.add_run(f'引導提示：{guide}')
            r2.font.size = Pt(10); r2.font.color.rgb = BLUE_MID; r2.font.name = '標楷體'
            set_east_asia_font(r2)
            for _ in range(4):
                lp = doc.add_paragraph()
                pPr = lp._p.get_or_add_pPr()
                pBdr = OxmlElement('w:pBdr')
                bot = OxmlElement('w:bottom')
                bot.set(qn('w:val'), 'single'); bot.set(qn('w:sz'), '4')
                bot.set(qn('w:color'), 'BBBBBB')
                pBdr.append(bot); pPr.append(pBdr)
            doc.add_paragraph()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--grade',      default='高二')
    parser.add_argument('--type',       default='course_result',
                        choices=['course_result','diverse','autobiography'])
    parser.add_argument('--content',    default='')
    parser.add_argument('--target_dept',default='')
    parser.add_argument('--output',     default='學習歷程.docx')
    args = parser.parse_args()

    type_labels = {'course_result':'課程學習成果','diverse':'多元表現','autobiography':'自傳'}
    doc = new_doc_a4()
    add_header_footer(doc, f'學習歷程檔案輔助｜{type_labels.get(args.type,"")}｜{args.grade}')
    cover_page(doc, '學習歷程檔案輔助框架',
               f'{type_labels.get(args.type,"")}｜{args.grade}',
               {'年級': args.grade, '文件類型': type_labels.get(args.type,''),
                '目標科系': args.target_dept or '（未指定）', '建立日期': str(date.today())})

    p = doc.add_paragraph()
    r = p.add_run('📌 重要提醒：本文件為引導框架，所有內容必須由學生本人以真實經歷填寫。\n'
                  '禁止直接複製 AI 生成內容作為學習歷程檔案上傳，請誠實呈現個人學習歷程。')
    r.font.size = Pt(11); r.bold = True; r.font.name = '標楷體'
    r.font.color.rgb = RED_SOFT; set_east_asia_font(r)
    doc.add_paragraph()

    add_portfolio_framework(doc, args.grade, args.type)
    doc.save(args.output)
    print(f'✓ 學習歷程框架已儲存：{args.output}')

if __name__ == '__main__':
    main()
