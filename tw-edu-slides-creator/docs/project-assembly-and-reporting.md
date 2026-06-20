# Project Assembly And Reporting

Read this before QA, speaker notes, PPTX assembly, or final reporting.

## QA

Inspect every final slide image before assembly:

- Traditional Chinese is readable and not garbled.
- Slide content matches `outline.md`.
- Text density fits the grade band.
- Each slide has one teaching purpose.
- Example and explanation are on the same slide when introducing new concepts.
- Text and related visuals are visually adjacent.
- No decorative filler, unrelated logo, fake screenshot, or invented curriculum code appears.
- Required assets are present and not distorted.

Repair severe defects before assembly.

## Teacher Speaker Notes

Create `speech.md` with headings:

```markdown
## Slide 1: Title

Teacher-facing talk track in Traditional Chinese.

---

注意點：
- 重點：...
- 學生可能誤解：...
- 提問：...
- 節奏：...
```

Notes should help a teacher run the class, not merely summarize the slide.

## PPTX Assembly

Run:

```bash
python3 scripts/assemble_image_pptx.py {base_dir} {deck_name}.pptx --aspect-ratio 16:9
```

Verify:

```bash
unzip -l {base_dir}/{deck_name}/{deck_name}.pptx | rg "ppt/slides/slide"
python3 scripts/slide_job_status.py {base_dir}/{deck_name}
```

## Final Report

Report:

- project directory,
- final PPTX path,
- slide image directory,
- `outline.md`,
- `speech.md`,
- slide count,
- backend label,
- QA status,
- any repaired or blocked slides.
