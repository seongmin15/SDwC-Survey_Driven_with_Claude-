# API Verification — Integration

> API와 데이터베이스 간 통합이 정상 동작하는지 검증합니다.
> 이 문서는 프로젝트 시작 시 20-api-contract.md, 21-data-design.md 기반으로 AI가 채웁니다.

## Verification Scope

> **ID Convention**: Use `I-NNN` (e.g., I-001, I-002). Each test case MUST have a unique ID.

#### DB Connection

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| I-001 | 앱 시작 시 PostgreSQL 연결 성공 | 연결 풀 생성, /ready 200 |
| I-002 | DB 연결 실패 시 /ready 응답 | 503 또는 비정상 응답 |

#### POST /intakes → DB

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| I-003 | 설문 저장 후 projects 테이블에 레코드 존재 | SELECT 결과 일치 |
| I-004 | 설문 저장 후 events 테이블에 `intake_saved` 이벤트 존재 | SELECT 결과 일치 |
| I-005 | 설문 저장 시 intake_data가 JSONB로 정확히 저장됨 | JSONB 비교 일치 |

#### POST /generate → DB

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| I-006 | 문서 생성 후 projects.status가 `generated`로 변경 | SELECT 결과 일치 |
| I-007 | 문서 생성 후 projects.zip_path가 설정됨 | NOT NULL 확인 |
| I-008 | 문서 생성 후 projects.generated_at이 설정됨 | NOT NULL 확인 |
| I-009 | 문서 생성 후 events 테이블에 `generated` 이벤트 존재 | SELECT 결과 일치 |

#### GET /projects/:id → DB

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| I-010 | 조회 결과가 DB 데이터와 일치 | 필드별 비교 통과 |

#### Transaction Integrity

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| I-011 | POST /intakes — projects INSERT 실패 시 events INSERT도 롤백 | 양쪽 모두 레코드 없음 |
| I-012 | POST /generate — ZIP 생성 실패 시 status 변경 롤백 | status 원래 값 유지 |

## Automated Test Location

```
tests/integration/
```
