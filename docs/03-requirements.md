# Requirements

## Services

- backend_api
- web_ui

## Functional Requirements

- 설문 입력 (intake_schema.yaml 기반 동적 폼)
- intake 데이터 + doc-templates 매칭 → 문서 자동 생성 (Template Engine)
- 생성된 문서 ZIP 패키징 및 다운로드
- 프로젝트 URL 발급
- REST API (설문 저장, 생성 트리거, 프로젝트 조회, ZIP 다운로드)
- Web UI (설문 페이지, 생성 페이지, 완료 페이지)
- Docker Compose 로컬 개발 환경
- TDD 기반 개발

### backend_api

- API Style: rest
- Auth: none
- Endpoints:

POST /intakes — 설문 데이터 저장
POST /generate — 문서 생성 트리거
GET /projects/:id — 프로젝트 메타 조회
GET /projects/:id/download — ZIP 다운로드

- Entities:

projects — 프로젝트 (설문 데이터 + 생성 상태)
events — 생성 이벤트 이력

### web_ui

- Pages:

Survey — 설문 입력 페이지
Generate — 문서 생성 페이지
Complete — 프로젝트 URL 안내 페이지

- Flow:

Survey → Generate → Complete (URL 복사)

- Connected API: backend_api

## Non-Functional Requirements

- Architecture: monolith
- Deployment: docker_compose
- Observability: 최소 (health/ready만)

## Tech Stack

| Layer | Technology |
|-------|-----------|

| Backend Language | python |
| Backend Framework | fastapi |
| Database (primary) | postgresql |

| Backend Deploy | docker |

| Frontend Language | typescript |
| Frontend Framework | react |
| CSS | tailwind |
| Frontend Deploy | same_server |

| Infra | docker_compose |

