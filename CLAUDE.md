# CLAUDE.md

## Core Rules

- AI acts as the executor. The human user is the final approver.
- Explicit user approval is required before any repository change.
- The project scope is defined by `docs/`. Do NOT expand scope without approval.
- Out-of-scope ideas go to `docs/999-roadmap-extensions.md`.
- Reference the skill matching the current target service: `skills/{service-name}/SKILL.md`.
- Global skills in `~/.claude/skills/` may be used as supplementary reference.
- `docs/*`: AI may propose edits. Changes require user approval. **All content in docs/ MUST be written in Korean (한글).**
- `skills/*/SKILL.md`: AI creates and updates. **MUST be written in English.**
- `.sdwc/skill-templates/*`: Read-only reference. NOT tracked by git.
- When applying the frontend-design skill, each task's acceptance criteria always take precedence. Apply design on top of meeting accessibility (WCAG AA), browser compatibility, and form usability requirements.

---

## Model Routing

- Planning, architecture decisions, document filling, and review: main agent (Opus).
- Code implementation tasks: dispatched with `--model sonnet`.
- Main agent reviews all code output before proposing to the user.

---

## TDD Policy

- Every implementation task follows Red → Green → Refactor:
  1. **Red**: Write failing test(s) first based on Acceptance Criteria.
  2. **Green**: Write minimal code to make the test(s) pass.
  3. **Refactor**: Clean up while keeping tests green.
- Test must be committed BEFORE implementation code.
- Task is not Done until all tests pass.
- Verification documents (22–24, 31–33) serve as the test specification source.

---

## Task Execution

`docs/09-task-backlog.md` is the SSOT for project task tracking.

### Rules

- AI may propose tasks in Backlog.
- Tasks must remain small (≈30 min review size).
- Status transitions require approval.
- Historical records must not be deleted.
- Result must be recorded when Status becomes Done.
- All Acceptance Criteria must be checked before transitioning to Done. If an item is deferred, remove it or mark "deferred to T<NNN>".
- Tasks derived from other tasks must include Origin.
- Issues exceeding 30 min must be split into a new task.
- Out-of-scope issues must be moved to `docs/999-roadmap-extensions.md`.

### Status Flow

Backlog → Ready → In Progress → Done

### Post-Task Completion (per task)

1. Update `docs/09-task-backlog.md`: set Status to Done, write Result.
2. Commit all changes (code + backlog update) on `task/*` branch.
3. `git push origin task/*`.

4. Notify user that the branch is ready for PR.

5. **Stop and wait** for user to merge the PR into develop.
6. After user confirms merge: `git checkout develop` → `git pull origin develop`.
7. Delete finished branch: `git branch -d task/*`.

---

## Project Initialization

Execute the following steps in order upon "프로젝트 시작해":

1. Read all files under `docs/`.
2. Fill detail documents (each **phase** requires approval — present all docs in a phase together):
   - **Phase 0**: Common detail docs (04-architecture.md Component Diagram)
   - **Phase A-1**: API contract (20)
   - **Phase A-2**: Data design (21, only if DB used)
   - **Phase B**: User flow (30)
   - **Phase C**: API verification (22 → 23 → 24) — requires Phase A complete
   - **Phase D**: UI verification (31 → 32 → 33) — requires Phase B complete
   - **Phase E**: Deployment template (10-*) — if present
   > Non-MSA: `docs/10~33-*.md`
   > MSA: `docs/services/{service-name}/20~33-*.md`
   > **Rules**:
   > - **Replace** each `<!-- AI:INIT: -->` comment block with the generated content (the comment itself must not remain).
   > - `<!-- AI:ONGOING: -->` comments are NOT filled during initialization — leave them as-is.
   > - Do NOT modify any existing content above or around AI comments.
3. Generate skill files under `skills/` using `.sdwc/skill-templates/` as reference.
   - Universal: `skills/git/SKILL.md`, `skills/collaboration/SKILL.md` (always)
   - Per-service: based on the Artifacts list in `docs/00-project-profile.md`, generate `skills/{service-name}/SKILL.md`
4. Generate `README.md` (requires approval).
   - Include project summary, tech stack, and getting started based on `docs/`.
5. Write initial task list in `docs/09-task-backlog.md` (requires approval).

6. **Verify completeness** (requires approval).
   > Tip: Use regex `[CISEAVP]-\d{3}` to extract verification IDs. Group results by category prefix for readability.
   - **6-1 API Reference Consistency**: Extract all API calls (e.g., `POST /intakes`) from consumer docs (`docs/30-user-flow.md`, etc.) and verify each exists as a heading in `docs/20-api-contract.md`.
   - **6-2 AC Traceability**: Extract all verification IDs (pattern: `C-NNN`, `I-NNN`, `S-NNN`, `E-NNN`, `A-NNN`, `V-NNN`) from verification docs (22–24, 31–33). Then extract all IDs referenced in task Acceptance Criteria in `docs/09-task-backlog.md`. Every verification ID must appear in at least one task AC. Consecutive IDs in the same category may use range notation (e.g., `C-001~C-010 → T003`). Non-consecutive IDs must be listed individually.
   - **6-3 Scope Coverage**: For each item in `scope.in_scope` from `docs/intake_data.yaml`, identify which task(s) cover it. Every scope item must have at least one corresponding task. Items that describe development methodology (e.g., "TDD") are covered by CLAUDE.md policies and need not map to a specific task.
   - **6-4 Dependency Order**: Verify tasks are ordered so that each task's prerequisites appear earlier. Typical ordering: infrastructure → data layer → API endpoints → business logic → UI pages → integration/E2E.
   - **6-5 No Residual AI Comments**: Verify that no `<!-- AI:INIT:` comments remain in any `docs/*.md` file. All should have been replaced in Step 2.
   - If gaps are found: add missing endpoints to API contract, add missing tasks, fix ordering, or update Acceptance Criteria. Then re-present the updated backlog for approval.

7. Run `git init` + generate `.gitignore` + initial commit on master.
   - `.gitignore` must include `.sdwc/`, language-specific ignores (e.g., `__pycache__/`, `node_modules/`, `*.pyc`), `.env`, and IDE files.
   - Immediately create and switch to `develop` branch: `git checkout -b develop`.
   - All subsequent work happens on `develop` or `task/*` branches from develop.

8. Ask user for remote repository URL. If provided, run `git remote add origin <url>` + `git push`. Otherwise skip.
9. Propose the first task.

---

## Project Resume

When the user says "프로젝트 이어서 해" or indicates continuation:

1. Read `docs/09-task-backlog.md` to identify current state.
2. Check which tasks are In Progress, Review, or Done.
3. Re-read the **Task Execution** section of this file (including Post-Task Completion).

4. Read relevant docs for the next pending task.

5. Verify current git branch: `git branch` → confirm on `develop`.

6. Propose the next action based on backlog state.

> Do NOT re-run Project Initialization. All state is already in docs/ and git.
