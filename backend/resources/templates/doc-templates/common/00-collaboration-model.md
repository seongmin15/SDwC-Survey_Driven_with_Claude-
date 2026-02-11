# Collaboration Model

> Core rules are in `CLAUDE.md`. This document defines project-specific collaboration settings.

## Roles

- AI: Executor (proposes changes, generates skills/tasks)
- Human: Approver (final decision and application)

## Working Style

- Methodology: {{collaboration.methodology}}
{{#if collaboration.methodology == scrum}}
- Sprint Length: {{collaboration.sprint_length}}
{{/if}}
- Task size target: ~{{collaboration.task_review_minutes}} minutes reviewable.
- WIP Limit: {{collaboration.wip_limit}}
- Prefer diffs/patches for all proposals.
- Keep historical records; do not delete past decisions/tasks.
