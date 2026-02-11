# Git Workflow

## Branch Strategy

master_develop_task

### Branch Roles

- `master` (or `main`): 배포용. 직접 커밋 금지.
- `develop`: 개발 기준 브랜치. 모든 task/* 브랜치는 여기서 분기.
- `task/*`: 작업 브랜치. 반드시 develop에서 분기.

### Branch Rules

- task/* 브랜치는 **반드시 develop에서** 생성합니다. master에서 분기하지 않습니다.
- 프로젝트 초기화 시 `git init` 후 즉시 develop 브랜치를 생성하고 전환합니다.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

Task: T<NNN>
```

### Header

- type: feat | fix | docs | refactor | test | chore
- scope: backend_api | web_ui | common | config
- subject: 현재형, 영어, 50자 이내

### Body (optional)

- 변경 이유와 내용을 간결하게 기술
- 72자 줄바꿈 권장

### Footer (required)

- `Task: T<NNN>` — 반드시 포함. 커밋과 태스크를 연결합니다.
- Breaking change가 있으면 `BREAKING CHANGE: <설명>` 추가

## Merge Policy

- PR 생성 주체: user

- task/* → develop: Squash merge 권장
- develop → master: 릴리스 시에만, 사용자 승인 필수

## Rules

- master/main에 직접 커밋 금지
- AI는 diff 제안만, 커밋/머지는 사용자 승인 후
- 하나의 커밋 = 하나의 관심사
- 서비스 간 변경을 하나의 커밋에 섞지 않음
