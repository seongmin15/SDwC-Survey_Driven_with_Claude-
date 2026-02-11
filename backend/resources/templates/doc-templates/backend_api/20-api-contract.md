# API Contract

> 이 문서는 프로젝트 시작 시 AI가 상세를 채웁니다.

## Overview

- Framework: {{backend.framework}}
- API Style: {{backend.api_style}}
- Auth: {{backend.auth}}

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

{{backend.main_endpoints}}

---

## Endpoint Details

> 아래 섹션은 프로젝트 시작 시 AI가 채웁니다.
> 각 엔드포인트별 Request/Response 스키마, Error cases를 상세화합니다.

<!-- AI:INIT: Based on backend.main_endpoints, fill the following during initialization.
     Per endpoint:
     - Request (body/params/query)
     - Response (status code + body)
     - Errors (status, error_code, condition)
     - Processing Logic (internal steps the endpoint performs, e.g., DB operations, file generation, external API calls, async jobs)
       If an endpoint's processing logic involves multiple complex sub-steps (e.g., template matching + rendering + ZIP packaging),
       list each sub-step explicitly so that task backlog can split them into separate ~30 min tasks.
       When there are ≥5 steps, group them into logical units separated by `---` (e.g., "Validation", "Core Logic", "Persistence").
-->

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
