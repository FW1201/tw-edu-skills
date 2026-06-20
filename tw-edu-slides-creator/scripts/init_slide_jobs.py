#!/usr/bin/env python3
"""Initialize slide_jobs.json and slide_run_state.json for image deck generation."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def slide_id(number: int) -> str:
    return f"slide_{number:02d}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck_dir")
    parser.add_argument("--slide-count", type=int, required=True)
    parser.add_argument("--backend-label", default="Codex imagegen")
    parser.add_argument("--sample-slide", default="")
    args = parser.parse_args()

    deck_dir = Path(args.deck_dir).expanduser().resolve()
    (deck_dir / "origin_image").mkdir(parents=True, exist_ok=True)
    (deck_dir / "prompts").mkdir(parents=True, exist_ok=True)
    sample = args.sample_slide.strip()

    slides = []
    for number in range(1, args.slide_count + 1):
        sid = slide_id(number)
        final_path = Path("origin_image") / f"{sid}.png"
        prompt_path = Path("prompts") / f"{sid}.json"
        accepted = sample in {sid, str(number)} and (deck_dir / final_path).exists()
        slides.append(
            {
                "slide_id": sid,
                "number": number,
                "status": "accepted" if accepted else "pending",
                "prompt_path": prompt_path.as_posix(),
                "final_path": final_path.as_posix(),
                "backend": args.backend_label,
                "qa_note": "approved sample" if accepted else "",
            }
        )

    jobs = {
        "created_at": now(),
        "updated_at": now(),
        "run_status": "created",
        "selected_backend": args.backend_label,
        "slide_count": args.slide_count,
        "slides": slides,
    }
    state = {
        "created_at": now(),
        "updated_at": now(),
        "status": "created",
        "history": [{"at": now(), "to": "created", "note": "initialized slide jobs"}],
    }
    (deck_dir / "slide_jobs.json").write_text(json.dumps(jobs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (deck_dir / "slide_run_state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(deck_dir / "slide_jobs.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
