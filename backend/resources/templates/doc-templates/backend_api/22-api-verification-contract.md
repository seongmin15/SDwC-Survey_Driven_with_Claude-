# API Verification — Contract

> API 엔드포인트가 `docs/20-api-contract.md`에 정의된 계약을 준수하는지 검증합니다.
> 이 문서는 프로젝트 시작 시 20-api-contract.md 기반으로 AI가 채웁니다.

## Verification Scope

> **ID Convention**: Use `C-NNN` (e.g., C-001, C-002). Each test case MUST have a unique ID.

<!-- AI:INIT: After Endpoint Details in 20-api-contract.md are filled,
     write contract test cases per endpoint.
     Include:
     - Expected response for valid input
     - Error for missing required fields
     - Error for invalid format
     - Error response format validation
     - If internal_style is defined (e.g., hexagonal, clean), add structure verification cases:
       domain layer must not import framework-specific modules, dependency direction must be inward-only.
-->

## Automated Test Location

```
tests/contract/
```
