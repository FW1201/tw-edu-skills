#!/usr/bin/env python3
"""教材轉精美教學簡報生成腳本"""
import argparse, sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from pptx import Presentation
from pptx.util import Cm, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# 年級字體規格
GRADE_SPECS = {
    'elementary_low': {'title_size': 40, 'body_size': 28, 'max_bullets': 3, 'img_ratio': 0.7},
    'elementary_high':{'title_size': 36, 'body_size': 24, 'max_bullets': 4, 'img_ratio': 0.55},
    'junior':         {'title_size': 32, 'body_size': 22, 'max_bullets': 5, 'img_ratio': 0.4},
    'senior':         {'title_size': 28, 'body_size': 20, 'max_bullets': 6, 'img_ratio': 0.3},
}

# 風格色盤
STYLES = {
    'modern': {'bg': RGBColor(0xFF,0xFF,0xFF), 'primary': RGBColor(0x1A,0x52,0x76),
               'accent': RGBColor(0xD4,0xAC,0x0D), 'text': RGBColor(0x1C,0x2A,0x35)},
    'colorful':{'bg': RGBColor(0xFF,0xFF,0xFF), 'primary': RGBColor(0x21,0x84,0xC7),
               'accent': RGBColor(0xE8,0x74,0x22), 'text': RGBColor(0x2C,0x3E,0x50)},
    'dark':    {'bg': RGBColor(0x1A,0x1A,0x2E), 'primary': RGBColor(0x16,0x21,0x3E),
               'accent': RGBColor(0xE9,0x4C,0x60), 'text': RGBColor(0xEE,0xEE,0xEE)},
    'local':   {'bg': RGBColor(0xFF,0xFF,0xF5), 'primary': RGBColor(0x5C,0x39,0x17),
               'accent': RGBColor(0xC0,0x39,0x2B), 'text': RGBColor(0x2C,0x1A,0x10)},
}

def get_stage(grade_str):
    g = grade_str.replace(' ', '')
    if any(x in g for x in ['一年','二年','低年級']): return 'elementary_low'
    if any(x in g for x in ['三年','四年','五年','六年','中年級','高年級','國小']): return 'elementary_high'
    if any(x in g for x in ['國中','七','八','九']): return 'junior'
    return 'senior'

def sf(tf, text, size, bold=False, color=None, align=PP_ALIGN.LEFT):
    if color is None: color = RGBColor(0x1C,0x2A,0x35)
    tf.text = ''
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold
    r.font.color.rgb = color; r.font.name = '微軟正黑體'

def add_topbar(slide, prs, color, height_cm=1.8):
    bar = slide.shapes.add_shape(1, 0, 0, prs.slide_width, Cm(height_cm))
    bar.fill.solid(); bar.fill.fore_color.rgb = color; bar.line.fill.background()

def add_title_slide(prs, title, subject, grade, style_name='modern'):
    c = STYLES[style_name]
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = c['bg']; bg.line.fill.background()
    # 上方色帶
    add_topbar(slide, prs, c['primary'], 2.5)
    # 底部色帶
    bot = slide.shapes.add_shape(1, 0, Cm(16.5), prs.slide_width, Cm(2.5))
    bot.fill.solid(); bot.fill.fore_color.rgb = c['primary']; bot.line.fill.background()
    # 金色裝飾線
    for y_cm in [2.5, 2.7]:
        line = slide.shapes.add_shape(1, 0, Cm(y_cm), prs.slide_width, Cm(0.08))
        line.fill.solid(); line.fill.fore_color.rgb = c['accent']; line.line.fill.background()

    txb = slide.shapes.add_textbox(Cm(1.5), Cm(4), Cm(22), Cm(4))
    sf(txb.text_frame, title, 38, bold=True, color=c['primary'], align=PP_ALIGN.CENTER)
    txb2 = slide.shapes.add_textbox(Cm(1.5), Cm(8.5), Cm(22), Cm(2))
    sf(txb2.text_frame, f'{subject}｜{grade}', 20, color=c['text'], align=PP_ALIGN.CENTER)
    txb3 = slide.shapes.add_textbox(Cm(1.5), Cm(17.0), Cm(22), Cm(1.2))
    sf(txb3.text_frame, '108 課綱素養導向教學', 14, color=RGBColor(0xFF,0xFF,0xFF), align=PP_ALIGN.CENTER)

def add_objectives_slide(prs, objectives, stage, style_name='modern'):
    c = STYLES[style_name]; spec = GRADE_SPECS[stage]
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = c['bg']; bg.line.fill.background()
    add_topbar(slide, prs, c['primary'])
    txb_t = slide.shapes.add_textbox(Cm(0.8), Cm(0.3), Cm(23), Cm(1.2))
    sf(txb_t.text_frame, '🎯 本節學習目標', spec['title_size']-8, bold=True,
       color=RGBColor(0xFF,0xFF,0xFF), align=PP_ALIGN.LEFT)

    txb_c = slide.shapes.add_textbox(Cm(1.5), Cm(2.5), Cm(22), Cm(12))
    txb_c.text_frame.word_wrap = True
    for i, obj in enumerate(objectives[:spec['max_bullets']]):
        p = txb_c.text_frame.paragraphs[0] if i==0 else txb_c.text_frame.add_paragraph()
        p.space_before = Pt(10)
        r = p.add_run()
        r.text = f'  ➤  {obj}'
        r.font.size = Pt(spec['body_size']); r.font.name = '微軟正黑體'
        r.font.color.rgb = c['text']

def add_content_slide(prs, title, bullets, note='', stage='junior', style_name='modern'):
    c = STYLES[style_name]; spec = GRADE_SPECS[stage]
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = c['bg']; bg.line.fill.background()
    add_topbar(slide, prs, c['primary'])
    txb_t = slide.shapes.add_textbox(Cm(0.8), Cm(0.3), Cm(23), Cm(1.2))
    sf(txb_t.text_frame, title, spec['title_size']-8, bold=True,
       color=RGBColor(0xFF,0xFF,0xFF), align=PP_ALIGN.LEFT)

    txb_c = slide.shapes.add_textbox(Cm(1.5), Cm(2.4), Cm(22.6), Cm(11))
    txb_c.text_frame.word_wrap = True
    for i, bullet in enumerate(bullets[:spec['max_bullets']]):
        p = txb_c.text_frame.paragraphs[0] if i==0 else txb_c.text_frame.add_paragraph()
        p.space_before = Pt(8)
        r = p.add_run(); r.text = f'▸  {bullet}'
        r.font.size = Pt(spec['body_size']); r.font.name = '微軟正黑體'; r.font.color.rgb = c['text']

    if note:
        note_box = slide.shapes.add_shape(1, Cm(1.2), Cm(14.2), Cm(22.6), Cm(1.0))
        note_box.fill.solid(); note_box.fill.fore_color.rgb = RGBColor(0xF0,0xF4,0xF8)
        note_box.line.color.rgb = c['primary']
        txb_n = slide.shapes.add_textbox(Cm(1.5), Cm(14.3), Cm(22), Cm(0.8))
        sf(txb_n.text_frame, f'💡 {note}', spec['body_size']-4, color=c['primary'])

def add_discussion_slide(prs, question, thinking_time='2', stage='junior', style_name='modern'):
    c = STYLES[style_name]; spec = GRADE_SPECS[stage]
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = c['bg']; bg.line.fill.background()
    add_topbar(slide, prs, RGBColor(0x1E,0x84,0x49))
    txb_t = slide.shapes.add_textbox(Cm(0.8), Cm(0.3), Cm(18), Cm(1.2))
    sf(txb_t.text_frame, '💬 思考時間', spec['title_size']-8, bold=True,
       color=RGBColor(0xFF,0xFF,0xFF))
    # 計時標籤
    timer = slide.shapes.add_shape(1, Cm(20), Cm(0.2), Cm(4.5), Cm(1.2))
    timer.fill.solid(); timer.fill.fore_color.rgb = c['accent']; timer.line.fill.background()
    txb_timer = slide.shapes.add_textbox(Cm(20.2), Cm(0.4), Cm(4.1), Cm(0.8))
    sf(txb_timer.text_frame, f'⏱ {thinking_time} 分鐘', 14, bold=True,
       color=c['primary'], align=PP_ALIGN.CENTER)

    txb_q = slide.shapes.add_textbox(Cm(2), Cm(4), Cm(21), Cm(6))
    txb_q.text_frame.word_wrap = True
    sf(txb_q.text_frame, question, spec['title_size']-2, bold=True,
       color=c['text'], align=PP_ALIGN.CENTER)

def add_summary_slide(prs, title, key_points, stage='junior', style_name='modern'):
    c = STYLES[style_name]; spec = GRADE_SPECS[stage]
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = c['bg']; bg.line.fill.background()
    add_topbar(slide, prs, RGBColor(0xD4,0xAC,0x0D))
    txb_t = slide.shapes.add_textbox(Cm(0.8), Cm(0.3), Cm(23), Cm(1.2))
    sf(txb_t.text_frame, f'📝 {title} — 重點整理', spec['title_size']-8, bold=True,
       color=RGBColor(0x1C,0x2A,0x35), align=PP_ALIGN.LEFT)

    # 重點色塊
    colors = [RGBColor(0xEB,0xF5,0xFB), RGBColor(0xEA,0xF3,0xDE),
              RGBColor(0xFA,0xEE,0xDA), RGBColor(0xFB,0xEA,0xF0)]
    for i, (key, val) in enumerate(key_points[:4]):
        col = i % 2; row = i // 2
        x = Cm(1.2 + col * 11.9); y = Cm(2.5 + row * 5.5)
        box = slide.shapes.add_shape(1, x, y, Cm(11.5), Cm(5))
        box.fill.solid(); box.fill.fore_color.rgb = colors[i]
        box.line.color.rgb = c['primary']
        txb_k = slide.shapes.add_textbox(x+Cm(0.3), y+Cm(0.3), Cm(10.9), Cm(1.2))
        sf(txb_k.text_frame, key, spec['body_size']-2, bold=True, color=c['primary'])
        txb_v = slide.shapes.add_textbox(x+Cm(0.3), y+Cm(1.6), Cm(10.9), Cm(3))
        txb_v.text_frame.word_wrap = True
        sf(txb_v.text_frame, val, spec['body_size']-4, color=c['text'])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--title',        default='課文標題')
    parser.add_argument('--subject',      default='國語文')
    parser.add_argument('--grade',        default='國中八年級')
    parser.add_argument('--stage',        default='junior',
                        choices=['elementary_low','elementary_high','junior','senior'])
    parser.add_argument('--style',        default='modern',
                        choices=['modern','colorful','dark','local'])
    parser.add_argument('--content_file', default='')
    parser.add_argument('--slides_count', type=int, default=12)
    parser.add_argument('--output',       default='教學簡報.pptx')
    args = parser.parse_args()

    # 從 content_file 讀取內容（若有）
    content_data = {}
    if args.content_file and Path(args.content_file).exists():
        try:
            content_data = json.loads(Path(args.content_file).read_text(encoding='utf-8'))
        except Exception:
            pass

    stage = args.stage or get_stage(args.grade)
    prs = Presentation()
    prs.slide_width = Cm(25.4); prs.slide_height = Cm(19.05)

    # 封面
    add_title_slide(prs, args.title, args.subject, args.grade, args.style)

    # 學習目標
    objectives = content_data.get('objectives', [
        f'能理解《{args.title}》的主要內容與結構',
        f'能分析並解釋文章的重要概念',
        f'能運用所學內容進行討論或創作',
    ])
    add_objectives_slide(prs, objectives, stage, args.style)

    # 主要內容投影片（由 content_data 驅動或使用預設）
    slides_data = content_data.get('slides', [
        {'title': '背景知識', 'bullets': ['相關概念一', '相關概念二', '相關概念三'],
         'note': '可請學生分享先備知識'},
        {'title': '核心概念一', 'bullets': ['說明A', '說明B', '補充說明C'],
         'note': '使用板書或概念圖輔助'},
        {'title': '核心概念二', 'bullets': ['說明A', '說明B'],
         'note': ''},
        {'title': '深度分析', 'bullets': ['分析面向一', '分析面向二', '延伸思考'],
         'note': '引導學生用自己的語言解釋'},
    ])
    for slide_data in slides_data:
        add_content_slide(prs, slide_data['title'], slide_data['bullets'],
                         slide_data.get('note',''), stage, args.style)

    # 討論投影片
    discussion_q = content_data.get('discussion_question',
        f'學了《{args.title}》之後，你有什麼新的發現或想法？')
    add_discussion_slide(prs, discussion_q, stage=stage, style_name=args.style)

    # 重點整理
    summary_points = content_data.get('summary', [
        ('核心主題', f'《{args.title}》的中心思想'),
        ('重要概念', '本課的 3 個關鍵詞'),
        ('學習技能', '閱讀理解 + 批判思考'),
        ('延伸思考', '課後可繼續探索的問題'),
    ])
    add_summary_slide(prs, args.title, summary_points[:4], stage, args.style)

    # 結尾
    c = STYLES[args.style]
    end_slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = end_slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = c['primary']; bg.line.fill.background()
    txb_end = end_slide.shapes.add_textbox(Cm(1.5), Cm(6), Cm(22), Cm(3))
    sf(txb_end.text_frame, '課後任務', 30, bold=True,
       color=RGBColor(0xFF,0xFF,0xFF), align=PP_ALIGN.CENTER)
    txb_end2 = end_slide.shapes.add_textbox(Cm(1.5), Cm(9.5), Cm(22), Cm(2))
    task = content_data.get('homework', f'請完成《{args.title}》相關學習單，下節課帶來討論。')
    sf(txb_end2.text_frame, task, 18, color=RGBColor(0xEB,0xF5,0xFB), align=PP_ALIGN.CENTER)

    prs.save(args.output)
    print(f'✓ 教學簡報已儲存：{args.output}（{len(prs.slides)} 張投影片）')

if __name__ == '__main__':
    main()
