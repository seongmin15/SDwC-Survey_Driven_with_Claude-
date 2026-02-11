# Observability

## MVP Inclusion

MVP에서는 최소 수준만 포함합니다 (health/ready, structured logging).

## Health Endpoints

| Service | Endpoint | Purpose |
|---------|----------|---------|
| backend_api | /health | Liveness check |
| backend_api | /ready | Readiness check |
| web_ui | /health | Liveness check |
| web_ui | /ready | Readiness check |

## Structured Logging

- Format: JSON
- Fields: timestamp, level, service, message
- Levels: DEBUG, INFO, WARN, ERROR

### Rules

- 요청/응답 로그: INFO
- 에러: ERROR + stack trace
- 시크릿/개인정보: 절대 로그에 포함하지 않음

