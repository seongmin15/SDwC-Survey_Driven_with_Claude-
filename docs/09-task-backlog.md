# Task Backlog

> 이 문서는 프로젝트의 단일 진실 공급원(SSOT)입니다.
> AI가 작업을 제안하고, 사용자가 승인하면 반영됩니다.

## Operating Rules

- 하나의 태스크는 ~30분 리뷰 가능한 크기로 유지합니다.
- WIP Limit: 2
- 상태 전환은 사용자 승인이 필요합니다.
- 이력은 삭제하지 않습니다.

- 모든 구현 태스크는 TDD(Red → Green → Refactor) 사이클을 따릅니다.
- 테스트 커밋이 구현 커밋보다 먼저 와야 합니다.

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

### T001: 프로젝트 기초 구조 및 Docker Compose 설정
- Status: Review
- Service: common
- Description: backend(Poetry/FastAPI), frontend(pnpm/React/Vite) 프로젝트 스캐폴딩 및 docker-compose.yml, Dockerfile 작성. 각 서비스의 /health, /ready 엔드포인트 구현.
- Acceptance Criteria:
  - [x] backend/ 디렉토리에 Poetry 프로젝트 초기화 (pyproject.toml)
  - [x] frontend/ 디렉토리에 pnpm + Vite + React + TypeScript + Tailwind 프로젝트 초기화
  - [x] docker-compose.yml로 postgres, backend_api, web_ui 3개 서비스 기동 확인
  - [x] backend GET /health → 200, GET /ready → 200 (C-023, C-024)
  - [x] frontend GET /health → 200, GET /ready → 200
  - [x] 헥사고날 디렉토리 구조 생성 (domain/, application/, adapters/, config/)
- Result:
  - backend/ — Poetry + FastAPI + 헥사고날 구조 (domain/application/adapters/config), Dockerfile
  - frontend/ — pnpm + Vite + React + TypeScript + Tailwind, health plugin, Dockerfile
  - docker-compose.yml — postgres:16-alpine, backend_api(:8000), web_ui(:3000)
  - 테스트: backend pytest 4 passed (C-023, C-024), frontend vitest 2 passed
  - Docker Compose AC는 이미지 빌드/기동으로 검증 가능 (docker compose up -d --build)

### T002: DB 스키마 및 마이그레이션 설정
- Status: Backlog
- Service: backend_api
- Description: PostgreSQL에 projects, events 테이블 생성. Alembic 마이그레이션 설정. 연결 풀 및 AsyncSession 구성.
- Acceptance Criteria:
  - [ ] Alembic 초기화 및 첫 마이그레이션 스크립트 (up/down)
  - [ ] projects 테이블 생성 (21-data-design.md 스펙 일치)
  - [ ] events 테이블 생성 (FK, CASCADE 포함)
  - [ ] AsyncSession 기반 DB 연결 풀 구성
  - [ ] I-001: 앱 시작 시 PostgreSQL 연결 성공 테스트
  - [ ] I-002: DB 연결 실패 시 /ready 비정상 응답 테스트
- Result:

### T003: Domain 레이어 — 엔티티 및 포트 정의
- Status: Backlog
- Service: backend_api
- Description: 헥사고날 아키텍처 Domain 레이어 구현. Project, Event 엔티티와 Repository 포트(인터페이스) 정의.
- Acceptance Criteria:
  - [ ] Project 엔티티 (id, project_name, status, intake_data, zip_path, created_at, generated_at)
  - [ ] Event 엔티티 (id, project_id, event_type, payload, created_at)
  - [ ] ProjectRepository 포트 (인터페이스) 정의
  - [ ] EventRepository 포트 (인터페이스) 정의
  - [ ] 도메인 예외 정의 (ProjectNotFound, AlreadyGenerated, NotYetGenerated 등)
  - [ ] C-021: Domain 레이어가 FastAPI/SQLAlchemy import 없음 테스트
  - [ ] C-022: 의존성 방향 검증 테스트
- Result:

### T004: Repository Adapter — SQLAlchemy 구현
- Status: Backlog
- Service: backend_api
- Description: Domain 포트의 SQLAlchemy 구현체 작성. projects, events CRUD.
- Acceptance Criteria:
  - [ ] ProjectRepository SQLAlchemy 구현 (create, get_by_id, update_status)
  - [ ] EventRepository SQLAlchemy 구현 (create, list_by_project_id)
  - [ ] I-003: 설문 저장 후 projects 테이블 레코드 존재 테스트
  - [ ] I-004: 설문 저장 후 events 테이블 이벤트 존재 테스트
  - [ ] I-005: intake_data JSONB 정확 저장 테스트
- Result:

### T005: POST /intakes 엔드포인트 구현
- Status: Backlog
- Service: backend_api
- Description: 설문 데이터 저장 API. Use Case + FastAPI Router 구현.
- Acceptance Criteria:
  - [ ] CreateIntake Use Case 구현
  - [ ] POST /intakes FastAPI 라우터 구현
  - [ ] Pydantic 요청/응답 모델 정의
  - [ ] C-001: 유효한 intake_data → 201 테스트
  - [ ] C-002: intake_data 누락 → 400 테스트
  - [ ] C-003: 스키마 검증 실패 → 400 테스트
  - [ ] C-004: 잘못된 타입 → 400 테스트
  - [ ] C-005: 빈 body → 400 테스트
  - [ ] C-006: 잘못된 Content-Type → 에러 테스트
  - [ ] I-011: projects+events 트랜잭션 롤백 테스트
- Result:

### T006: POST /generate 엔드포인트 — Template Matching & Rendering
- Status: Backlog
- Service: backend_api
- Description: 문서 생성 트리거 API. intake_data 기반 템플릿 매칭 및 Jinja2 렌더링 로직 구현.
- Acceptance Criteria:
  - [ ] GenerateDocuments Use Case 구현
  - [ ] Template Engine 서비스 구현 (intake_data → 템플릿 매칭 → Jinja2 렌더링)
  - [ ] CLAUDE.md, docs/*.md, .sdwc/ 구조 파일 생성
  - [ ] C-007: 유효한 project_id → 200, generated 테스트
  - [ ] C-008: project_id 누락 → 400 테스트
  - [ ] C-009: 미존재 project_id → 404 테스트
  - [ ] C-010: UUID 아닌 project_id → 422 테스트
  - [ ] C-011: 이미 generated → 409 테스트
- Result:

### T007: POST /generate 엔드포인트 — ZIP 패키징 및 DB 업데이트
- Status: Backlog
- Service: backend_api
- Description: 렌더링된 문서를 ZIP으로 패키징하고 DB 상태를 업데이트하는 로직 구현.
- Acceptance Criteria:
  - [ ] ZIP Packager 서비스 구현
  - [ ] 생성 결과 ZIP 저장 및 zip_path 기록
  - [ ] I-006: projects.status → generated 변경 테스트
  - [ ] I-007: projects.zip_path 설정 테스트
  - [ ] I-008: projects.generated_at 설정 테스트
  - [ ] I-009: events에 generated 이벤트 테스트
  - [ ] I-012: ZIP 생성 실패 시 트랜잭션 롤백 테스트
- Result:

### T008: GET /projects/:id 엔드포인트 구현
- Status: Backlog
- Service: backend_api
- Description: 프로젝트 메타 조회 API 구현.
- Acceptance Criteria:
  - [ ] GetProject Use Case 구현
  - [ ] GET /projects/:id FastAPI 라우터 구현
  - [ ] C-012: 존재하는 project_id → 200 테스트
  - [ ] C-013: 미존재 project_id → 404 테스트
  - [ ] C-014: UUID 아닌 project_id → 422 테스트
  - [ ] I-010: 조회 결과 DB 데이터 일치 테스트
- Result:

### T009: GET /projects/:id/download 엔드포인트 구현
- Status: Backlog
- Service: backend_api
- Description: ZIP 다운로드 API 구현. 스트리밍 응답.
- Acceptance Criteria:
  - [ ] DownloadProject Use Case 구현
  - [ ] GET /projects/:id/download FastAPI 라우터 구현 (StreamingResponse)
  - [ ] C-015: generated 프로젝트 → 200, application/zip 테스트
  - [ ] C-016: 미존재 project_id → 404 테스트
  - [ ] C-017: 미생성 프로젝트 → 409 테스트
  - [ ] C-018: UUID 아닌 project_id → 422 테스트
- Result:

### T010: 공통 에러 핸들링 및 응답 형식 통합
- Status: Backlog
- Service: backend_api
- Description: 전역 예외 핸들러 및 공통 응답 형식(success/error) 통합.
- Acceptance Criteria:
  - [ ] FastAPI exception handler로 도메인 예외 → HTTP 상태 매핑
  - [ ] C-019: 에러 응답 형식 `{ "error", "message" }` 통합 테스트
  - [ ] C-020: 성공 응답 형식 `{ "data" }` 통합 테스트
  - [ ] S-006: 스택 트레이스 미노출 테스트
  - [ ] S-007: DB 연결 정보 미노출 테스트
  - [ ] S-008: 서버 정보 미노출 테스트
- Result:

### T011: 보안 검증 구현
- Status: Backlog
- Service: backend_api
- Description: 입력 검증 보안 및 환경 보안 테스트 구현.
- Acceptance Criteria:
  - [ ] S-001: SQL injection 문자열 정상 처리 테스트
  - [ ] S-002: 대용량 payload 거부 테스트
  - [ ] S-003: 잘못된 JSON 형식 처리 테스트
  - [ ] S-004: path traversal 거부 테스트
  - [ ] S-005: 빈 body 처리 테스트
  - [ ] S-009: 하드코딩 시크릿 미존재 검사
  - [ ] S-010: Docker 이미지 .env 미포함 검사
  - [ ] S-011: 로그 시크릿 미포함 테스트
  - [ ] S-012: .gitignore 검사
- Result:

### T012: Web UI — 프로젝트 초기화 및 공통 레이아웃
- Status: Backlog
- Service: web_ui
- Description: React 프로젝트 라우팅 설정, 공통 Layout 컴포넌트, API 클라이언트 레이어 구현.
- Acceptance Criteria:
  - [ ] React Router 설정 (/, /generate/:id, /complete/:id, 404 → / 리다이렉트)
  - [ ] 공통 Layout 컴포넌트 (헤더/푸터)
  - [ ] API 클라이언트 모듈 (환경변수 기반 base URL)
  - [ ] V-011: 일관된 헤더/푸터 테스트
  - [ ] V-012: 콘텐츠 영역 중앙 정렬 테스트
  - [ ] E-012: 미존재 경로 → Survey 리다이렉트 테스트
- Result:

### T013: Web UI — Survey 페이지 구현
- Status: Backlog
- Service: web_ui
- Description: intake_schema.yaml 기반 동적 설문 폼 페이지 구현.
- Acceptance Criteria:
  - [ ] 동적 폼 렌더링 (intake_schema.yaml 구조 기반)
  - [ ] 클라이언트측 필수 필드 검증
  - [ ] POST /intakes 호출 및 상태 관리 (idle/loading/success/error)
  - [ ] 성공 시 Generate 페이지로 자동 이동
  - [ ] E-004: 필수 필드 비움 → 검증 에러 테스트
  - [ ] E-005: 잘못된 형식 → 에러 메시지 테스트
  - [ ] E-006: API 타임아웃 → error 상태 테스트
  - [ ] V-001~V-003: 반응형 레이아웃 테스트
  - [ ] V-004~V-006: 상태별 시각 테스트
  - [ ] A-001~A-007: 접근성 테스트
- Result:

### T014: Web UI — Generate 페이지 구현
- Status: Backlog
- Service: web_ui
- Description: 문서 생성 트리거 및 진행 상태 표시 페이지 구현.
- Acceptance Criteria:
  - [ ] 페이지 진입 시 POST /generate 자동 호출
  - [ ] 상태 관리 (idle/loading/success/error)
  - [ ] 성공 시 Complete 페이지로 자동 이동
  - [ ] 에러 시 재시도 버튼
  - [ ] project_id 유효성 검증 → 무효 시 Survey 리다이렉트
  - [ ] E-007: API 500 → error + 재시도 테스트
  - [ ] E-010: invalid-id 직접 접근 → 리다이렉트 테스트
  - [ ] E-013: 이미 generated → Complete 리다이렉트 테스트
  - [ ] E-014: 새로고침 시 상태 복원 테스트
  - [ ] V-007~V-008: 상태별 시각 테스트
  - [ ] A-008~A-010: 접근성 테스트
- Result:

### T015: Web UI — Complete 페이지 구현
- Status: Backlog
- Service: web_ui
- Description: 프로젝트 URL 안내, ZIP 다운로드, URL 복사 기능 구현.
- Acceptance Criteria:
  - [ ] GET /projects/:id 호출하여 프로젝트 정보 표시
  - [ ] ZIP 다운로드 버튼 (GET /projects/:id/download)
  - [ ] URL 복사 버튼 (클립보드 API)
  - [ ] "새 프로젝트 시작" 링크 → Survey
  - [ ] project_id 조회 실패 시 에러 처리
  - [ ] status가 generated가 아닌 경우 리다이렉트
  - [ ] E-001: 전체 happy path 테스트
  - [ ] E-002: URL 복사 테스트
  - [ ] E-003: 새 프로젝트 시작 테스트
  - [ ] E-008: 조회 실패 → error 테스트
  - [ ] E-009: 다운로드 네트워크 실패 테스트
  - [ ] E-011: intake_saved 상태 직접 접근 → 리다이렉트 테스트
  - [ ] E-015: 새로고침 시 상태 복원 테스트
  - [ ] V-009~V-010: 시각 테스트
  - [ ] A-011~A-013: 접근성 테스트
- Result:

### T016: 공통 접근성 및 시각 검증
- Status: Backlog
- Service: web_ui
- Description: 전체 페이지 공통 접근성(Color/Contrast, Focus) 및 브라우저 호환성 검증.
- Acceptance Criteria:
  - [ ] A-014: 일반 텍스트 명암비 4.5:1 이상
  - [ ] A-015: 큰 텍스트 명암비 3:1 이상
  - [ ] A-016: 색상 외 정보 전달 수단 확인
  - [ ] A-017: 포커스 인디케이터 확인
  - [ ] V-013~V-016: Chrome/Firefox/Safari/Edge 렌더링 테스트
- Result:

