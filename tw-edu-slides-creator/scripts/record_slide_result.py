#!/usr/bin/env python3
"""Record a generated slide image and copy it into origin_image/."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def norm_slide(value: str) -> str:
    value = value.strip()
    if value.startswith("slide_"):
        return f"slide_{int(value.removeprefix('slide_')):02d}"
    return f"slide_{int(value):02d}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck_dir")
    parser.add_argument("--slide", required=True)
    parser.add_argument("--backend-used", required=True)
    parser.add_argument("--selected-source", required=True)
    parser.add_argument("--qa-note", default="")
    args = parser.parse_args()

    deck_dir = Path(args.deck_dir).expanduser().resolve()
    jobs_path = deck_dir / "slide_jobs.json"
    jobs = json.loads(jobs_path.read_text(encoding="utf-8"))
    sid = norm_slide(args.slide)
    source = Path(args.selected_source).expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(source)
    dest = deck_dir / "origin_image" / f"{sid}.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)

    for slide in jobs.get("slides", []):
        if slide.get("slide_id") == sid:
            slide.update(
                {
                    "status": "recorded",
                    "backend_used": args.backend_used,
                    "selected_source": str(source),
                    "final_path": dest.relative_to(deck_dir).as_posix(),
                    "sha256": sha256(dest),
                    "qa_note": args.qa_note,
                    "recorded_at": now(),
                }
            )
            break
    else:
        raise KeyError(f"slide not found: {sid}")

    statuses = {slide.get("status") for slide in jobs.get("slides", [])}
    jobs["run_status"] = "slides_recorded" if statuses <= {"recorded", "accepted"} else "in_progress"
    jobs["updated_at"] = now()
    jobs_path.write_text(json.dumps(jobs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
