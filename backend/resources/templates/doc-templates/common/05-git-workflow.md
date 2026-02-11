# Git Workflow

## Branch Strategy

{{git.branch_strategy}}

### Branch Roles

{{#if git.branch_strategy == master_develop_task}}
- `master` (or `main`): 배포용. 직접 커밋 금지.
- `develop`: 개발 기준 브랜치. 모든 task/* 브랜치는 여기서 분기.
- `task/*`: 작업 브랜치. 반드시 develop에서 분기.
{{/if}}

{{#if git.branch_strategy == main_feature}}
- `main`: 통합 및 배포 브랜치. 직접 커밋 금지.
- `task/*`: 작업 브랜치. 반드시 main에서 분기.
{{/if}}

{{#if git.branch_strategy == trunk}}
- `main`: 단일 통합 브랜치. 항상 배포 가능 상태 유지.
- `task/*`: 짧은 수명의 작업 브랜치. main에서 분기, 빠르게 머지.
{{/if}}

{{#if git.branch_strategy == gitflow}}
- `master` (or `main`): 배포용. 직접 커밋 금지.
- `develop`: 개발 기준 브랜치. 모든 feature/* 브랜치는 여기서 분기.
- `feature/*`: 기능 개발 브랜치. develop에서 분기.
- `release/*`: 릴리스 준비 브랜치. develop에서 분기.
- `hotfix/*`: 긴급 수정 브랜치. master에서 분기.
{{/if}}

### Branch Rules

{{#if git.branch_strategy == master_develop_task}}
- task/* 브랜치는 **반드시 develop에서** 생성합니다. master에서 분기하지 않습니다.
- 프로젝트 초기화 시 `git init` 후 즉시 develop 브랜치를 생성하고 전환합니다.
{{/if}}

{{#if git.branch_strategy == main_feature}}
- task/* 브랜치는 **반드시 main에서** 생성합니다.
- develop 브랜치는 사용하지 않습니다.
- 프로젝트 초기화 시 `git init`으로 main 브랜치에서 시작합니다.
{{/if}}

{{#if git.branch_strategy == trunk}}
- task/* 브랜치는 main에서 생성하며, 가능한 빠르게 (1일 이내) 머지합니다.
- 장기 브랜치를 만들지 않습니다.
{{/if}}

{{#if git.branch_strategy == gitflow}}
- feature/* 브랜치는 **반드시 develop에서** 생성합니다.
- 프로젝트 초기화 시 `git init` 후 즉시 develop 브랜치를 생성하고 전환합니다.
- 릴리스 시 develop → release/* → master 순서를 따릅니다.
{{/if}}

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

Task: T<NNN>
```

### Header

- type: feat | fix | docs | refactor | test | chore
- scope: {{#each services}}{{this}}{{#unless @last}} | {{/unless}}{{/each}} | common | config
- subject: 현재형, 영어, 50자 이내

### Body (optional)

- 변경 이유와 내용을 간결하게 기술
- 72자 줄바꿈 권장

### Footer (required)

- `Task: T<NNN>` — 반드시 포함. 커밋과 태스크를 연결합니다.
- Breaking change가 있으면 `BREAKING CHANGE: <설명>` 추가

## Merge Policy

- PR 생성 주체: {{git.pr_by}}
{{#if git.branch_strategy == master_develop_task}}
- task/* → develop: Squash merge 권장
- develop → master: 릴리스 시에만, 사용자 승인 필수
{{/if}}
{{#if git.branch_strategy == main_feature}}
- task/* → main: Squash merge 권장
{{/if}}
{{#if git.branch_strategy == trunk}}
- task/* → main: Squash merge 권장
{{/if}}
{{#if git.branch_strategy == gitflow}}
- feature/* → develop: Squash merge 권장
- develop → master: 릴리스 시에만, 사용자 승인 필수
{{/if}}

## Rules

- master/main에 직접 커밋 금지
- AI는 diff 제안만, 커밋/머지는 사용자 승인 후
- 하나의 커밋 = 하나의 관심사
- 서비스 간 변경을 하나의 커밋에 섞지 않음
