"""Compose a math worksheet from a version 1 source file."""
import argparse
from copy import deepcopy
import json
import math
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from xml.etree.ElementTree import Element, SubElement, ElementTree


def native_math(parts):
    from docx.oxml import OxmlElement

    def node(name, *children):
        result = OxmlElement("m:" + name)
        for child in children:
            result.append(child)
        return result

    def expression(parts):
        return node("e", *(part(value) for value in parts))

    def part(value):
        if isinstance(value, str):
            run_text = node("t")
            run_text.text = value
            return node("r", run_text)
        kind, cells = next(iter(value.items()))
        if kind in ("frac", "sup"):
            first, second = cells
            if kind == "frac":
                return node("f", node("num", part(first)), node("den", part(second)))
            return node("sSup", node("e", part(first)), node("sup", part(second)))
        if kind == "system":
            begin = node("begChr")
            end = node("endChr")
            from docx.oxml.ns import qn
            begin.set(qn("m:val"), "{")
            end.set(qn("m:val"), "")
            return node("d", node("dPr", begin, end),
                        node("e", node("eqArr", *(expression(row) for row in cells))))
        matrix = node("m", *(node("mr", *(expression([cell]) for cell in row)) for row in cells))
        return node("d", node("e", matrix))

    return node("oMath", *(part(value) for value in parts))


def validate_parts(parts):
    if not isinstance(parts, list) or not parts:
        raise ValueError("公式 parts 必須為非空陣列")
    for value in parts:
        if isinstance(value, str) and value:
            continue
        if not isinstance(value, dict) or len(value) != 1:
            raise ValueError("無效的公式結構")
        kind, rows = next(iter(value.items()))
        if kind in ("frac", "sup") and isinstance(rows, list) and len(rows) == 2:
            validate_parts(rows)
        elif kind in ("matrix", "system") and isinstance(rows, list) and rows:
            if kind == "matrix" and any(len(row) != len(rows[0]) for row in rows):
                raise ValueError("矩陣每列的欄數必須一致")
            for row in rows:
                validate_parts(row)
        else:
            raise ValueError(f"不支援的公式結構：{kind}")


DEFAULT_FONT = "Noto Serif TC"
DEFAULT_FALLBACK = "Noto Sans TC"
COLUMN_GAP_CM = 0.8


def resolve_font(requested, fallback):
    """Resolve exact family names instead of accepting fontconfig's silent substitutes."""
    matcher = shutil.which("fc-match")
    if not matcher:
        return requested, None, "未找到 fc-match，請開啟成品確認字型。", False
    for family in dict.fromkeys((requested, fallback)):
        result = subprocess.run([matcher, "-f", "%{family}\t%{file}\t%{index}", family],
                                capture_output=True, text=True, check=False)
        fields = result.stdout.strip().split("\t")
        if len(fields) != 3 or not Path(fields[1]).is_file():
            continue
        aliases = [name.strip().casefold() for name in fields[0].split(",")]
        if family.casefold() in aliases:
            note = "" if family == requested else f"找不到 {requested}，改用 {family}。"
            return family, (fields[1], int(fields[2] or 0) % 65536), note, True
    return requested, None, f"找不到 {requested} 或 {fallback}，請確認輸出字型。", False


def layout_zones(source):
    settings = source.get("layout", {})
    if not isinstance(settings, dict):
        raise ValueError("layout 必須為物件")
    mode = settings.get("mode", "single")
    if mode not in ("single", "double", "mixed"):
        raise ValueError("layout.mode 可用 single、double、mixed")
    for key in ("font_family", "fallback_font_family"):
        if key in settings and (not isinstance(settings[key], str) or not settings[key].strip()
                                or any(c in settings[key] for c in "\n\r\t")):
            raise ValueError(f"layout.{key} 必須為單行字型名稱")
    for key in ("column_rule", "exam_header"):
        if key in settings and type(settings[key]) is not bool:
            raise ValueError(f"layout.{key} 須為布林值")
    if "question_gap_pt" in settings:
        gap = settings["question_gap_pt"]
        if type(gap) is not int or not 0 <= gap <= 30:
            raise ValueError("layout.question_gap_pt 須為 0 至 30 點的整數")
    zones = settings.get("zones", [])
    if mode != "mixed":
        if zones:
            raise ValueError("layout.zones 只適用於 mixed")
        return []
    if not isinstance(zones, list) or not zones or not all(isinstance(zone, dict) for zone in zones):
        raise ValueError("mixed 需要至少一個題組分區")
    order = [item["id"] for item in source["items"]]
    positions = []
    for zone in zones:
        first = zone.get("start_item")
        if first not in order:
            raise ValueError(f"分區起始題號不存在：{first}")
        positions.append(order.index(first))
        columns = zone.get("columns")
        if type(columns) is not int or columns not in (1, 2):
            raise ValueError("分區欄數須為 1 或 2")
        if "title" in zone and (not isinstance(zone["title"], str) or not zone["title"].strip()):
            raise ValueError("分區標題須為非空文字")
    if positions[0] != 0 or positions != sorted(set(positions)):
        raise ValueError("分區須從首題開始，依題序排列且不可重複")
    if {zone["columns"] for zone in zones} != {1, 2}:
        raise ValueError("mixed 須同時有一欄及兩欄分區")
    return zones


def chinese_number(number):
    digits = "零一二三四五六七八九"
    if number < 10:
        return digits[number]
    tens, ones = divmod(number, 10)
    if tens > 9:
        raise ValueError("單份教材最多 99 個大題")
    return (digits[tens] if tens > 1 else "") + "十" + (digits[ones] if ones else "")


def numbered_source(source):
    """Derive display labels without replacing the source IDs or changing source text."""
    result = deepcopy(source)
    zones = {zone["start_item"]: zone for zone in layout_zones(result)}
    items = result["items"]
    if not zones and not items[0].get("group_heading"):
        items[0]["group_heading"] = "圖示" if result["purpose"] == "數學圖文" else "練習題"
    section = counter = child = 0
    active_parent = False
    for item in items:
        zone = zones.get(item["id"])
        if zone or item.get("group_heading"):
            if zone and item.get("group_heading"):
                raise ValueError("分區首題請在 zone.title 或 group_heading 擇一設定標題")
            section += 1
            counter = child = 0
            active_parent = False
            target, field = (zone, "title") if zone else (item, "group_heading")
            text = re.sub(r"^(?:第[零一二三四五六七八九十]+部分[｜：:、 ]*|[零一二三四五六七八九十]+、)",
                          "", target.get(field, "練習題"))
            target[field] = f"{chinese_number(section)}、{text}"
        parent = item.get("parent_heading")
        subquestion = item.get("subquestion", False)
        if parent is not None:
            if not isinstance(parent, str) or not parent.strip() or subquestion is not True:
                raise ValueError("parent_heading 須為非空文字，只填在第一個子題")
            counter += 1
            child = 0
            active_parent = True
            item["parent_heading"] = f"{counter}、{parent}"
        if type(subquestion) is not bool:
            raise ValueError("subquestion 須為布林值")
        if subquestion:
            if not active_parent:
                raise ValueError(f'{item["id"]} 的子題缺少 parent_heading')
            child += 1
            item["display_number"] = f"（{child}）"
        else:
            active_parent = False
            counter += 1
            item["display_number"] = f"{counter}、"
    return result


def diagram(spec, svg_path=None, png_path=None, font_family=DEFAULT_FONT, font_file=None):
    width, height = spec["size"]
    if not all(type(v) is int and 0 < v <= 2000 for v in (width, height)):
        raise ValueError("圖面尺寸須是 1–2000 的整數")
    svg = Element("svg", xmlns="http://www.w3.org/2000/svg", viewBox=f"0 0 {width} {height}")
    SubElement(svg, "title").text = spec["alt"]
    SubElement(svg, "rect", width=str(width), height=str(height), fill="white")
    if png_path:
        from PIL import Image, ImageDraw, ImageFont
        picture = Image.new("RGB", (3 * width, 3 * height), "white")
        canvas = ImageDraw.Draw(picture)
        font_path = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
        if not font_path.is_file() and shutil.which("fc-match"):
            font_path = Path(subprocess.check_output(
                ["fc-match", "-f", "%{file}", "DejaVu Sans"], text=True))
        if font_file:
            font = ImageFont.truetype(font_file[0], 38, index=font_file[1])
        else:
            font = ImageFont.truetype(str(font_path), 38) if font_path.is_file() else ImageFont.load_default(size=38)

    def draw_line(points, dashed=False):
        if len(points) < 2:
            raise ValueError("線至少需要兩點")
        if not all(math.isfinite(x) and math.isfinite(y) for x, y in points):
            raise ValueError("座標須為有限數值")
        element = SubElement(svg, "polyline", points=" ".join(f"{x:.3f},{y:.3f}" for x, y in points),
                             fill="none", stroke="#181818", **{"stroke-width": "2"})
        if dashed:
            element.set("stroke-dasharray", "6 5")
        if png_path:
            if not dashed:
                canvas.line([(3 * x, 3 * y) for x, y in points], fill="#181818", width=6)
                return
            distance = 0.0
            for start, end in zip(points, points[1:]):
                length = math.dist(start, end)
                offset = 0.0
                while offset < length:
                    phase = (distance + offset) % 11
                    ink = phase < 6
                    step = min(length - offset, max((6 if ink else 11) - phase, 1e-6))
                    if ink:
                        segment = [tuple(3 * (a + (b - a) * t / length) for a, b in zip(start, end))
                                   for t in (offset, offset + step)]
                        canvas.line(segment, fill="#181818", width=6)
                    offset += step
                distance += length

    for line in spec.get("lines", []):
        draw_line(line)
    for x, y, radius, start, sweep in spec.get("arcs", []):
        angles = [math.radians(start + sweep * index / 90) for index in range(91)]
        draw_line([(x + radius * math.cos(a), y - radius * math.sin(a)) for a in angles])
    for curve in spec.get("curves", []):
        function = {"sin": math.sin, "cos": math.cos, "reciprocal": lambda t: 1 / t}[curve["function"]]
        ox, oy = curve["origin"]
        sx, sy = curve["scale"]
        for low, high in curve["domains"]:
            if not low < high or (curve["function"] == "reciprocal" and low <= 0 <= high):
                raise ValueError("函數區間無效或跨越不連續點")
            values = [low + (high - low) * index / 300 for index in range(301)]
            draw_line([(ox + sx * t, oy - sy * function(t)) for t in values], curve.get("dashed", False))
    for x, y, label in spec.get("labels", []):
        SubElement(svg, "text", x=str(x), y=str(y), **{"font-size": "13", "font-family": f"{font_family}, sans-serif"}).text = label
        if png_path:
            canvas.text((x * 3, y * 3), label, font=font, fill="black", anchor="ls")
    if svg_path:
        ElementTree(svg).write(svg_path, encoding="utf-8", xml_declaration=True)
    if png_path:
        picture.save(png_path)


def validate(source):
    required = ("title", "stage", "purpose")
    if source.get("version") != 1 or any(not source.get(key) for key in required):
        raise ValueError("缺少教材版本、標題、學段或用途")
    ids = set()
    for item in source["items"]:
        key = item["id"]
        if not key.isascii() or not key.isalnum() or key in ids or not item["prompt"]:
            raise ValueError("題目 ID 須是唯一英數字，且須有題幹")
        ids.add(key)
        if "formula" in item:
            if not item["formula"]["latex"]:
                raise ValueError("缺少 LaTeX 原文")
            formula = item["formula"]
            validate_parts(formula["parts"])
            if "answer_blank" in formula and type(formula["answer_blank"]) is not bool:
                raise ValueError("formula.answer_blank 須為布林值")
            if formula.get("answer_blank"):
                tail = formula["parts"][-1]
                if isinstance(tail, str) and tail.rstrip().endswith(("=", "＝")):
                    raise ValueError("answer_blank 會補等號，公式末尾請省略等號")
        if "figure" in item:
            diagram(item["figure"])
        if "table" in item:
            rows = item["table"]
            if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
                raise ValueError("表格欄數不一致")
        if not 0 <= item.get("answer_lines", 0) <= 12:
            raise ValueError("作答行數須介於 0 到 12")
    if not ids:
        raise ValueError("教材至少須有一題")
    zones = {zone["start_item"]: zone for zone in layout_zones(source)}
    columns = 2 if source.get("layout", {}).get("mode") == "double" else 1
    for index, item in enumerate(source["items"]):
        zone = zones.get(item["id"])
        if zone:
            columns = zone["columns"]
        if "column_break" in item and type(item["column_break"]) is not bool:
            raise ValueError("column_break 須為布林值")
        if item.get("column_break") and (columns != 2 or index == 0 or zone or item.get("page_break")):
            raise ValueError("換欄須位於雙欄區內，且不可與區首或換頁同時使用")
        if "group_heading" in item and (not isinstance(item["group_heading"], str)
                                        or not item["group_heading"].strip()):
            raise ValueError("題區標題須為非空文字")
        if "workspace_mm" in item:
            height = item["workspace_mm"]
            if type(height) is not int or not 5 <= height <= 90 or item.get("answer_lines"):
                raise ValueError("workspace_mm 須為 5 至 90 毫米的整數，與 answer_lines 擇一")
    numbered_source(source)


def document(source, path, assets, teacher, font_family):
    from docx import Document
    from docx.enum.section import WD_SECTION_START
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor

    source = numbered_source(source)
    doc = Document()
    section = doc.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.top_margin = section.bottom_margin = Cm(1.6)
    section.left_margin = section.right_margin = Cm(1.8)
    layout = source.get("layout", {})
    exam_header = layout.get("exam_header", False)
    styles = (("Normal", 10.5), ("Title", 15), ("Heading 1", 12),
              ("Heading 2", 11), ("Heading 3", 10.5))
    for name, size in styles:
        style = doc.styles[name]
        style.font.name = font_family
        fonts = style.element.get_or_add_rPr().rFonts
        for attr in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
            fonts.attrib.pop(qn("w:" + attr), None)
        fonts.set(qn("w:eastAsia"), font_family)
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor.from_string("202020")
    normal = doc.styles["Normal"].paragraph_format
    normal.space_after = Pt(3)
    normal.line_spacing = Pt(15)
    for level in (1, 2, 3):
        heading_style = doc.styles[f"Heading {level}"].paragraph_format
        heading_style.space_before = Pt(5 if level == 1 else 4)
        heading_style.space_after = Pt(2)
        heading_style.line_spacing = Pt(17)
        heading_style.keep_with_next = True
    grid = section._sectPr.find(qn("w:docGrid"))
    if grid is not None:
        section._sectPr.remove(grid)
    title = doc.add_heading(source["title"], 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_after = Pt(4)
    border = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "nil")
    border.append(bottom)
    title._p.get_or_add_pPr().append(border)

    graphic = source["purpose"] == "數學圖文"
    role = ("授課用圖" if teacher else "圖文預覽") if graphic else ("教師版" if teacher else "學生版")
    meta = doc.add_paragraph(f'{source["stage"]}　｜　{role}')
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta.paragraph_format.space_after = Pt(5)
    for run in meta.runs:
        run.font.size = Pt(9)
    if not teacher and not graphic:
        fields = "____ 年 ____ 班　　座號 ____　　姓名 ______________"
        if exam_header:
            fields = "學校 ________　　" + fields
        identity = doc.add_paragraph(fields)
        identity.alignment = WD_ALIGN_PARAGRAPH.CENTER
        identity.paragraph_format.space_after = Pt(8)
        for run in identity.runs:
            run.font.size = Pt(9)

    mode = layout.get("mode", "single")
    zones = {zone["start_item"]: zone for zone in layout_zones(source)}
    columns = 1
    question_gap = layout.get("question_gap_pt", 10)

    def switch_columns(count, page_break=False):
        nonlocal columns
        if count == columns and not page_break:
            return
        start = WD_SECTION_START.NEW_PAGE if page_break else WD_SECTION_START.CONTINUOUS
        section = doc.add_section(start)
        settings = section._sectPr.find(qn("w:cols"))
        settings.set(qn("w:num"), str(count))
        settings.set(qn("w:equalWidth"), "1")
        settings.set(qn("w:space"), str(Cm(COLUMN_GAP_CM).twips))
        settings.set(qn("w:sep"), "1" if count == 2 and layout.get("column_rule") else "0")
        columns = count

    for index, item in enumerate(source["items"]):
        zone = zones.get(item["id"])
        separate = index > 0 and not (zone or item.get("column_break") or item.get("page_break"))
        page_break = bool(item.get("page_break"))
        desired = zone["columns"] if zone else (2 if mode == "double" else columns)
        if zone and zone.get("title"):
            if columns != 1 or page_break:
                switch_columns(1, page_break)
            heading = doc.add_heading(zone["title"], level=1)
            if desired != 1:
                # The heading precedes the section break, so it spans the full page.
                heading.paragraph_format.keep_with_next = False
            page_break = False
        if desired != columns:
            switch_columns(desired, page_break)
            page_break = False
        if item.get("column_break"):
            marker = doc.add_paragraph()
            marker.paragraph_format.space_after = Pt(0)
            marker.paragraph_format.line_spacing = Pt(1)
            marker.add_run().add_break(WD_BREAK.COLUMN)
        if item.get("group_heading"):
            group = doc.add_heading(item["group_heading"], level=1)
            group.paragraph_format.page_break_before = page_break
            if separate:
                group.paragraph_format.space_before = Pt(question_gap)
            page_break = False
        subquestion = bool(item.get("subquestion"))
        if item.get("parent_heading"):
            parent = doc.add_heading(item["parent_heading"], level=2)
            parent.paragraph_format.page_break_before = page_break
            if separate and not item.get("group_heading"):
                parent.paragraph_format.space_before = Pt(question_gap)
            page_break = False
        heading_text = item.get("heading", "練習")
        label = item.get("display_number", item["id"])
        separator = " " if subquestion else ""
        heading = doc.add_heading(label + (separator + heading_text if heading_text else ""),
                                  level=3 if subquestion else 2)
        heading.paragraph_format.page_break_before = page_break
        if separate and not item.get("group_heading") and not item.get("parent_heading"):
            heading.paragraph_format.space_before = Pt(question_gap)
        content_cm = (17.4 - COLUMN_GAP_CM * (columns - 1)) / columns - (0.4 if subquestion else 0)
        first_paragraph = len(doc.paragraphs) - 1
        prompt = doc.add_paragraph(item["prompt"])
        prompt.paragraph_format.keep_together = True
        following_answer = bool(item.get("answer") if teacher else
                                item.get("answer_lines") or item.get("workspace_mm"))
        prompt.paragraph_format.keep_with_next = (
            any(key in item for key in ("formula", "figure", "table")) or following_answer
        )
        if "formula" in item:
            math_paragraph = doc.add_paragraph()
            math_paragraph.paragraph_format.line_spacing = 1.0
            formula = item["formula"]
            parts = formula["parts"] + ([" ="] if formula.get("answer_blank") else [])
            math_paragraph._p.append(native_math(parts))
            math_paragraph.paragraph_format.keep_with_next = (
                any(key in item for key in ("figure", "table")) or following_answer
            )
        if "figure" in item:
            picture = doc.add_picture(str(assets / (item["id"] + ".png")), width=Cm(min(13.4, content_cm)))
            picture._inline.docPr.set("descr", item["figure"]["alt"])
            picture_format = doc.paragraphs[-1].paragraph_format
            picture_format.line_spacing = 1.0
            picture_format.keep_with_next = "table" in item or following_answer
        if "table" in item:
            rows = item["table"]
            table = doc.add_table(rows=0, cols=len(rows[0]))
            table.style = "Table Grid"
            table.autofit = False
            for column in table.columns:
                column.width = Cm(content_cm / len(rows[0]))
            for row_index, row in enumerate(rows):
                for cell, data in zip(table.add_row().cells, row):
                    cell.text = str(data)
                    if row_index == 0:
                        shading = OxmlElement("w:shd")
                        shading.set(qn("w:fill"), "EEEEEE")
                        cell._tc.get_or_add_tcPr().append(shading)
                        for run in cell.paragraphs[0].runs:
                            run.bold = True
                    cell.paragraphs[0].paragraph_format.keep_with_next = (
                        row_index + 1 < len(rows)
                        or following_answer
                    )
        if teacher and item.get("answer"):
            teacher_note = doc.add_paragraph()
            teacher_note.paragraph_format.space_before = Pt(3)
            teacher_note.paragraph_format.left_indent = Cm(0.2)
            teacher_note.paragraph_format.keep_together = True
            label, delimiter, answer = item["answer"].partition("｜")
            if delimiter and label in ("解答", "原稿附答"):
                teacher_note.add_run("解析｜").bold = True
                teacher_note.add_run(answer)
            else:
                teacher_note.add_run("解析｜").bold = True
                teacher_note.add_run(item["answer"])
        elif not teacher:
            blank_mm = item.get("workspace_mm", 6 * item.get("answer_lines", 0))
            if blank_mm:
                space = doc.add_paragraph()
                space.paragraph_format.line_spacing = Cm(blank_mm / 10)
                space.paragraph_format.space_before = Pt(0)
                space.paragraph_format.space_after = Pt(0)
        if subquestion:
            for paragraph in doc.paragraphs[first_paragraph:]:
                paragraph.paragraph_format.left_indent = Cm(0.4)
    doc.save(path)


def from_edu_input(data):
    """Adapt the common suite envelope while preserving each item ID."""
    return {
        "version": 1,
        "stage": data["context"]["grade"],
        "sources": [record["title"] for record in data["sources"]],
        **data["content"],
    }


def render_docx_pair(source, output):
    """Produce the suite-standard student/teacher file pair."""
    stem = output.with_suffix("")
    student = stem.with_name(stem.name + "-student").with_suffix(".docx")
    teacher = stem.with_name(stem.name + "-teacher").with_suffix(".docx")
    if any(path.exists() for path in (output, student, teacher)):
        raise ValueError("考卷輸出路徑已存在")
    layout = source.get("layout", {})
    requested = layout.get("font_family", DEFAULT_FONT).strip()
    fallback = layout.get("fallback_font_family", DEFAULT_FALLBACK).strip()
    family, font_file, note, _ = resolve_font(requested, fallback)
    if note:
        print(note, file=sys.stderr)
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="tw-edu-math-", dir=output.parent) as work:
        assets = Path(work)
        for item in source["items"]:
            if "figure" in item:
                diagram(item["figure"], png_path=assets / (item["id"] + ".png"),
                        font_family=family, font_file=font_file)
        for path, has_answers in ((student, False), (teacher, True)):
            document(source, assets / path.name, assets, has_answers, family)
        for path in (student, teacher):
            (assets / path.name).replace(path)
    return [student, teacher]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--validate-only", action="store_true")
    modes.add_argument("--figures-only", action="store_true")
    modes.add_argument("--no-pdf", action="store_true")
    args = parser.parse_args()
    source = json.loads(args.source.read_text(encoding="utf-8"))
    validate(source)
    if args.validate_only:
        print("教材來源驗證通過")
        return
    if not args.output:
        parser.error("請指定 --output")
    soffice = None if args.no_pdf or args.figures_only else shutil.which("soffice")
    if not (args.no_pdf or args.figures_only or soffice):
        parser.error("缺少 soffice；可用 --no-pdf 產生 DOCX")
    out = args.output.resolve()
    if out.exists() and any(out.iterdir()):
        parser.error("請指定空白輸出目錄")
    out.mkdir(parents=True, exist_ok=True)
    layout = source.get("layout", {})
    requested = layout.get("font_family", DEFAULT_FONT).strip()
    fallback = layout.get("fallback_font_family", DEFAULT_FALLBACK).strip()
    font_family, font_file, font_note, resolved = resolve_font(requested, fallback)
    if font_note:
        print(font_note, file=sys.stderr)
    report = {"requested_font": requested, "selected_font": font_family,
              "local_font_confirmed": resolved, "font_note": font_note,
              "layout_mode": layout.get("mode", "single"),
              "column_rule": layout.get("column_rule", False),
              "question_gap_pt": layout.get("question_gap_pt", 10)}
    for item in source["items"]:
        if "figure" in item:
            basename = out / item["id"]
            diagram(item["figure"], basename.with_suffix(".svg"),
                    None if args.figures_only else basename.with_suffix(".png"), font_family, font_file)
    if args.figures_only:
        (out / "render-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        return
    student = {key: source[key] for key in ("version", "title", "stage", "purpose", "sources", "layout") if key in source}
    student["items"] = [{key: value for key, value in item.items() if key in (
        "id", "heading", "prompt", "figure", "formula", "table", "answer_lines", "page_break",
        "column_break", "group_heading", "workspace_mm", "subquestion", "parent_heading"
    )} for item in source["items"]]
    student_file = out / "student.docx"
    teacher_file = out / "teacher.docx"
    document(student, student_file, out, False, font_family)
    document(source, teacher_file, out, True, font_family)
    (out / "student-source.json").write_text(json.dumps(student, ensure_ascii=False, indent=2) + "\n",
                                               encoding="utf-8")
    if soffice:
        with TemporaryDirectory(prefix="math-lo-") as profile:
            env = os.environ.copy()
            if sys.platform == "darwin" and not env.get("FONTCONFIG_FILE"):
                config = Element("fontconfig")
                for font_dir in (Path("/System/Library/Fonts"), Path("/Library/Fonts"),
                                 Path.home() / "Library/Fonts"):
                    SubElement(config, "dir").text = str(font_dir)
                SubElement(config, "cachedir").text = str(Path(profile) / "fonts-cache")
                path = Path(profile) / "fonts.conf"
                ElementTree(config).write(path, encoding="utf-8", xml_declaration=True)
                env["FONTCONFIG_FILE"] = str(path)
            subprocess.run([soffice, "-env:UserInstallation=" + Path(profile).as_uri(), "--headless",
                            "--convert-to", "pdf:writer_pdf_Export", "--outdir", str(out),
                            str(student_file), str(teacher_file)], check=True, env=env)
        for name in ("student.pdf", "teacher.pdf"):
            if not (out / name).is_file():
                raise RuntimeError(f"未產生 {name}")
        font_inspector = shutil.which("pdffonts")
        if font_inspector:
            report["pdf_fonts"] = {}
            for name in ("student.pdf", "teacher.pdf"):
                audit = subprocess.run([font_inspector, str(out / name)], capture_output=True, text=True)
                if audit.returncode != 0:
                    report["pdf_fonts"][name] = "無法讀取字型資訊"
                else:
                    report["pdf_fonts"][name] = audit.stdout.splitlines()[2:]
    (out / "render-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")



if __name__ == "__main__":
    main()
