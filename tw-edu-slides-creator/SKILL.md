---
name: tw-edu-slides-creator
description: |
  台灣 K-12 教育簡報生成器。採用 codex-ppt-style 工作流：先確認教學大綱與視覺風格，
  再生成一張樣張，樣張通過後逐頁生成完整 16:9 投影片圖片，寫入講者備註並組裝成 PPTX。
  保留台灣教學脈絡、年級自適應、Bloom 分層、108 課綱、課堂活動與教學 QA。
  觸發詞：簡報、投影片、PPT、slides、上課簡報、教學簡報、課程簡報、做一份簡報。
version: 4.0.0
author: 奇老師・數位敘事力社群
allowed-tools: "Read, Write, Edit, Bash, Task"
tags: [education, slides, pptx, Taiwan, K-12, codex-ppt-style, image-deck]
references:
  - docs/workflow-gates-and-progress.md
  - docs/outline-style-sample.md
  - docs/slide-generation-state.md
  - docs/project-assembly-and-reporting.md
  - references/presentation-style-library.md
  - references/pptx-layout-templates.md
  - references/palette-library.md
  - references/layout-grid.md
  - references/slide_design_principles.md
---

# tw-edu-slides-creator v4.0

台灣 K-12 教育簡報生成 Skill。這版採用 `codex-ppt-skill` 的工作形式：每張投影片先生成為完整 16:9 圖片，再組裝成 `.pptx`，並把 `speech.md` 寫入 PowerPoint 講者備註。

本 skill 的差異不在輸出形式，而在內容框架：它仍負責把教材、課文、活動設計或教學目標轉成適合台灣課堂的簡報節奏，包含年級自適應、Bloom 分層、108 課綱對齊、示例優先、活動安排與教師講稿。

## Hard Constraints

- 使用 `codex-ppt-style` gate：來源整理 -> `outline.md` -> 視覺風格 -> 單頁樣張 -> 全量逐頁生成 -> QA -> `speech.md` -> PPTX 組裝。
- 未完成 outline / style / sample gate 前，不建立 final `deck_spec.json`、`speech.md`、正式 prompts、完整 slide images 或 `.pptx`，除非使用者明確要求跳過確認。
- 每張 final slide 都是一張完整 16:9 投影片圖片，放在 `origin_image/slide_XX.png`。
- 逐頁生成，不得把多張投影片塞進同一張圖片。
- 樣張通過後維持同一視覺身份；版面可以依教學目的變化。
- 所有中文字必須清楚、正確、可讀。若出現亂碼、截斷、過小或重疊，必須修復再組裝。
- 教學簡報不應只是教材摘錄。每張投影片都要服務一個教學行為：引入、示例、解析、練習、討論、統整、延伸。
- 對尚未掌握概念的學生，先示例再解析；不要直接用問題取代教學。
- 說明文字與對應圖像必須同頁相鄰，避免跨頁造成認知負擔。
- 裝飾性視覺一律降到最低；每個視覺元素都要回答「它幫助學生理解什麼？」

## Project Structure

```text
{base_dir}/{deck_name}/
├── origin_image/
│   ├── slide_01.png
│   ├── slide_02.png
│   └── ...
├── prompts/
│   ├── slide_01.json
│   └── ...
├── deck_spec.json
├── outline.md
├── speech.md
├── slide_jobs.json
├── slide_run_state.json
└── {deck_name}.pptx
```

If the user does not specify a destination, use `artifacts/教師/{deck_slug}/` inside the LLM Wiki workspace.

## Default Workflow

1. **Collect teaching context**
   - Topic / 課文 / 教材 source.
   - Grade band: 國小低 / 國小中高 / 國中 / 高中 / 大學.
   - Subject and class duration.
   - Learning objective, prior knowledge, assessment or activity needs.
   - Whether teacher notes are needed. Default: yes.

2. **Read required references**
   - `docs/workflow-gates-and-progress.md`
   - `docs/outline-style-sample.md`
   - `references/slide_design_principles.md`
   - `references/presentation-style-library.md`
   - Existing grade / concept alignment references when available in the parent repo.

3. **Create `outline.md` for confirmation**
   - Use Bloom progression:
     - remember / understand -> concept framing, vocab, example
     - apply / analyze -> comparison, process, practice, error analysis
     - evaluate / create -> discussion, task, reflection, output
   - For each slide, define:
     - slide number and title,
     - teaching purpose,
     - student-facing on-slide text,
     - teacher explanation need,
     - visual idea,
     - activity / question / assessment,
     - grade-density check.
   - Stop for confirmation unless the user explicitly skips it.

4. **Confirm visual style**
   - Offer 2-3 concrete style choices when the user has not specified one.
   - Recommended default is `Edu Warm Classroom` for general K-12 teaching.
   - Use `Academic Clean` for high-school or research-heavy topics, `Neon Circuit` for AI / technology topics, and `Hand-drawn Explainer` for concept explanation.

5. **Generate and approve one sample slide**
   - Pick a representative content slide, not merely the cover.
   - Save as the final filename, such as `origin_image/slide_04.png`.
   - Ask the user to confirm:
     - grade-appropriate density,
     - Chinese legibility,
     - visual explanation quality,
     - teaching usefulness,
     - style consistency.

6. **Create final deck artifacts**
   - Write `deck_spec.json` with teaching context, confirmed style, approved sample, and slide specs.
   - Write one self-contained `prompts/slide_XX.json` per slide.
   - Initialize state:

     ```bash
     python3 scripts/init_slide_jobs.py {deck_dir} --slide-count {N} --backend-label "Codex imagegen" --sample-slide slide_04
     ```

7. **Generate final slide images**
   - Use `imagegen` one slide at a time, or slide subagents when available.
   - Each prompt must include:
     - `Slide NN of TOTAL, independent 16:9 teaching slide image`
     - exact Traditional Chinese on-slide text,
     - grade band and reading density,
     - learning objective,
     - visual explanation role,
     - no watermark, no unrelated logos, no slide number unless requested.
   - Record accepted images:

     ```bash
     python3 scripts/record_slide_result.py {deck_dir} --slide slide_02 --backend-used "Codex imagegen" --selected-source /path/to/generated.png --qa-note "Readable; grade density OK."
     ```

8. **QA and repair**
   - Read `docs/project-assembly-and-reporting.md`.
   - Check each final image for:
     - Traditional Chinese correctness,
     - grade-appropriate density,
     - one teaching purpose,
     - text-image proximity,
     - no decorative clutter,
     - visible examples before analysis,
     - no invented curriculum codes or fake sources.

9. **Write `speech.md`**
   - Use `## Slide N: Title` headings.
   - Write teacher-facing speaker notes in Traditional Chinese.
   - Include `注意點：` for pacing, student misconceptions, board-work cues, and interaction prompts.

10. **Assemble `.pptx`**

    ```bash
    python3 scripts/assemble_image_pptx.py {base_dir} {deck_name}.pptx --aspect-ratio 16:9
    unzip -l {base_dir}/{deck_name}/{deck_name}.pptx | rg "ppt/slides/slide"
    python3 scripts/slide_job_status.py {base_dir}/{deck_name}
    ```

11. **Report**
    - Return project directory, PPTX path, slide count, image directory, `outline.md`, `speech.md`, backend label, and QA status.

## Grade Density Rules

| Grade band | On-slide text density | Visual ratio | Teaching rhythm |
|---|---:|---:|---|
| 國小低 | 20-40 Chinese chars per content slide | 60-70% visual | concrete example, picture, oral prompt |
| 國小中高 | 40-70 chars | 50-60% visual | example -> rule -> quick check |
| 國中 | 70-110 chars | 40-50% visual | concept -> comparison -> guided practice |
| 高中 | 100-160 chars | 30-45% visual | claim -> evidence -> analysis -> transfer |
| 大學 / 研習 | 120-220 chars | depends on purpose | framework, case, discussion, implementation |

If content exceeds density, split the slide. Do not shrink text below readability.

## Slide Role Library

Use roles as planning vocabulary. Do not force a fixed template.

- `cover`: topic, class, hook.
- `learning-goals`: 2-4 concrete objectives.
- `entry-example`: concrete example before abstraction.
- `concept-explain`: definition, diagram, example.
- `vocab`: term, meaning, example sentence.
- `compare`: two concepts, texts, strategies, or errors.
- `process`: step-by-step method.
- `guided-practice`: task, scaffold, expected output.
- `discussion`: question, evidence, sentence starter.
- `misconception`: common error and correction.
- `exit-ticket`: quick formative assessment.
- `summary`: 3-5 takeaways.
- `homework`: output requirement and rubric cue.

## Prompt Pattern

```text
Slide NN of TOTAL, independent 16:9 teaching slide image.
Audience: {grade band}, {subject}.
Learning purpose: {one teaching purpose}.
Style: {confirmed visual style; inspect approved sample if available}.
Title: 「...」
Text, render verbatim in Traditional Chinese:
- 「...」
- 「...」
Visual explanation: {diagram, comparison, example, activity card, timeline, concept map}.
Teaching constraints: text and image must be on the same slide and visually adjacent; example before analysis when introducing new concepts; grade-appropriate text density.
Avoid: decorative filler, emoji, tiny text, fake screenshots, invented curriculum codes, unrelated logos, slide numbers unless requested.
```

## Delta Updates

- `換第 N 張`: revise only that slide prompt/image, record result, reassemble.
- `改風格`: regenerate one sample first, then apply the approved style to affected slides.
- `加活動`: insert one `guided-practice` or `discussion` slide and update state.
- `加講稿`: update `speech.md`, then reassemble PPTX.
- `降低難度`: revise on-slide text and speaker notes for the target grade, regenerate affected images.

## Relationship To Existing Renderer

The existing `assets/slides-kit/` renderer remains in the repo as a structured reference and fallback for schema validation ideas, layout vocabulary, and older editable-deck work. The v4.0 operating flow in this `SKILL.md` is image-based PPTX assembly modeled after `codex-ppt-skill`.

## Reference Map

- `docs/workflow-gates-and-progress.md`: approval gates and completion evidence.
- `docs/outline-style-sample.md`: teaching outline, style, and sample slide rules.
- `docs/slide-generation-state.md`: prompt jobs and state files.
- `docs/project-assembly-and-reporting.md`: QA, notes, PPTX assembly, and final report.
- `references/presentation-style-library.md`: education-focused visual style systems.
- `references/sample-approval-template.md`: sample review checklist.
- `references/slide_design_principles.md`: established education slide design doctrine.
- `assets/slides-kit/`: legacy / reference renderer and layout vocabulary.
