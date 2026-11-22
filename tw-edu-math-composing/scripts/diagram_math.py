"""Lay out small math labels using shared text and vector-stroke primitives."""
from dataclasses import dataclass
from typing import Callable


@dataclass
class Box:
    width: float
    top: float
    bottom: float
    paint: Callable[[float, float], None]


def label_box(parts, size, measure, text, stroke):
    def row(values, scale):
        boxes = [part(value, scale) for value in values]

        def paint(x, y):
            for box in boxes:
                box.paint(x, y)
                x += box.width

        return Box(sum(box.width for box in boxes), min(box.top for box in boxes),
                   max(box.bottom for box in boxes), paint)

    def part(value, scale):
        if isinstance(value, str) or "op" in value:
            label = value if isinstance(value, str) else value["op"]
            width, top, bottom = measure(label, scale)
            return Box(width, top, bottom, lambda x, y: text(x, y, label, scale))
        kind, args = next(iter(value.items()))
        if kind == "row":
            return row(args, scale)
        if kind == "frac":
            num, den = (part(arg, scale * .88) for arg in args)
            width = max(num.width, den.width) + scale * .30
            line_y = -scale * .24
            rise = line_y - scale * .11 - num.bottom
            drop = line_y + scale * .14 - den.top

            def paint(x, y):
                num.paint(x + (width - num.width) / 2, y + rise)
                den.paint(x + (width - den.width) / 2, y + drop)
                stroke([(x, y + line_y), (x + width, y + line_y)], max(1, scale * .075))

            return Box(width, rise + num.top, drop + den.bottom, paint)
        if kind == "rad":
            child = part(args, scale)
            shoulder = scale * .62
            roof = min(-scale * .82, child.top - scale * .12)
            bottom = max(0, child.bottom)
            width = shoulder + child.width + scale * .11

            def paint(x, y):
                child.paint(x + shoulder, y)
                stroke([(x, y - scale * .30), (x + scale * .16, y - scale * .37),
                        (x + scale * .28, y + scale * .03), (x + shoulder * .87, y + roof),
                        (x + width, y + roof)], max(1, scale * .075))

            return Box(width, roof, bottom + scale * .03, paint)
        if kind == "sup":
            base, exponent = part(args[0], scale), part(args[1], scale * .7)
            lift = -scale * .53

            def paint(x, y):
                base.paint(x, y)
                exponent.paint(x + base.width, y + lift)

            return Box(base.width + exponent.width, min(base.top, lift + exponent.top),
                       max(base.bottom, lift + exponent.bottom), paint)
        raise ValueError(f"圖中公式標籤不支援 {kind}；可改為文件公式")

    return row(parts, size)
