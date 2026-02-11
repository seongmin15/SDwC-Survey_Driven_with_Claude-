# Data Design

> 이 문서는 프로젝트 시작 시 AI가 상세를 채웁니다.

## Databases

### postgresql — primary

- Engine: postgresql
- Role: primary
- Reason: JSONB 지원으로 설문 데이터를 유연하게 저장 가능. 안정성, 확장성.

## Entities (설문 기준)

projects — 프로젝트 (설문 데이터 + 생성 상태)
events — 생성 이벤트 이력

---

## postgresql (primary) — Table Details

> 아래 섹션은 프로젝트 시작 시 AI가 채웁니다.
> 이 데이터베이스에 속하는 테이블/컬렉션의 상세를 작성합니다.

#### projects 테이블

프로젝트 메타 정보와 설문 데이터를 저장한다.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | UUID | NO | PK, gen_random_uuid() |
| `project_name` | VARCHAR(100) | NO | intake_data.project.name에서 추출 |
| `status` | VARCHAR(20) | NO | 프로젝트 상태 (`intake_saved`, `generated`) |
| `intake_data` | JSONB | NO | 설문 응답 전체 (intake_schema.yaml 구조) |
| `zip_path` | VARCHAR(500) | YES | 생성된 ZIP 파일 경로 (생성 전 NULL) |
| `created_at` | TIMESTAMPTZ | NO | 생성 시각, DEFAULT now() |
| `generated_at` | TIMESTAMPTZ | YES | 문서 생성 완료 시각 (생성 전 NULL) |

**Indexes**

| Name | Columns | Type | Purpose |
|------|---------|------|---------|
| `pk_projects` | `id` | PRIMARY KEY | PK |
| `idx_projects_status` | `status` | BTREE | 상태별 조회 |

**Constraints**

- `chk_projects_status`: `status IN ('intake_saved', 'generated')`

---

#### events 테이블

프로젝트 생성 이벤트 이력을 기록한다.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | UUID | NO | PK, gen_random_uuid() |
| `project_id` | UUID | NO | FK → projects.id |
| `event_type` | VARCHAR(50) | NO | 이벤트 유형 (`intake_saved`, `generated`) |
| `payload` | JSONB | YES | 이벤트 부가 데이터 |
| `created_at` | TIMESTAMPTZ | NO | 이벤트 발생 시각, DEFAULT now() |

**Indexes**

| Name | Columns | Type | Purpose |
|------|---------|------|---------|
| `pk_events` | `id` | PRIMARY KEY | PK |
| `idx_events_project_id` | `project_id` | BTREE | 프로젝트별 이벤트 조회 |
| `idx_events_event_type` | `event_type` | BTREE | 이벤트 유형별 조회 |

**Constraints**

- `fk_events_project`: `project_id REFERENCES projects(id) ON DELETE CASCADE`

## Cross-Database Considerations

> 다중 DB 환경에서의 데이터 정합성과 동기화 전략을 기술합니다.

해당 없음 — 단일 데이터베이스 구성

## Migration Rules

- 모든 마이그레이션은 up/down 양방향으로 작성
- 데이터 삭제가 포함된 마이그레이션은 별도 승인 필요
- 스키마 변경 시 이 문서를 먼저 업데이트
