# Implementation status

Baseline: d19f192 (2026-09-07). Original checkout HEAD 1cff78d with README changes, four script mode changes and untracked short-video outputs, retained untouched.

| Tasks | Shared interface | Resolution |
|---|---|---|
| Runtime / packaging | scripts/edu_runtime, schemas, examples | Runtime worker supplies canonical package and per-skill schemas/examples; controller syncs copies. |
| Runtime / skill docs | input contract | schema_version 1.0, skill, language, context, sources, content; schema-specific task payloads. |
| Runtime / tests | CLI | --input, --output, --example, --validate-only; explicit migration errors for unsupported old calls. |
| Packaging / documentation | inventory | Exactly 21 existing Skill names, no additional skills. |
| Task 1 internal consistency | validated content / output | Validate before output; explicit examples only. |
| Task 2 internal consistency | single source / independent install | Generated physical copies verified by CI, not runtime sibling dependencies. |

Task 1: in progress.
Task 2: in progress.
Host, Office, GitHub release checks: pending.
