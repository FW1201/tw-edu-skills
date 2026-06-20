#!/usr/bin/env python3
"""Print slide_jobs.json status."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck_dir")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    deck_dir = Path(args.deck_dir).expanduser().resolve()
    jobs = json.loads((deck_dir / "slide_jobs.json").read_text(encoding="utf-8"))
    by_status = defaultdict(list)
    for slide in jobs.get("slides", []):
        by_status[slide.get("status", "unknown")].append(slide.get("slide_id"))
    summary = {
        "deck_dir": str(deck_dir),
        "run_status": jobs.get("run_status"),
        "selected_backend": jobs.get("selected_backend"),
        "slide_count": len(jobs.get("slides", [])),
        "counts": {status: len(slides) for status, slides in sorted(by_status.items())},
        "slides": {status: slides for status, slides in sorted(by_status.items())},
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"deck_dir={summary['deck_dir']}")
        print(f"run_status={summary['run_status']}")
        print(f"selected_backend={summary['selected_backend']}")
        for status, slides in summary["slides"].items():
            print(f"{status}: {', '.join(slides)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
