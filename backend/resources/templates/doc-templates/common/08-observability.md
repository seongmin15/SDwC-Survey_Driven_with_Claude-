# Observability

## MVP Inclusion

{{#if observability.included_in_mvp}}
Observability가 MVP에 포함됩니다.
{{else}}
MVP에서는 최소 수준만 포함합니다 (health/ready, structured logging).
{{/if}}

{{#if observability.included_in_mvp}}
## Tool Stack

| Category | Tool |
|----------|------|
| Logging | {{observability.logging}} |
| Metrics | {{observability.metrics}} |
| Tracing | {{#if observability.tracing}}포함{{else}}미포함 (향후 추가 가능){{/if}} |
{{/if}}

## Health Endpoints

| Service | Endpoint | Purpose |
|---------|----------|---------|
{{#each services}}
| {{this}} | /health | Liveness check |
| {{this}} | /ready | Readiness check |
{{/each}}

## Structured Logging

- Format: JSON
- Fields: timestamp, level, service, message{{#if observability.tracing}}, trace_id{{/if}}
- Levels: DEBUG, INFO, WARN, ERROR
{{#if observability.included_in_mvp}}
- Tool: {{observability.logging}}
{{/if}}

### Rules

- 요청/응답 로그: INFO
- 에러: ERROR + stack trace
- 시크릿/개인정보: 절대 로그에 포함하지 않음

{{#if observability.included_in_mvp}}
{{#if observability.metrics != none}}
## Metrics

- Tool: {{observability.metrics}}

### 기본 메트릭

- 요청 수 (request count)
- 응답 시간 (response latency)
- 에러율 (error rate)
- JVM/프로세스 메트릭 (해당 시)

<!-- AI:ONGOING: Add application-specific metrics during development -->
{{/if}}

{{#if observability.tracing}}
## Distributed Tracing

- trace_id를 모든 요청/이벤트에 전파합니다.
- 서비스 간 호출 시 trace_id를 헤더로 전달합니다.
- 로그에 trace_id를 포함하여 요청 흐름을 추적할 수 있게 합니다.

<!-- AI:INIT: Define trace propagation strategy during initialization -->
{{/if}}
{{/if}}
