# Slide Generation State

Read this before creating prompts, generating final slides, or recording slide results.

## Required Files

After the sample is approved, create:

```text
deck_spec.json
prompts/slide_01.json
prompts/slide_02.json
...
slide_jobs.json
slide_run_state.json
```

Each prompt JSON should include:

- slide id and number,
- title,
- exact Traditional Chinese on-slide text,
- grade band,
- learning objective,
- Bloom level,
- teaching purpose,
- confirmed style,
- visual explanation plan,
- required assets,
- output path,
- constraints for readability and grade density.

## State Scripts

Initialize jobs:

```bash
python3 scripts/init_slide_jobs.py {deck_dir} --slide-count {N} --backend-label "Codex imagegen" --sample-slide slide_04
```

Check status:

```bash
python3 scripts/slide_job_status.py {deck_dir}
```

Record an accepted generated slide:

```bash
python3 scripts/record_slide_result.py {deck_dir} \
  --slide slide_02 \
  --backend-used "Codex imagegen" \
  --selected-source /absolute/path/to/generated.png \
  --qa-note "Readable; grade density OK."
```

## Subagents

When slide subagents are available, assign one slide job to each worker. The parent agent owns all state files and final assembly.

Workers return only:

- selected generated image path,
- backend used,
- one-sentence QA note.
