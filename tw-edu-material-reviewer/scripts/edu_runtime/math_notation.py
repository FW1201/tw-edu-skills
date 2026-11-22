"""Word equation objects and conservative legacy numeric notation."""
import re

# Fractions use plain 1/2 or √3/2 only. Dates (7/8 日), URLs and chained ratios stay text.
NUMERIC = re.compile(
    r"(?<![A-Za-z0-9_./:\-])(?P<num>√?\d+)\s*/\s*(?P<den>\d+)(?![A-Za-z0-9_./\-]|\s*[年月日])"
    r"|√(?P<rad>\d+)(?![.\d])"
)


def legacy_runs(text):
    """Convert unambiguous integer fractions and single numeric radicands."""
    end = 0
    for match in NUMERIC.finditer(text):
        if end < match.start():
            yield {"text": text[end:match.start()]}
        if match["rad"] is not None:
            value = {"rad": match["rad"]}
        elif int(match["den"]) == 0:
            yield {"text": match[0]}
            end = match.end()
            continue
        else:
            num = match["num"]
            value = {"frac": [{"rad": num[1:]} if num.startswith("√") else num, match["den"]]}
        yield {"math": [value]}
        end = match.end()
    if end < len(text):
        yield {"text": text[end:]}


def normalize_parts(parts):
    result = []
    for value in parts:
        if isinstance(value, str):
            for run in legacy_runs(value):
                result.extend(run["math"] if "math" in run else [run["text"]])
        else:
            kind, args = next(iter(value.items()))
            if kind == "op":
                result.append(value)
            elif kind == "row":
                result.append({"row": normalize_parts(args)})
            elif kind == "rad":
                result.append({"rad": normalize_argument(args)})
            elif kind in ("matrix", "system"):
                result.append({kind: [[normalize_argument(cell) for cell in row] for row in args]})
            else:
                result.append({kind: [normalize_argument(arg) for arg in args]})
    return result


def normalize_argument(value):
    parts = normalize_parts([value])
    return parts[0] if len(parts) == 1 else {"row": parts}


def validate_runs(runs):
    if not isinstance(runs, list) or not runs:
        raise ValueError("行內數學須為非空片段陣列")
    for run in runs:
        if not isinstance(run, dict) or len(run) != 1:
            raise ValueError("行內片段只可含 text 或 math")
        if "math" in run:
            validate_parts(run["math"])
        elif not isinstance(run.get("text"), str) or not run["text"]:
            raise ValueError("text 片段須為非空字串")


def append_runs(paragraph, text, runs=None, *, allow_legacy=True):
    runs = runs if runs is not None else (legacy_runs(text) if allow_legacy else [{"text": text}])
    has_math = False
    for run in runs:
        if "math" in run:
            paragraph._p.append(native_math(run["math"]))
            has_math = True
        else:
            paragraph.add_run(run["text"])
    return has_math


def native_math(parts):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    def node(name, *children):
        result = OxmlElement("m:" + name)
        for child in children:
            result.append(child)
        return result

    def flatten(values):
        for val in values:
            if isinstance(val, dict) and "row" in val:
                yield from flatten(val["row"])
            else:
                yield val

    def expression(parts):
        return argument("e", {"row": parts})

    def argument(tag, value):
        return node(tag, *(part(element) for element in flatten([value])))

    def part(value):
        if isinstance(value, str):
            run_text = node("t")
            run_text.text = value
            if value != value.strip():
                run_text.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            return node("r", run_text)
        kind, cells = next(iter(value.items()))
        if kind == "row":
            raise ValueError("巢狀 row 請放在運算物件的引數內")
        if kind == "rad":
            hide = node("degHide")
            hide.set(qn("m:val"), "1")
            return node("rad", node("radPr", hide), node("deg"), argument("e", cells))
        if kind == "op":
            run_text = node("t")
            run_text.text = cells
            return node("r", node("rPr", node("nor")), run_text)
        if kind in ("frac", "sup"):
            first, second = cells
            if kind == "frac":
                return node("f", argument("num", first), argument("den", second))
            return node("sSup", argument("e", first), argument("sup", second))
        if kind == "system":
            begin = node("begChr")
            end = node("endChr")
            begin.set(qn("m:val"), "{")
            end.set(qn("m:val"), "")
            return node("d", node("dPr", begin, end),
                        node("e", node("eqArr", *(expression(row) for row in cells))))
        matrix = node("m", *(node("mr", *(argument("e", cell) for cell in row)) for row in cells))
        return node("d", node("e", matrix))

    return node("oMath", *(part(element) for element in flatten(normalize_parts(parts))))


def validate_parts(parts):
    if not isinstance(parts, list) or not parts:
        raise ValueError("公式 parts 必須為非空陣列")
    for value in parts:
        if isinstance(value, str) and value:
            continue
        if not isinstance(value, dict) or len(value) != 1:
            raise ValueError("無效的公式結構")
        kind, rows = next(iter(value.items()))
        if kind == "rad":
            validate_parts([rows])
        elif kind == "row":
            validate_parts(rows)
        elif kind == "op" and isinstance(rows, str) and rows in {"sin", "cos", "tan", "log", "ln"}:
            pass
        elif kind in ("frac", "sup") and isinstance(rows, list) and len(rows) == 2:
            validate_parts(rows)
        elif kind in ("matrix", "system") and isinstance(rows, list) and rows:
            if kind == "matrix" and any(len(row) != len(rows[0]) for row in rows):
                raise ValueError("矩陣每列的欄數必須一致")
            for row in rows:
                validate_parts(row)
        else:
            raise ValueError(f"不支援的公式結構：{kind}")
