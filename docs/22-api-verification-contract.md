# API Verification — Contract

> API 엔드포인트가 `docs/20-api-contract.md`에 정의된 계약을 준수하는지 검증합니다.
> 이 문서는 프로젝트 시작 시 20-api-contract.md 기반으로 AI가 채웁니다.

## Verification Scope

> **ID Convention**: Use `C-NNN` (e.g., C-001, C-002). Each test case MUST have a unique ID.

#### POST /intakes — Contract

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| C-001 | 유효한 intake_data로 요청 | 201 Created, project_id 반환 |
| C-002 | intake_data 필드 누락 | 400, `MISSING_REQUIRED_FIELD` |
| C-003 | intake_data가 스키마 검증 실패 (필수 하위 필드 누락) | 400, `INVALID_INTAKE_DATA` |
| C-004 | intake_data가 잘못된 타입 (string 대신 number 등) | 400, `INVALID_INTAKE_DATA` |
| C-005 | 빈 JSON body `{}` | 400, `MISSING_REQUIRED_FIELD` |
| C-006 | Content-Type이 application/json이 아님 | 422 또는 415 에러 |

#### POST /generate — Contract

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| C-007 | 유효한 project_id (status: intake_saved) | 200 OK, status: generated |
| C-008 | project_id 누락 | 400, `MISSING_REQUIRED_FIELD` |
| C-009 | 존재하지 않는 project_id | 404, `PROJECT_NOT_FOUND` |
| C-010 | UUID 형식이 아닌 project_id | 422, `INVALID_PROJECT_ID` |
| C-011 | 이미 generated 상태인 프로젝트 | 409, `ALREADY_GENERATED` |

#### GET /projects/:id — Contract

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| C-012 | 존재하는 project_id 조회 | 200 OK, 프로젝트 메타 반환 |
| C-013 | 존재하지 않는 project_id | 404, `PROJECT_NOT_FOUND` |
| C-014 | UUID 형식이 아닌 project_id | 422, `INVALID_PROJECT_ID` |

#### GET /projects/:id/download — Contract

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| C-015 | generated 상태 프로젝트 다운로드 | 200 OK, application/zip 응답 |
| C-016 | 존재하지 않는 project_id | 404, `PROJECT_NOT_FOUND` |
| C-017 | 아직 generated가 아닌 프로젝트 | 409, `NOT_YET_GENERATED` |
| C-018 | UUID 형식이 아닌 project_id | 422, `INVALID_PROJECT_ID` |

#### Error Response Format

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| C-019 | 모든 에러 응답이 `{ "error": "...", "message": "..." }` 형식 | JSON 구조 검증 통과 |
| C-020 | 성공 응답이 `{ "data": { ... } }` 형식 | JSON 구조 검증 통과 |

#### Hexagonal Architecture — Structure

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| C-021 | Domain 레이어가 FastAPI/SQLAlchemy 모듈을 import하지 않음 | import 분석 통과 |
| C-022 | 의존성 방향이 outer → inner만 허용 (Adapter → Application → Domain) | 의존성 분석 통과 |

#### GET /health, GET /ready — Contract

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| C-023 | GET /health 호출 | 200 OK, `{ "status": "ok" }` |
| C-024 | GET /ready 호출 | 200 OK, `{ "status": "ready" }` |

## Automated Test Location

```
tests/contract/
```
