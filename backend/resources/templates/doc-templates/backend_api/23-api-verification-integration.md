# API Verification — Integration

> API와 데이터베이스 간 통합이 정상 동작하는지 검증합니다.
> 이 문서는 프로젝트 시작 시 20-api-contract.md, 21-data-design.md 기반으로 AI가 채웁니다.

## Verification Scope

> **ID Convention**: Use `I-NNN` (e.g., I-001, I-002). Each test case MUST have a unique ID.

<!-- AI:INIT: After 20-api-contract.md and 21-data-design.md are filled,
     write integration test cases for:
     - DB connection verification
     - Endpoint → DB data flow verification
     - Transaction integrity verification
     - Cross-service data flow (if applicable)
-->

## Automated Test Location

```
tests/integration/
```
