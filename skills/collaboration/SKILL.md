Service: sdwc
Artifacts: backend_api, web_ui

Execution Policy:
- Approval Required: true
- Methodology: kanban
- WIP Limit: 2
- Task Size: 30 min

## Context

- Project: sdwc
- Services: backend_api, web_ui

## Rules

- **Roles**: AI is Executor (proposes changes, generates skills/tasks); Human is Approver (final decision)
- **Task status flow**: Backlog → Ready → In Progress → Review → Done
- **Status transitions require user approval**
- **Task size**: each task must be reviewable in ~30 minutes; split larger tasks
- **WIP Limit**: maximum 2 tasks In Progress at any time
- **Historical records**: never delete past tasks or decisions
- **Result required**: when status becomes Done, Result must be recorded
- **Acceptance Criteria**: all items must be checked before transitioning to Done; deferred items marked "deferred to T<NNN>"
- **Origin tracking**: tasks derived from other tasks must include Origin field
- **TDD mandatory**: every implementation task follows Red → Green → Refactor; test committed before implementation
- **Post-task**: update backlog → commit on task/* branch → push → notify user for PR → wait for merge

## Patterns

- **Task proposal**: use the format in docs/09-task-backlog.md (T<NNN>, Status, Service, Description, AC, Result)
- **Cross-service tasks**: split into separate tasks per service when possible; if tightly coupled, note both services
- **Documentation updates**: update relevant docs/ files when API contract, data design, or user flow changes
- **Diff/patch format**: prefer showing diffs for all code proposals

## Anti-patterns

- Making changes without user approval
- Deleting historical records from backlog
- Exceeding WIP limit (max 2 concurrent In Progress)
- Scope creep without explicit approval
- Skipping TDD cycle (writing implementation before tests)
- Moving tasks to Done without recording Result
- Expanding project scope beyond docs/ without approval

## Checklist

- [ ] All Acceptance Criteria checked
- [ ] Result recorded in backlog with files created, test results, issues found
- [ ] Relevant docs updated (API contract, data design, user flow)
- [ ] No scope items left unaddressed
- [ ] TDD cycle followed: test committed before implementation
- [ ] Task branch pushed and user notified for PR
