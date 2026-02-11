# API Verification — Security

> API의 보안 관련 항목을 검증합니다.
> 이 문서는 프로젝트 시작 시 AI가 채웁니다.

## Auth Policy

- Auth: {{backend.auth}}

## Verification Scope

> **ID Convention**: Use `S-NNN` (e.g., S-001, S-002). Each test case MUST have a unique ID.

<!-- AI:INIT: Based on 20-api-contract.md and auth policy,
     write security test cases for:
     - Input validation (SQL injection, payload size, JSON format)
     - Information exposure (stack trace, DB error, secret leakage)
     - Environment security (hardcoding, Docker image, logs, .gitignore)
     - Auth (based on auth method)
-->

## Automated Test Location

```
tests/security/
```
