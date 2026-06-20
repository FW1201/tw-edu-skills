# Workflow Gates And Progress

Read this before advancing phases or reporting progress.

## Mandatory Gates

Phase order:

1. Teaching source reading and objective extraction
2. `outline.md` confirmation
3. Visual style confirmation
4. One sample slide approval
5. Full slide image generation
6. QA, speaker notes, and PPTX assembly

Do not create final `deck_spec.json`, `speech.md`, prompt jobs, final slide images, or `.pptx` before the required earlier gates are approved, unless the user explicitly asks to skip confirmations.

If early internal planning is necessary, use draft filenames such as `deck_spec.draft.json` or `speech.draft.md`.

## Visible Progress

Use this checklist for non-trivial decks:

1. Prepare teaching source, outline, and style decisions.
2. Generate and approve one sample slide.
3. Prepare slide jobs and state files.
4. Generate and record final slide images.
5. QA and repair slides.
6. Write teacher notes and assemble PPTX.

Completion evidence:

- Teaching outline: approved `outline.md`.
- Style: one confirmed style direction.
- Sample: one approved `origin_image/slide_XX.png`.
- Jobs: `deck_spec.json`, `prompts/slide_XX.json`, `slide_jobs.json`, and `slide_run_state.json`.
- Results: every expected final slide exists under `origin_image/`.
- Assembly: final `.pptx` exists and speaker notes from `speech.md` are written when applicable.
