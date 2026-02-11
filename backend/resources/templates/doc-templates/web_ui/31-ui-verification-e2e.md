# UI Verification — E2E

> 사용자 플로우 전체가 end-to-end로 동작하는지 검증합니다.
> 이 문서는 프로젝트 시작 시 30-user-flow.md 기반으로 AI가 채웁니다.

## Verification Scope

> **ID Convention**: Use `E-NNN` (e.g., E-001, E-002). Each test case MUST have a unique ID.

<!-- AI:INIT: After Page Details in 30-user-flow.md are filled,
     write e2e test cases for:
     - Happy path (full flow)
     - Validation (missing required, invalid format)
     - Error handling (API timeout, network failure)
     - Navigation (direct URL, back/forward)
     - Re-entry (leave and return)
-->

## Automated Test Location

```
tests/e2e/
```
