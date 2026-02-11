# API Contract

> 이 문서는 프로젝트 시작 시 AI가 상세를 채웁니다.

## Overview

- Framework: fastapi
- API Style: rest
- Auth: none

## Common Response Format

### Success
```json
{
  "data": { ... }
}
```

### Error
```json
{
  "error": "<error_code>",
  "message": "<human_readable_message>"
}
```

## Endpoints (설문 기준)

POST /intakes — 설문 데이터 저장
POST /generate — 문서 생성 트리거
GET /projects/:id — 프로젝트 메타 조회
GET /projects/:id/download — ZIP 다운로드

---

## Endpoint Details

> 아래 섹션은 프로젝트 시작 시 AI가 채웁니다.
> 각 엔드포인트별 Request/Response 스키마, Error cases를 상세화합니다.

### POST /intakes

설문 데이터를 저장하고 프로젝트를 생성한다.

**Request**

```json
POST /intakes
Content-Type: application/json

{
  "intake_data": {
    "project": { "name": "my-app", "description": "...", "target_users": "...", "core_value": "..." },
    "scope": { "in_scope": ["..."], "out_of_scope": "..." },
    "architecture": { "pattern": "monolith", "internal_style": "hexagonal" },
    "services": ["backend_api", "web_ui"],
    "backend": { "language": "python", "framework": "fastapi", "..." : "..." },
    "web": { "language": "typescript", "framework": "react", "..." : "..." }
  }
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `intake_data` | object | yes | intake_schema.yaml 구조를 따르는 설문 응답 전체 |

**Response** `201 Created`

```json
{
  "data": {
    "project_id": "uuid-string",
    "status": "intake_saved",
    "created_at": "2026-01-01T00:00:00Z"
  }
}
```

**Errors**

| Status | error_code | 조건 |
|--------|-----------|------|
| 400 | `INVALID_INTAKE_DATA` | intake_data가 스키마 검증 실패 |
| 400 | `MISSING_REQUIRED_FIELD` | intake_data 누락 |
| 422 | `UNPROCESSABLE_ENTITY` | JSON 파싱은 성공했으나 의미적 검증 실패 |

**Processing Logic**

1. **Validation** — intake_data를 intake_schema.yaml 기반으로 검증
2. **Persistence** — projects 테이블에 새 레코드 INSERT (status: `intake_saved`, intake_data를 JSONB로 저장)
3. **Event** — events 테이블에 `intake_saved` 이벤트 INSERT
4. **Response** — project_id, status, created_at 반환

---

### POST /generate

저장된 설문 데이터 기반으로 문서 패키지를 생성한다.

**Request**

```json
POST /generate
Content-Type: application/json

{
  "project_id": "uuid-string"
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `project_id` | string (UUID) | yes | 대상 프로젝트 ID |

**Response** `200 OK`

```json
{
  "data": {
    "project_id": "uuid-string",
    "status": "generated",
    "download_url": "/projects/{project_id}/download",
    "generated_at": "2026-01-01T00:01:00Z"
  }
}
```

**Errors**

| Status | error_code | 조건 |
|--------|-----------|------|
| 400 | `MISSING_REQUIRED_FIELD` | project_id 누락 |
| 404 | `PROJECT_NOT_FOUND` | 해당 project_id가 존재하지 않음 |
| 409 | `ALREADY_GENERATED` | 이미 생성 완료된 프로젝트 |
| 422 | `INVALID_PROJECT_ID` | UUID 형식이 아님 |
| 500 | `GENERATION_FAILED` | 문서 생성 중 내부 오류 |

**Processing Logic**

--- *Validation*

1. project_id 형식 검증 (UUID)
2. projects 테이블에서 프로젝트 조회, 존재 여부 및 상태 확인

--- *Core Logic — Template Matching*

3. 프로젝트의 intake_data에서 서비스 목록, 아키텍처 정보 추출
4. doc-templates 목록과 매칭하여 필요한 템플릿 결정

--- *Core Logic — Document Rendering*

5. 각 템플릿에 intake_data 값을 주입하여 문서 렌더링 (Jinja2 등)
6. CLAUDE.md, docs/*.md, .sdwc/ 구조로 파일 생성

--- *Core Logic — ZIP Packaging*

7. 생성된 파일들을 ZIP으로 패키징
8. ZIP 파일을 저장 경로에 기록

--- *Persistence*

9. projects 테이블 status를 `generated`로 UPDATE, zip_path 기록
10. events 테이블에 `generated` 이벤트 INSERT

---

### GET /projects/:id

프로젝트 메타 정보를 조회한다.

**Request**

```
GET /projects/{project_id}
```

| 파라미터 | 위치 | 타입 | 필수 | 설명 |
|---------|------|------|------|------|
| `project_id` | path | string (UUID) | yes | 대상 프로젝트 ID |

**Response** `200 OK`

```json
{
  "data": {
    "project_id": "uuid-string",
    "project_name": "my-app",
    "status": "generated",
    "intake_data": { "..." : "..." },
    "created_at": "2026-01-01T00:00:00Z",
    "generated_at": "2026-01-01T00:01:00Z"
  }
}
```

**Errors**

| Status | error_code | 조건 |
|--------|-----------|------|
| 404 | `PROJECT_NOT_FOUND` | 해당 project_id가 존재하지 않음 |
| 422 | `INVALID_PROJECT_ID` | UUID 형식이 아님 |

**Processing Logic**

1. project_id 형식 검증
2. projects 테이블에서 조회
3. 프로젝트 메타 정보 반환

---

### GET /projects/:id/download

생성된 문서 패키지를 ZIP 파일로 다운로드한다.

**Request**

```
GET /projects/{project_id}/download
```

| 파라미터 | 위치 | 타입 | 필수 | 설명 |
|---------|------|------|------|------|
| `project_id` | path | string (UUID) | yes | 대상 프로젝트 ID |

**Response** `200 OK`

```
Content-Type: application/zip
Content-Disposition: attachment; filename="{project_name}.zip"

<binary ZIP data>
```

**Errors**

| Status | error_code | 조건 |
|--------|-----------|------|
| 404 | `PROJECT_NOT_FOUND` | 해당 project_id가 존재하지 않음 |
| 409 | `NOT_YET_GENERATED` | 아직 문서가 생성되지 않은 프로젝트 |
| 422 | `INVALID_PROJECT_ID` | UUID 형식이 아님 |
| 500 | `FILE_NOT_FOUND` | ZIP 파일이 디스크에서 누락됨 |

**Processing Logic**

1. project_id 형식 검증
2. projects 테이블에서 조회, status가 `generated`인지 확인
3. zip_path에서 파일 존재 확인
4. ZIP 파일을 스트리밍 응답으로 반환

---

### GET /health

**Response** `200 OK`
```json
{ "status": "ok" }
```

### GET /ready

**Response** `200 OK`
```json
{ "status": "ready" }
```
