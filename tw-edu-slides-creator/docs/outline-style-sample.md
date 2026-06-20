# Outline, Style, And Sample

Read this before writing `outline.md`, choosing visual style, or generating a sample slide.

## Teaching Outline

Create `outline.md` before generating slide images. Each slide must include:

- slide number,
- slide title,
- teaching purpose,
- Bloom level,
- exact student-facing on-slide text,
- teacher explanation need,
- visual explanation idea,
- activity / discussion / assessment cue,
- grade-density check,
- required assets.

Use example-first design for new concepts:

1. show a concrete example,
2. guide students to notice features,
3. explain the concept,
4. practice or transfer.

Stop after presenting the outline unless the user explicitly asked to continue without approval.

## Style

If the user has not specified a style, offer 2-3 options and recommend one. Include:

- palette,
- typography,
- layout rhythm,
- illustration or diagram treatment,
- density rules,
- anti-patterns.

Default recommendations:

- `Edu Warm Classroom`: general K-12 teaching.
- `Academic Clean`: high-school or evidence-heavy content.
- `Neon Circuit`: AI / technology / digital learning.
- `Hand-drawn Explainer`: abstract concepts and process explanations.

## Sample Slide

Generate exactly one representative content slide after outline and style confirmation.

Requirements:

- Save it as its final filename, such as `origin_image/slide_04.png`.
- Use real teaching content, not a generic title page.
- State the backend/tool used.
- Ask the user to confirm grade appropriateness, text clarity, visual explanation quality, and teaching usefulness.

After approval, record:

```json
{
  "sample_generation_method": {
    "backend_used": "Codex imagegen",
    "tool_name": "imagegen",
    "mode": "generate",
    "approved_sample_path": "origin_image/slide_04.png",
    "handoff_rule": "Use the same backend family and inspect the approved sample for style consistency."
  }
}
```
