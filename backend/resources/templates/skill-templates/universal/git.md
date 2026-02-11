# SKILL-git.md

---
name: git
type: universal
source_docs: [00-collaboration-model.md, 05-git-workflow.md, 09-task-backlog.md]
---

{{fixed}}
Service: {{project_name}}
Artifacts: {{source:00-project-profile.md → artifacts}}
Branch Strategy: {{source:05-git-workflow.md → branch_strategy}}

Execution Policy:
- Approval Required: true
- Git Flow: {{@integration_branch}}
{{/fixed}}

## Context

- Project: {{project_name}}
- Branch strategy: {{source:05-git-workflow.md → branch_strategy}}

## Rules

{{generate}}
Extract from {{source:05-git-workflow.md}}:
- Branch naming conventions
- Merge policy (fast-forward, squash, etc.)
- Protected branch settings
- Commit message format and required fields
{{/generate}}

## Patterns

{{generate}}
Based on the branch strategy, describe:
- Recommended branch lifecycle (create → work → PR → merge → delete)
- Commit granularity guidelines
- Conflict resolution workflow
{{/generate}}

## Anti-patterns

{{generate}}
Common git anti-patterns to avoid:
- Direct commits to protected branches
- Large monolithic commits mixing unrelated changes
- Force-pushing to shared branches
- Committing secrets, credentials, or .env files
{{/generate}}

## Checklist

{{generate}}
Pre-commit/pre-push verification items:
- Branch name follows naming convention
- Commit message includes Task reference (T<NNN>)
- No untracked files left behind
- .gitignore covers all generated/sensitive files
{{/generate}}
