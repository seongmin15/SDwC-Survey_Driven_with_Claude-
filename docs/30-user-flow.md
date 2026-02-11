# User Flow

> 이 문서는 프로젝트 시작 시 AI가 상세를 채웁니다.

## Overview

- Framework: react
- Connected API: backend_api

## Pages (설문 기준)

Survey — 설문 입력 페이지
Generate — 문서 생성 페이지
Complete — 프로젝트 URL 안내 페이지

## Flow (설문 기준)

Survey → Generate → Complete (URL 복사)

---

## Page Details

> 아래 섹션은 프로젝트 시작 시 AI가 채웁니다.
> 각 페이지별 진입/이탈 조건, 상태, API 호출, 엣지 케이스를 상세화합니다.

### Survey 페이지

- **Purpose**: intake_schema.yaml 기반 동적 폼으로 설문 데이터를 입력받는다.
- **Route**: `/`
- **Entry Condition**: 없음 (랜딩 페이지)
- **API Calls**:
  - `POST /intakes` — 폼 제출 시 설문 데이터 저장
- **Completion Condition**: API가 `201 Created` 반환 시 (project_id 수신)
- **Navigation**: 완료 → Generate 페이지 (`/generate/{project_id}`)

**States**

| State | UI 표시 |
|-------|---------|
| idle | 빈 설문 폼 표시, 제출 버튼 활성 |
| loading | 제출 버튼 비활성 + 로딩 인디케이터 |
| success | Generate 페이지로 자동 이동 |
| error | 에러 메시지 표시 (폼 유지), 재시도 가능 |

---

### Generate 페이지

- **Purpose**: 문서 생성을 트리거하고 진행 상태를 표시한다.
- **Route**: `/generate/{project_id}`
- **Entry Condition**: 유효한 project_id가 URL에 존재
- **API Calls**:
  - `POST /generate` — 페이지 진입 시 문서 생성 트리거
- **Completion Condition**: API가 `200 OK` (status: `generated`) 반환 시
- **Navigation**: 완료 → Complete 페이지 (`/complete/{project_id}`)

**States**

| State | UI 표시 |
|-------|---------|
| idle | 생성 시작 대기 (자동 트리거 전 잠시 표시) |
| loading | 문서 생성 중 프로그레스 표시 |
| success | Complete 페이지로 자동 이동 |
| error | 에러 메시지 + 재시도 버튼 표시 |

---

### Complete 페이지

- **Purpose**: 프로젝트 URL 안내 및 ZIP 다운로드 제공
- **Route**: `/complete/{project_id}`
- **Entry Condition**: 유효한 project_id, 프로젝트 status가 `generated`
- **API Calls**:
  - `GET /projects/{project_id}` — 프로젝트 메타 정보 로드
  - `GET /projects/{project_id}/download` — ZIP 다운로드 버튼 클릭 시
- **Completion Condition**: 사용자가 ZIP 다운로드 완료 또는 페이지 이탈
- **Navigation**: 없음 (최종 페이지). "새 프로젝트 시작" 링크 → Survey 페이지

**States**

| State | UI 표시 |
|-------|---------|
| loading | 프로젝트 정보 로딩 중 |
| success | 프로젝트 URL 표시 + ZIP 다운로드 버튼 + URL 복사 버튼 |
| error | 에러 메시지 (프로젝트 조회 실패) |

---

### Edge Cases

| 상황 | 동작 |
|------|------|
| 뒤로가기 (Generate → Survey) | Survey 페이지를 빈 폼으로 표시 (새 설문 시작) |
| 뒤로가기 (Complete → Generate) | Generate 페이지에서 이미 완료 상태 확인 → Complete로 리다이렉트 |
| 네트워크 오류 | 각 페이지의 error 상태 표시, 재시도 버튼 제공 |
| 브라우저 새로고침 | 현재 URL 기반으로 상태 복원 (project_id로 API 재호출) |

### Navigation Rules

| 직접 URL 접근 | 동작 |
|--------------|------|
| `/` | Survey 폼 정상 표시 |
| `/generate/{project_id}` | project_id 유효성 확인 → 유효하면 생성 진행, 무효하면 Survey로 리다이렉트 |
| `/complete/{project_id}` | project_id 조회 → status가 `generated`이면 정상 표시, 아니면 적절한 페이지로 리다이렉트 |
| 존재하지 않는 경로 | Survey 페이지(`/`)로 리다이렉트 |
