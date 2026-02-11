# API Verification — Security

> API의 보안 관련 항목을 검증합니다.
> 이 문서는 프로젝트 시작 시 AI가 채웁니다.

## Auth Policy

- Auth: none

## Verification Scope

> **ID Convention**: Use `S-NNN` (e.g., S-001, S-002). Each test case MUST have a unique ID.

#### Input Validation

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| S-001 | intake_data에 SQL injection 문자열 포함 | 정상 저장 (JSONB이므로 SQL 실행 안됨), 에러 아님 |
| S-002 | 매우 큰 payload (10MB 이상) 전송 | 413 또는 적절한 거부 응답 |
| S-003 | 잘못된 JSON 형식 전송 | 400/422 에러, 서버 크래시 없음 |
| S-004 | project_id에 path traversal 문자열 (`../../etc/passwd`) | 422, `INVALID_PROJECT_ID` |
| S-005 | 빈 body 전송 | 400/422 에러, 서버 크래시 없음 |

#### Information Exposure

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| S-006 | 에러 응답에 스택 트레이스가 포함되지 않음 | error/message 필드만 존재 |
| S-007 | 에러 응답에 DB 연결 정보가 노출되지 않음 | 연결 문자열 미포함 |
| S-008 | 존재하지 않는 엔드포인트 호출 시 서버 정보 미노출 | Server 헤더에 버전 정보 없음 |

#### Environment Security

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| S-009 | 환경변수에 하드코딩된 시크릿이 없음 | 코드 내 시크릿 리터럴 미발견 |
| S-010 | Docker 이미지에 .env 파일 미포함 | 이미지 레이어 검사 통과 |
| S-011 | 로그에 시크릿/개인정보 미포함 | 로그 출력 검사 통과 |
| S-012 | .gitignore에 .env, __pycache__/, node_modules/ 포함 | 파일 검사 통과 |

## Automated Test Location

```
tests/security/
```
