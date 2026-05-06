#!/usr/bin/env python3
"""教材轉精美教學簡報生成腳本 V3.0
基於官方 context-to-pptx render_pptx.py（純 Python stdlib，無外部依賴）
11 種版型 × 9 種教育色盤 × 4 種年級字體規格 × 16:9 寬螢幕
"""
import argparse, json, sys, html
from zipfile import ZIP_DEFLATED, ZipFile
from pathlib import Path
from io import BytesIO

# ══════════════════════════════════════════════════════════════
# 投影片尺寸（EMU）
# ══════════════════════════════════════════════════════════════
SLIDE_W = 9144000   # 16 英寸 × 914400 EMU/英寸
SLIDE_H = 5143500   # 9 英寸

# ══════════════════════════════════════════════════════════════
# 9 種教育色盤
# ══════════════════════════════════════════════════════════════
EDU_THEMES: dict[str, dict[str, str]] = {
    "edu-warm":  {"bg":"FFFBF5","primary":"D97757","secondary":"6A9BCC","accent":"788C5D",
                  "gold":"E8A820","text":"141413","muted":"6B6B6B","white":"FFFFFF",
                  "soft":"F5EEE4","card":"FFFFFF","line":"DDD5C6"},
    "modern":    {"bg":"FFFFFF","primary":"1A5276","secondary":"2E86C1","accent":"D4AC0D",
                  "gold":"D4AC0D","text":"1C2A35","muted":"5B6677","white":"FFFFFF",
                  "soft":"D6EAF8","card":"FFFFFF","line":"D6EAF8"},
    "colorful":  {"bg":"FFFFFF","primary":"2184C7","secondary":"1565C0","accent":"E87422",
                  "gold":"E8A820","text":"2C3E50","muted":"5B6677","white":"FFFFFF",
                  "soft":"D6EEF8","card":"FFFFFF","line":"D6EEF8"},
    "dark":      {"bg":"1A1A2E","primary":"4A90D9","secondary":"7B2FFF","accent":"E94C60",
                  "gold":"FFD700","text":"EEEEEE","muted":"AAAAAA","white":"FFFFFF",
                  "soft":"2D2D4A","card":"1E1E3A","line":"3A3A5A"},
    "local":     {"bg":"FFFFF5","primary":"5C3917","secondary":"A04000","accent":"C0392B",
                  "gold":"C68D00","text":"2C1A10","muted":"7D6E5A","white":"FFFFFF",
                  "soft":"F5EAD5","card":"FFFFFF","line":"E8D5B0"},
    "nature":    {"bg":"FFFFFF","primary":"2E7D32","secondary":"388E3C","accent":"8BC34A",
                  "gold":"9E9D24","text":"1B3A1C","muted":"5D7A5E","white":"FFFFFF",
                  "soft":"F1F8E9","card":"FFFFFF","line":"C8E6C9"},
    "tech":      {"bg":"0D1117","primary":"1565C0","secondary":"00BCD4","accent":"7B2FFF",
                  "gold":"FFD700","text":"E0F2F1","muted":"AAAAAA","white":"FFFFFF",
                  "soft":"1A273A","card":"161B22","line":"30363D"},
    "warm":      {"bg":"FFFFFF","primary":"BF360C","secondary":"D84315","accent":"FF9800",
                  "gold":"FF9800","text":"3E1C00","muted":"8D5524","white":"FFFFFF",
                  "soft":"FFF8E1","card":"FFFFFF","line":"FFCCBC"},
    "purple":    {"bg":"FFFFFF","primary":"4A148C","secondary":"6A1B9A","accent":"CE93D8",
                  "gold":"FFD54F","text":"1A003C","muted":"7B6B8E","white":"FFFFFF",
                  "soft":"F3E5F5","card":"FFFFFF","line":"E1BEE7"},
}

# ══════════════════════════════════════════════════════════════
# 年級字體規格（EMU: 1pt = 12700 hundredths-of-pt，但 pptx sz 用百分之一點）
# pptx <a:sz> = 點數 × 100，例如 28pt = 2800
# ══════════════════════════════════════════════════════════════
GRADE_FONT_SCALE: dict[str, dict[str, int]] = {
    "elementary_low":  {"title": 3600, "body": 2800, "small": 2000, "max_bullets": 3},
    "elementary_high": {"title": 3200, "body": 2400, "small": 1800, "max_bullets": 4},
    "junior":          {"title": 2900, "body": 2200, "small": 1600, "max_bullets": 5},
    "senior":          {"title": 2600, "body": 2000, "small": 1400, "max_bullets": 6},
}

# ══════════════════════════════════════════════════════════════
# 工具函式
# ══════════════════════════════════════════════════════════════
def emu(pt: float) -> int:
    """點數轉 EMU（914400 / 72 = 12700 EMU per pt）"""
    return int(pt * 12700)

def pct(val: float) -> int:
    """百分比轉 EMU pctage（1% = 1000）"""
    return int(val * 1000)

def clr(hex6: str) -> str:
    return hex6.upper()

def x(tag: str, content: str = "", **attrs) -> str:
    attr_str = "".join(f' {k.replace("_", ":")}="{v}"' for k, v in attrs.items())
    if content:
        return f"<{tag}{attr_str}>{content}</{tag}>"
    return f"<{tag}{attr_str}/>"

def run(text: str, sz: int, bold: bool = False, color: str = "000000",
        lang: str = "zh-TW") -> str:
    b = "<a:b/>" if bold else ""
    return (
        f'<a:r><a:rPr lang="{lang}" sz="{sz}" dirty="0">'
        f'<a:solidFill><a:srgbClr val="{clr(color)}"/></a:solidFill>'
        f'{b}</a:rPr>'
        f'<a:t>{html.escape(text)}</a:t></a:r>'
    )

def para(runs_xml: str, align: str = "l", spc_bef: int = 0,
         line_spc: int = 17000) -> str:
    """段落，line_spc 單位為 hundredths-of-a-percent（170% = 17000）"""
    return (
        f'<a:p><a:pPr algn="{align}" indent="0">'
        f'<a:spcBef><a:spcPts val="{spc_bef}"/></a:spcBef>'
        f'<a:lnSpc><a:spcPct val="{line_spc}"/></a:lnSpc>'
        f'</a:pPr>{runs_xml}</a:p>'
    )

def text_body(x_emu: int, y_emu: int, w_emu: int, h_emu: int,
              paragraphs: str, margin: int = 91440) -> str:
    return (
        f'<p:sp><p:nvSpPr>'
        f'<p:cNvPr id="0" name=""/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
        f'<p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm>'
        f'<a:off x="{x_emu}" y="{y_emu}"/><a:ext cx="{w_emu}" cy="{h_emu}"/>'
        f'</a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:noFill/></p:spPr>'
        f'<p:txBody><a:bodyPr wrap="square" lIns="{margin}" rIns="{margin}" '
        f'tIns="{margin}" bIns="{margin}" anchor="ctr"/>'
        f'<a:lstStyle/>{paragraphs}</p:txBody></p:sp>'
    )

def rect(x_emu: int, y_emu: int, w_emu: int, h_emu: int,
         fill: str, alpha: int = 100000) -> str:
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="0" name=""/>'
        f'<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm>'
        f'<a:off x="{x_emu}" y="{y_emu}"/><a:ext cx="{w_emu}" cy="{h_emu}"/>'
        f'</a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:solidFill><a:srgbClr val="{clr(fill)}">'
        f'<a:alpha val="{alpha}"/>'
        f'</a:srgbClr></a:solidFill>'
        f'<a:ln w="0"><a:noFill/></a:ln>'
        f'</p:spPr><p:txBody><a:bodyPr/><a:lstStyle/></p:txBody></p:sp>'
    )

def line_sep(y_emu: int, color: str, w_emu: int = None) -> str:
    w = w_emu or SLIDE_W
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="0" name=""/>'
        f'<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm>'
        f'<a:off x="0" y="{y_emu}"/><a:ext cx="{w}" cy="12700"/>'
        f'</a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:solidFill><a:srgbClr val="{clr(color)}"/></a:solidFill>'
        f'</p:spPr><p:txBody><a:bodyPr/><a:lstStyle/></p:txBody></p:sp>'
    )

def wrap_slide(shapes: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
        ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<p:cSld><p:spTree>'
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
        '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        f'{shapes}'
        '</p:spTree></p:cSld>'
        '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'
    )

# ══════════════════════════════════════════════════════════════
# 版型渲染器
# ══════════════════════════════════════════════════════════════
def render_cover(slide: dict, theme: dict, grade: dict) -> str:
    title = slide.get("title", "")
    subtitle = slide.get("subtitle", "")
    meta = slide.get("meta", "")
    shapes = ""
    # 背景漸層色塊：底部 primary 橫帶
    shapes += rect(0, 0, SLIDE_W, SLIDE_H, theme["bg"])
    shapes += rect(0, int(SLIDE_H * 0.62), SLIDE_W, int(SLIDE_H * 0.38), theme["primary"])
    shapes += rect(0, int(SLIDE_H * 0.60), SLIDE_W, int(SLIDE_H * 0.04), theme["accent"])
    # 主標題
    t_size = grade["title"]
    shapes += text_body(
        emu(2), emu(1.2), SLIDE_W - emu(4), int(SLIDE_H * 0.55),
        para(run(title, t_size + 200, bold=True, color=theme["text"]), align="l", line_spc=14000),
        margin=0,
    )
    # 副標題
    if subtitle:
        shapes += text_body(
            emu(2), int(SLIDE_H * 0.64), SLIDE_W - emu(4), int(SLIDE_H * 0.18),
            para(run(subtitle, grade["body"], color=theme["white"]), align="l"),
            margin=0,
        )
    if meta:
        shapes += text_body(
            emu(2), int(SLIDE_H * 0.82), SLIDE_W - emu(4), int(SLIDE_H * 0.12),
            para(run(meta, grade["small"], color=theme["white"]), align="l"),
            margin=0,
        )
    return wrap_slide(shapes)


def render_section(slide: dict, theme: dict, grade: dict) -> str:
    title = slide.get("title", "")
    subtitle = slide.get("subtitle", "")
    shapes = ""
    shapes += rect(0, 0, SLIDE_W, SLIDE_H, theme["primary"])
    shapes += rect(0, int(SLIDE_H * 0.7), SLIDE_W, int(SLIDE_H * 0.04), theme["accent"])
    shapes += text_body(
        emu(2.5), int(SLIDE_H * 0.28), SLIDE_W - emu(5), int(SLIDE_H * 0.40),
        para(run(title, grade["title"] + 400, bold=True, color=theme["white"]), align="ctr", line_spc=12000),
        margin=0,
    )
    if subtitle:
        shapes += text_body(
            emu(2.5), int(SLIDE_H * 0.72), SLIDE_W - emu(5), int(SLIDE_H * 0.16),
            para(run(subtitle, grade["body"], color=theme["soft"]), align="ctr"),
            margin=0,
        )
    return wrap_slide(shapes)


def render_bullets(slide: dict, theme: dict, grade: dict) -> str:
    title = slide.get("title", "")
    bullets = slide.get("bullets", [])[:grade["max_bullets"]]
    shapes = ""
    shapes += rect(0, 0, SLIDE_W, SLIDE_H, theme["bg"])
    # 頂部色條
    shapes += rect(0, 0, SLIDE_W, int(SLIDE_H * 0.115), theme["primary"])
    # 標題
    shapes += text_body(
        emu(0.5), emu(0.1), SLIDE_W - emu(1), int(SLIDE_H * 0.115),
        para(run(title, grade["title"], bold=True, color=theme["white"]), align="l", line_spc=12000),
        margin=emu(0.2),
    )
    # 子彈點
    BULLET_H = int((SLIDE_H * 0.84) / max(len(bullets), 1))
    for i, b in enumerate(bullets):
        y = int(SLIDE_H * 0.13) + i * BULLET_H
        shapes += rect(emu(0.35), y + int(BULLET_H * 0.3), emu(0.2), emu(0.2), theme["accent"])
        shapes += text_body(
            emu(0.8), y, SLIDE_W - emu(1.3), BULLET_H,
            para(run(str(b), grade["body"], color=theme["text"]), align="l"),
            margin=emu(0.1),
        )
    return wrap_slide(shapes)


def render_two_column(slide: dict, theme: dict, grade: dict) -> str:
    title = slide.get("title", "")
    left_title = slide.get("left_title", "")
    right_title = slide.get("right_title", "")
    left_items = slide.get("left", [])
    right_items = slide.get("right", [])
    col_w = int(SLIDE_W * 0.46)
    shapes = ""
    shapes += rect(0, 0, SLIDE_W, SLIDE_H, theme["bg"])
    shapes += rect(0, 0, SLIDE_W, int(SLIDE_H * 0.115), theme["primary"])
    shapes += text_body(
        emu(0.5), emu(0.1), SLIDE_W - emu(1), int(SLIDE_H * 0.115),
        para(run(title, grade["title"], bold=True, color=theme["white"]), align="l", line_spc=12000),
        margin=emu(0.2),
    )
    # 左欄
    shapes += rect(emu(0.3), int(SLIDE_H * 0.13), col_w, int(SLIDE_H * 0.085), theme["soft"])
    shapes += text_body(
        emu(0.3), int(SLIDE_H * 0.13), col_w, int(SLIDE_H * 0.085),
        para(run(left_title, grade["body"], bold=True, color=theme["primary"]), align="ctr", line_spc=12000),
    )
    left_y = int(SLIDE_H * 0.225)
    for item in left_items:
        shapes += text_body(
            emu(0.5), left_y, col_w - emu(0.5), grade["body"] * 130,
            para(run(f"・{item}", grade["small"], color=theme["text"]), align="l"),
            margin=emu(0.05),
        )
        left_y += grade["body"] * 130
    # 右欄
    rx = int(SLIDE_W * 0.52)
    shapes += rect(rx, int(SLIDE_H * 0.13), col_w, int(SLIDE_H * 0.085), theme["soft"])
    shapes += text_body(
        rx, int(SLIDE_H * 0.13), col_w, int(SLIDE_H * 0.085),
        para(run(right_title, grade["body"], bold=True, color=theme["primary"]), align="ctr", line_spc=12000),
    )
    right_y = int(SLIDE_H * 0.225)
    for item in right_items:
        shapes += text_body(
            rx + emu(0.2), right_y, col_w - emu(0.5), grade["body"] * 130,
            para(run(f"・{item}", grade["small"], color=theme["text"]), align="l"),
            margin=emu(0.05),
        )
        right_y += grade["body"] * 130
    return wrap_slide(shapes)


def render_compare(slide: dict, theme: dict, grade: dict) -> str:
    title = slide.get("title", "")
    left_title = slide.get("left_title", "")
    right_title = slide.get("right_title", "")
    left_items = slide.get("left", [])
    right_items = slide.get("right", [])
    col_w = int(SLIDE_W * 0.47)
    shapes = ""
    shapes += rect(0, 0, SLIDE_W, SLIDE_H, theme["bg"])
    shapes += rect(0, 0, SLIDE_W, int(SLIDE_H * 0.115), theme["primary"])
    shapes += text_body(
        emu(0.5), emu(0.1), SLIDE_W - emu(1), int(SLIDE_H * 0.115),
        para(run(title, grade["title"], bold=True, color=theme["white"]), align="l", line_spc=12000),
        margin=emu(0.2),
    )
    # 左欄（primary）
    shapes += rect(0, int(SLIDE_H * 0.115), col_w, int(SLIDE_H * 0.885), theme["primary"])
    shapes += text_body(
        emu(0.3), int(SLIDE_H * 0.13), col_w - emu(0.3), int(SLIDE_H * 0.1),
        para(run(left_title, grade["body"], bold=True, color=theme["white"]), align="ctr", line_spc=12000),
    )
    ly = int(SLIDE_H * 0.245)
    for item in left_items:
        shapes += text_body(
            emu(0.5), ly, col_w - emu(0.8), grade["body"] * 140,
            para(run(f"▸ {item}", grade["small"], color=theme["white"]), align="l"),
            margin=emu(0.05),
        )
        ly += grade["body"] * 140
    # 右欄（soft）
    rx = int(SLIDE_W * 0.53)
    shapes += rect(rx, int(SLIDE_H * 0.115), col_w, int(SLIDE_H * 0.885), theme["soft"])
    shapes += text_body(
        rx + emu(0.3), int(SLIDE_H * 0.13), col_w - emu(0.3), int(SLIDE_H * 0.1),
        para(run(right_title, grade["body"], bold=True, color=theme["primary"]), align="ctr", line_spc=12000),
    )
    ry = int(SLIDE_H * 0.245)
    for item in right_items:
        shapes += text_body(
            rx + emu(0.5), ry, col_w - emu(0.8), grade["body"] * 140,
            para(run(f"▸ {item}", grade["small"], color=theme["text"]), align="l"),
            margin=emu(0.05),
        )
        ry += grade["body"] * 140
    return wrap_slide(shapes)


def render_objectives(slide: dict, theme: dict, grade: dict) -> str:
    title = slide.get("title", "學習目標")
    bullets = slide.get("bullets", [])[:6]
    LABEL_COLORS = [theme["primary"], theme["secondary"], theme["accent"]]
    LABELS = ["認知", "情意", "態度"]
    shapes = ""
    shapes += rect(0, 0, SLIDE_W, SLIDE_H, theme["bg"])
    shapes += rect(0, 0, SLIDE_W, int(SLIDE_H * 0.115), theme["primary"])
    shapes += text_body(
        emu(0.5), emu(0.1), SLIDE_W - emu(1), int(SLIDE_H * 0.115),
        para(run(title, grade["title"], bold=True, color=theme["white"]), align="l", line_spc=12000),
        margin=emu(0.2),
    )
    obj_h = int(SLIDE_H * 0.84 / max(len(bullets), 1))
    for i, b in enumerate(bullets):
        y = int(SLIDE_H * 0.13) + i * obj_h
        lc = LABEL_COLORS[i % len(LABEL_COLORS)]
        lb = LABELS[i % len(LABELS)] if i < len(LABELS) else f"{i+1}"
        shapes += rect(emu(0.35), y + int(obj_h * 0.15), emu(0.8), obj_h - int(obj_h * 0.3), lc)
        shapes += text_body(
            emu(0.35), y + int(obj_h * 0.15), emu(0.8), obj_h - int(obj_h * 0.3),
            para(run(lb, grade["small"] - 100, bold=True, color=theme["white"]), align="ctr", line_spc=12000),
            margin=emu(0.05),
        )
        shapes += text_body(
            emu(1.4), y, SLIDE_W - emu(1.8), obj_h,
            para(run(str(b), grade["body"], color=theme["text"]), align="l"),
            margin=emu(0.1),
        )
    return wrap_slide(shapes)


def render_vocab(slide: dict, theme: dict, grade: dict) -> str:
    title = slide.get("title", "詞彙學習")
    items = slide.get("items", [])[:grade["max_bullets"]]
    shapes = ""
    shapes += rect(0, 0, SLIDE_W, SLIDE_H, theme["bg"])
    shapes += rect(0, 0, SLIDE_W, int(SLIDE_H * 0.115), theme["primary"])
    shapes += text_body(
        emu(0.5), emu(0.1), SLIDE_W - emu(1), int(SLIDE_H * 0.115),
        para(run(title, grade["title"], bold=True, color=theme["white"]), align="l", line_spc=12000),
        margin=emu(0.2),
    )
    card_h = int(SLIDE_H * 0.82 / max(len(items), 1))
    for i, item in enumerate(items):
        y = int(SLIDE_H * 0.13) + i * card_h
        word = item.get("word", "")
        reading = item.get("reading", "")
        definition = item.get("definition", "")
        shapes += rect(emu(0.3), y + int(card_h * 0.08), emu(2.2), card_h - int(card_h * 0.16), theme["soft"])
        shapes += text_body(
            emu(0.3), y + int(card_h * 0.08), emu(2.2), card_h - int(card_h * 0.16),
            para(run(word, grade["body"] + 200, bold=True, color=theme["primary"]), align="ctr", line_spc=11000)
            + para(run(reading, grade["small"], color=theme["muted"]), align="ctr"),
            margin=emu(0.1),
        )
        shapes += text_body(
            emu(2.8), y, SLIDE_W - emu(3.1), card_h,
            para(run(definition, grade["body"], color=theme["text"]), align="l"),
            margin=emu(0.1),
        )
    return wrap_slide(shapes)


def render_activity(slide: dict, theme: dict, grade: dict) -> str:
    title = slide.get("title", "課堂活動")
    steps = slide.get("steps", [])[:6]
    shapes = ""
    shapes += rect(0, 0, SLIDE_W, SLIDE_H, theme["bg"])
    shapes += rect(0, 0, SLIDE_W, int(SLIDE_H * 0.115), theme["accent"])
    shapes += text_body(
        emu(0.5), emu(0.1), SLIDE_W - emu(1), int(SLIDE_H * 0.115),
        para(run(title, grade["title"], bold=True, color=theme["white"]), align="l", line_spc=12000),
        margin=emu(0.2),
    )
    step_h = int(SLIDE_H * 0.84 / max(len(steps), 1))
    for i, step in enumerate(steps):
        y = int(SLIDE_H * 0.13) + i * step_h
        shapes += rect(emu(0.3), y + int(step_h * 0.15), emu(0.55), emu(0.55), theme["primary"])
        shapes += text_body(
            emu(0.3), y + int(step_h * 0.15), emu(0.55), emu(0.55),
            para(run(str(i + 1), grade["small"], bold=True, color=theme["white"]), align="ctr", line_spc=12000),
            margin=emu(0.05),
        )
        shapes += text_body(
            emu(1.1), y, SLIDE_W - emu(1.5), step_h,
            para(run(str(step), grade["body"], color=theme["text"]), align="l"),
            margin=emu(0.1),
        )
    return wrap_slide(shapes)


def render_discussion(slide: dict, theme: dict, grade: dict) -> str:
    question = slide.get("question", "")
    timer = slide.get("timer_min", 3)
    hint = slide.get("hint", "")
    shapes = ""
    shapes += rect(0, 0, SLIDE_W, SLIDE_H, theme["primary"])
    # 裝飾大問號圖示區（右側）
    shapes += rect(int(SLIDE_W * 0.72), int(SLIDE_H * 0.1), int(SLIDE_W * 0.26), int(SLIDE_H * 0.8), theme["secondary"])
    shapes += text_body(
        int(SLIDE_W * 0.72), int(SLIDE_H * 0.1), int(SLIDE_W * 0.26), int(SLIDE_H * 0.8),
        para(run("?", grade["title"] + 2000, bold=True, color=theme["white"]), align="ctr"),
    )
    # 問題文字
    shapes += text_body(
        emu(1), int(SLIDE_H * 0.18), int(SLIDE_W * 0.68), int(SLIDE_H * 0.52),
        para(run(question, grade["body"] + 200, bold=True, color=theme["white"]), align="l"),
        margin=emu(0.2),
    )
    # 計時標示
    shapes += rect(emu(0.8), int(SLIDE_H * 0.74), int(SLIDE_W * 0.3), int(SLIDE_H * 0.14), theme["accent"])
    shapes += text_body(
        emu(0.8), int(SLIDE_H * 0.74), int(SLIDE_W * 0.3), int(SLIDE_H * 0.14),
        para(run(f"討論時間：{timer} 分鐘", grade["small"], bold=True, color=theme["white"]), align="ctr", line_spc=12000),
    )
    if hint:
        shapes += text_body(
            emu(0.8), int(SLIDE_H * 0.6), int(SLIDE_W * 0.65), int(SLIDE_H * 0.12),
            para(run(f"提示：{hint}", grade["small"], color=theme["soft"]), align="l"),
            margin=emu(0.1),
        )
    return wrap_slide(shapes)


def render_hero(slide: dict, theme: dict, grade: dict) -> str:
    headline = slide.get("headline", "")
    subline = slide.get("subline", "")
    shapes = ""
    shapes += rect(0, 0, SLIDE_W, SLIDE_H, theme["bg"])
    shapes += rect(0, int(SLIDE_H * 0.42), SLIDE_W, int(SLIDE_H * 0.04), theme["accent"])
    shapes += text_body(
        emu(1.5), int(SLIDE_H * 0.15), SLIDE_W - emu(3), int(SLIDE_H * 0.5),
        para(run(headline, grade["title"] + 800, bold=True, color=theme["primary"]), align="ctr", line_spc=12000),
        margin=0,
    )
    if subline:
        shapes += text_body(
            emu(2), int(SLIDE_H * 0.58), SLIDE_W - emu(4), int(SLIDE_H * 0.22),
            para(run(subline, grade["body"], color=theme["muted"]), align="ctr"),
            margin=0,
        )
    return wrap_slide(shapes)


def render_summary(slide: dict, theme: dict, grade: dict) -> str:
    title = slide.get("title", "重點整理")
    pairs = slide.get("pairs", [])[:grade["max_bullets"]]
    shapes = ""
    shapes += rect(0, 0, SLIDE_W, SLIDE_H, theme["bg"])
    shapes += rect(0, 0, SLIDE_W, int(SLIDE_H * 0.115), theme["primary"])
    shapes += text_body(
        emu(0.5), emu(0.1), SLIDE_W - emu(1), int(SLIDE_H * 0.115),
        para(run(title, grade["title"], bold=True, color=theme["white"]), align="l", line_spc=12000),
        margin=emu(0.2),
    )
    row_h = int(SLIDE_H * 0.84 / max(len(pairs), 1))
    for i, pair in enumerate(pairs):
        y = int(SLIDE_H * 0.13) + i * row_h
        term = pair[0] if len(pair) > 0 else ""
        desc = pair[1] if len(pair) > 1 else ""
        bg = theme["soft"] if i % 2 == 0 else theme["card"]
        shapes += rect(emu(0.3), y + int(row_h * 0.08), SLIDE_W - emu(0.6), row_h - int(row_h * 0.16), bg)
        shapes += text_body(
            emu(0.5), y + int(row_h * 0.08), emu(2.8), row_h - int(row_h * 0.16),
            para(run(term, grade["body"], bold=True, color=theme["primary"]), align="l"),
            margin=emu(0.15),
        )
        shapes += text_body(
            emu(3.5), y + int(row_h * 0.08), SLIDE_W - emu(4.0), row_h - int(row_h * 0.16),
            para(run(desc, grade["small"], color=theme["text"]), align="l"),
            margin=emu(0.15),
        )
    return wrap_slide(shapes)


LAYOUT_MAP = {
    "cover":      render_cover,
    "section":    render_section,
    "bullets":    render_bullets,
    "two-column": render_two_column,
    "compare":    render_compare,
    "objectives": render_objectives,
    "vocab":      render_vocab,
    "activity":   render_activity,
    "discussion": render_discussion,
    "hero":       render_hero,
    "summary":    render_summary,
}

# ══════════════════════════════════════════════════════════════
# PPTX 靜態 XML 構件
# ══════════════════════════════════════════════════════════════
def build_content_types(num_slides: int) -> str:
    slides = "".join(
        f'<Override PartName="/ppt/slides/slide{i+1}.xml" '
        f'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(num_slides)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
        f'{slides}'
        '</Types>'
    )

def build_root_rels() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
        '</Relationships>'
    )

def build_ppt_rels(num_slides: int) -> str:
    slides = "".join(
        f'<Relationship Id="rId{i+3}" '
        f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" '
        f'Target="slides/slide{i+1}.xml"/>'
        for i in range(num_slides)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>'
        f'{slides}'
        '</Relationships>'
    )

def build_slide_master_rels() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
        '</Relationships>'
    )

def build_slide_rels(slide_idx: int) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
        '</Relationships>'
    )

def build_presentation(num_slides: int, bg_hex: str) -> str:
    slide_ids = "".join(
        f'<p:sldId id="{256 + i}" r:id="rId{i+3}"/>'
        for i in range(num_slides)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
        ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        ' saveSubsetFonts="1">'
        '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
        f'<p:sldIdLst>{slide_ids}</p:sldIdLst>'
        f'<p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="custom"/>'
        '<p:notesSz cx="6858000" cy="9144000"/>'
        '</p:presentation>'
    )

def build_theme_xml(theme: dict) -> str:
    bg = theme["bg"]
    primary = theme["primary"]
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="EduTheme">'
        '<a:themeElements>'
        '<a:clrScheme name="EduColors">'
        f'<a:dk1><a:srgbClr val="{clr(theme["text"])}"/></a:dk1>'
        f'<a:lt1><a:srgbClr val="{clr(bg)}"/></a:lt1>'
        f'<a:dk2><a:srgbClr val="{clr(primary)}"/></a:dk2>'
        f'<a:lt2><a:srgbClr val="{clr(theme["soft"])}"/></a:lt2>'
        f'<a:accent1><a:srgbClr val="{clr(theme["accent"])}"/></a:accent1>'
        f'<a:accent2><a:srgbClr val="{clr(theme["secondary"])}"/></a:accent2>'
        f'<a:accent3><a:srgbClr val="{clr(theme["gold"])}"/></a:accent3>'
        f'<a:accent4><a:srgbClr val="{clr(theme["muted"])}"/></a:accent4>'
        '<a:accent5><a:srgbClr val="4BACC6"/></a:accent5>'
        '<a:accent6><a:srgbClr val="F79646"/></a:accent6>'
        '<a:hlink><a:srgbClr val="0563C1"/></a:hlink>'
        '<a:folHlink><a:srgbClr val="954F72"/></a:folHlink>'
        '</a:clrScheme>'
        '<a:fontScheme name="EduFonts">'
        '<a:majorFont>'
        '<a:latin typeface="Work Sans"/>'
        '<a:ea typeface="Microsoft JhengHei"/>'
        '<a:cs typeface=""/>'
        '</a:majorFont>'
        '<a:minorFont>'
        '<a:latin typeface="Noto Sans TC"/>'
        '<a:ea typeface="Microsoft JhengHei"/>'
        '<a:cs typeface=""/>'
        '</a:minorFont>'
        '</a:fontScheme>'
        '<a:fmtScheme name="Office"><a:fillStyleLst>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '</a:fillStyleLst><a:lnStyleLst>'
        '<a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
        '<a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
        '<a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
        '</a:lnStyleLst><a:effectStyleLst>'
        '<a:effectStyle><a:effectLst/></a:effectStyle>'
        '<a:effectStyle><a:effectLst/></a:effectStyle>'
        '<a:effectStyle><a:effectLst/></a:effectStyle>'
        '</a:effectStyleLst><a:bgFillStyleLst>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '</a:bgFillStyleLst></a:fmtScheme>'
        '</a:themeElements></a:theme>'
    )

def build_slide_master(bg_hex: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
        ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<p:cSld>'
        f'<p:bg><p:bgPr><a:solidFill><a:srgbClr val="{clr(bg_hex)}"/></a:solidFill>'
        '<a:effectLst/></p:bgPr></p:bg>'
        '<p:spTree>'
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
        '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        '</p:spTree></p:cSld>'
        '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1"'
        ' accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5"'
        ' accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
        '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId2"/></p:sldLayoutIdLst>'
        '</p:sldMaster>'
    )

def build_slide_layout(bg_hex: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
        ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        ' type="blank" preserve="1">'
        '<p:cSld>'
        f'<p:bg><p:bgPr><a:solidFill><a:srgbClr val="{clr(bg_hex)}"/></a:solidFill>'
        '<a:effectLst/></p:bgPr></p:bg>'
        '<p:spTree>'
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
        '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        '</p:spTree></p:cSld>'
        '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>'
        '</p:sldLayout>'
    )

# ══════════════════════════════════════════════════════════════
# 主要輸出函式
# ══════════════════════════════════════════════════════════════
def normalize_theme(name: str) -> dict[str, str]:
    return EDU_THEMES.get(name, EDU_THEMES["edu-warm"])

def write_pptx(spec: dict, output_path: str, theme_name: str, grade_name: str) -> None:
    theme = normalize_theme(theme_name)
    grade = GRADE_FONT_SCALE.get(grade_name, GRADE_FONT_SCALE["junior"])
    slides_spec = spec.get("slides", [])

    buf = BytesIO()
    with ZipFile(buf, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", build_content_types(len(slides_spec)))
        z.writestr("_rels/.rels", build_root_rels())
        z.writestr("ppt/presentation.xml", build_presentation(len(slides_spec), theme["bg"]))
        z.writestr("ppt/_rels/presentation.xml.rels", build_ppt_rels(len(slides_spec)))
        z.writestr("ppt/theme/theme1.xml", build_theme_xml(theme))
        z.writestr("ppt/slideMasters/slideMaster1.xml", build_slide_master(theme["bg"]))
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", build_slide_master_rels())
        z.writestr("ppt/slideLayouts/slideLayout1.xml", build_slide_layout(theme["bg"]))
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>'
                   '</Relationships>')
        for i, slide_spec in enumerate(slides_spec):
            layout = slide_spec.get("layout", "bullets")
            renderer = LAYOUT_MAP.get(layout, render_bullets)
            slide_xml = renderer(slide_spec, theme, grade)
            z.writestr(f"ppt/slides/slide{i+1}.xml", slide_xml)
            z.writestr(f"ppt/slides/_rels/slide{i+1}.xml.rels", build_slide_rels(i))

    Path(output_path).write_bytes(buf.getvalue())
    print(f"✓ 已輸出：{output_path}（{len(slides_spec)} 張投影片，主題：{theme_name}，年級：{grade_name}）")

# ══════════════════════════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════════════════════════
def main() -> None:
    ap = argparse.ArgumentParser(description="教學簡報生成器 V3.0")
    ap.add_argument("--spec",      required=True,  help="投影片規格 JSON 檔路徑")
    ap.add_argument("--output",    required=True,  help="輸出 .pptx 路徑")
    ap.add_argument("--edu_theme", default="edu-warm",
                    choices=list(EDU_THEMES.keys()), help="色盤主題名稱")
    ap.add_argument("--grade",     default="junior",
                    choices=list(GRADE_FONT_SCALE.keys()), help="年級字體規格")
    args = ap.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"錯誤：找不到規格檔 {args.spec}", file=sys.stderr)
        sys.exit(1)

    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    # 支援 spec 內嵌主題與年級（CLI 參數優先）
    theme_name = args.edu_theme or spec.get("edu_theme", "edu-warm")
    grade_name = args.grade or spec.get("grade_stage", "junior")

    write_pptx(spec, args.output, theme_name, grade_name)

if __name__ == "__main__":
    main()
