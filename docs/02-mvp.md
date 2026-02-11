# MVP

## MVP Scope

- 설문 입력 (intake_schema.yaml 기반 동적 폼)
- intake 데이터 + doc-templates 매칭 → 문서 자동 생성 (Template Engine)
- 생성된 문서 ZIP 패키징 및 다운로드
- 프로젝트 URL 발급
- REST API (설문 저장, 생성 트리거, 프로젝트 조회, ZIP 다운로드)
- Web UI (설문 페이지, 생성 페이지, 완료 페이지)
- Docker Compose 로컬 개발 환경
- TDD 기반 개발

## Out of Scope

> 아래 항목은 MVP에 포함하지 않으며 `docs/999-roadmap-extensions.md`에 기록됩니다.

- 팀 협업 기능
- 사용자 인증
- Notion 연동
- CLI (sdwc clone / sdwc start) — MVP 이후
- CI/CD 파이프라인 — MVP 이후
- 클라우드 배포 — MVP 이후

## Success Criteria

설문 작성 → 문서 생성 → ZIP 다운로드 → Claude Code에서 "프로젝트 시작해" →
Claude가 docs/ 읽고 skills/ 생성하여 프로젝트 초기화 완료.

## Constraints

- Stage: MVP
- Architecture: monolith
- Services: backend_api, web_ui
- Deployment: docker_compose
- Auth: none
- Observability: 최소 (health/ready만)
