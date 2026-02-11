# UI Verification — E2E

> 사용자 플로우 전체가 end-to-end로 동작하는지 검증합니다.
> 이 문서는 프로젝트 시작 시 30-user-flow.md 기반으로 AI가 채웁니다.

## Verification Scope

> **ID Convention**: Use `E-NNN` (e.g., E-001, E-002). Each test case MUST have a unique ID.

#### Happy Path — Full Flow

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| E-001 | Survey 폼 작성 → 제출 → Generate 자동 이동 → 생성 완료 → Complete 이동 → ZIP 다운로드 | 전체 플로우 정상 완료, ZIP 파일 수신 |
| E-002 | Complete 페이지에서 프로젝트 URL 복사 버튼 클릭 | 클립보드에 URL 복사 성공 |
| E-003 | Complete 페이지에서 "새 프로젝트 시작" 클릭 | Survey 페이지로 이동, 빈 폼 표시 |

#### Validation

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| E-004 | Survey 폼에서 필수 필드 비워두고 제출 | 클라이언트측 검증 에러 표시, 제출 차단 |
| E-005 | Survey 폼에서 잘못된 형식 입력 후 제출 | 검증 에러 메시지 표시 |

#### Error Handling

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| E-006 | Survey 제출 시 API 타임아웃 | error 상태 표시, 재시도 가능 |
| E-007 | Generate 단계에서 API 500 에러 | error 상태 + 재시도 버튼 표시 |
| E-008 | Complete 페이지에서 프로젝트 조회 실패 | error 상태 표시 |
| E-009 | ZIP 다운로드 시 네트워크 실패 | 에러 알림 표시, 재시도 가능 |

#### Navigation

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| E-010 | `/generate/{invalid-id}` 직접 접근 | Survey 페이지로 리다이렉트 |
| E-011 | `/complete/{project_id}` (status: intake_saved) 직접 접근 | 적절한 페이지로 리다이렉트 |
| E-012 | 존재하지 않는 경로 접근 | Survey 페이지로 리다이렉트 |
| E-013 | Generate 완료 후 뒤로가기 → Complete → 다시 Generate 직접 접근 | Complete로 리다이렉트 |

#### Re-entry

| ID | 테스트 케이스 | 기대 결과 |
|----|-------------|----------|
| E-014 | Generate 진행 중 브라우저 새로고침 | project_id 기반 상태 복원, 생성 재시도 |
| E-015 | Complete 페이지 새로고침 | project_id로 API 재호출, 정상 표시 |

## Automated Test Location

```
tests/e2e/
```
