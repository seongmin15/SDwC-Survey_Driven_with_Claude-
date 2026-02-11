# SKILL-collaboration.md

---
name: collaboration
type: universal
source_docs: [00-project-profile.md, 00-collaboration-model.md, 09-task-backlog.md]
---

{{fixed}}
Service: {{project_name}}
Artifacts: {{source:00-project-profile.md → artifacts}}

Execution Policy:
- Approval Required: true
- Methodology: {{source:00-collaboration-model.md → methodology}}
- WIP Limit: {{source:00-collaboration-model.md → wip_limit}}
- Task Size: {{source:00-collaboration-model.md → task_review_minutes}} min
{{/fixed}}

## Context

- Project: {{project_name}}
- Services: {{source:00-project-profile.md → artifacts}}

## Rules

{{generate}}
Extract from {{source:00-collaboration-model.md}} and {{source:09-task-backlog.md}}:
- Role definitions (AI vs Human responsibilities)
- Task status flow and transition rules
- Approval requirements for each status transition
- Task size constraints and splitting criteria
{{/generate}}

## Patterns

{{generate}}
Recommended collaboration patterns:
- Task proposal format and structure
- How to handle cross-service tasks
- Documentation update triggers (when to update docs/)
- Diff/patch proposal format
{{/generate}}

## Anti-patterns

{{generate}}
Collaboration anti-patterns to avoid:
- Making changes without user approval
- Deleting historical records from backlog
- Exceeding WIP limit
- Scope creep without explicit approval
{{/generate}}

## Checklist

{{generate}}
Pre-task-completion verification:
- All Acceptance Criteria checked
- Result recorded in backlog
- Relevant docs updated
- No scope items left unaddressed
{{/generate}}
