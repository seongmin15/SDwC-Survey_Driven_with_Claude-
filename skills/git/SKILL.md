Service: sdwc
Artifacts: backend_api, web_ui
Branch Strategy: master_develop_task

Execution Policy:
- Approval Required: true
- Git Flow: develop

## Context

- Project: sdwc
- Branch strategy: master_develop_task

## Rules

- **Branch naming**: `master` (production), `develop` (integration), `task/*` (work branches)
- **Branch creation**: task/* branches MUST branch from `develop`, never from master
- **Protected branches**: master and develop — no direct commits allowed
- **Merge policy**: task/* → develop via Squash merge; develop → master only at release, requires user approval
- **Commit message format**:
  ```
  <type>(<scope>): <subject>

  <body>

  Task: T<NNN>
  ```
  - type: feat | fix | docs | refactor | test | chore
  - scope: backend_api | web_ui | common | config
  - subject: present tense, English, max 50 chars
  - Footer `Task: T<NNN>` is REQUIRED
- **One commit = one concern**: do not mix cross-service changes in a single commit

## Patterns

- **Branch lifecycle**: create from develop → work → commit → push → user creates PR → squash merge → delete branch
- **Commit granularity**: one logical change per commit; separate test commits from implementation commits (TDD)
- **Conflict resolution**: rebase task/* onto develop before PR; resolve conflicts locally, never on remote

## Anti-patterns

- Direct commits to master or develop
- Large monolithic commits mixing unrelated changes
- Force-pushing to shared branches (develop, master)
- Committing secrets, credentials, or .env files
- Omitting Task reference in commit footer
- Mixing backend_api and web_ui changes in one commit

## Checklist

- [ ] Branch name follows `task/<description>` convention
- [ ] Branch created from latest develop
- [ ] Commit message includes `Task: T<NNN>` footer
- [ ] Commit type and scope are correct
- [ ] No untracked files left behind
- [ ] .gitignore covers .env, __pycache__/, node_modules/, .sdwc/
- [ ] No secrets or credentials in committed files
