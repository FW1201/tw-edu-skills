# Slide Worker Handoff

You are generating exactly one teaching slide image for `tw-edu-slides-creator`.

Read only the assigned `prompts/slide_XX.json` and any explicitly provided images. Use the approved sample slide as style reference if listed. Do not edit `outline.md`, `deck_spec.json`, `slide_jobs.json`, `speech.md`, or other slide prompt files.

Return:

- selected image path,
- backend/tool used,
- one-sentence QA note about readability and grade density.

The parent agent will record the result and assemble the deck.
