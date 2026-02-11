# Task Backlog

> 이 문서는 프로젝트의 단일 진실 공급원(SSOT)입니다.
> AI가 작업을 제안하고, 사용자가 승인하면 반영됩니다.

## Operating Rules

- 하나의 태스크는 ~{{collaboration.task_review_minutes}}분 리뷰 가능한 크기로 유지합니다.
- WIP Limit: {{collaboration.wip_limit}}
- 상태 전환은 사용자 승인이 필요합니다.
- 이력은 삭제하지 않습니다.
{{#if collaboration.tdd}}
- 모든 구현 태스크는 TDD(Red → Green → Refactor) 사이클을 따릅니다.
- 테스트 커밋이 구현 커밋보다 먼저 와야 합니다.
{{/if}}

## Status Flow

Backlog → Ready → In Progress → Review → Done

## Task Format

```
### T<NNN>: <제목>
- Status: Backlog | Ready | In Progress | Review | Done
- Service: <서비스명>
- Origin: T<NNN> (선택, 다른 태스크에서 파생 시)
- Description: <설명>
- Acceptance Criteria:
  - [ ] <기준 1>
  - [ ] <기준 2>
- Result: (완료 후 기록)
```

### Origin 규칙

- 다른 태스크의 Result에서 발견된 이슈로 파생된 경우 기록합니다.
- 최초 태스크는 Origin을 생략합니다.

### Result 규칙

- Status가 Done이 되면 Result를 반드시 기록합니다.
- Acceptance Criteria의 모든 항목이 체크되어야 Done으로 전환할 수 있습니다.
- 일부 항목을 다른 태스크로 분리한 경우, 원본 항목을 제거하거나 "deferred to T<NNN>"으로 표기합니다.
- 생성된 파일, 테스트 결과, 발견된 이슈를 포함합니다.
- 태스크 내에서 바로 해결한 이슈도 기록합니다.
- 30분을 초과하는 이슈는 새 태스크 번호로 분리합니다.
- 범위 밖 이슈는 `docs/999-roadmap-extensions.md`로 이동합니다.

---

## Tasks

{{#if collaboration.methodology == scrum}}
### Sprint Format

```
## Sprint <N>
- Goal: <스프린트 목표>
- Period: YYYY-MM-DD ~ YYYY-MM-DD
- Status: Planning | Active | Done

### T<NNN>: ...
```

> 프로젝트 시작 시 AI가 초기 작업 목록과 Sprint 1을 작성합니다.
{{else}}
> 프로젝트 시작 시 AI가 초기 작업 목록을 작성합니다.
{{/if}}
