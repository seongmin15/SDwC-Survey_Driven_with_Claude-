Service: sdwc
Artifacts: backend_api, web_ui
Primary Stack: Python / FastAPI / Poetry
Database: PostgreSQL (primary)

Execution Policy:
- Approval Required: true
- Git Flow: develop

## Context

- Project: sdwc
- Architecture: monolith, hexagonal internal style
- Tech stack: Python 3.12+ / FastAPI / SQLAlchemy / Poetry
- Endpoints: POST /intakes, POST /generate, GET /projects/:id, GET /projects/:id/download, GET /health, GET /ready
- DB tables: projects, events
- Deployment: Docker Compose
- Observability: structured JSON logging, /health + /ready endpoints

## Rules

### API Contract Rules

- POST /intakes: accepts intake_data (JSONB), returns 201 with project_id
- POST /generate: accepts project_id, triggers document generation, returns 200 with status
- GET /projects/:id: returns project metadata
- GET /projects/:id/download: returns ZIP file stream (application/zip)
- Success response format: `{ "data": { ... } }`
- Error response format: `{ "error": "<code>", "message": "<text>" }`
- All UUIDs validated before DB query

### Data Rules

- projects table: id (UUID PK), project_name, status, intake_data (JSONB), zip_path, created_at, generated_at
- events table: id (UUID PK), project_id (FK → projects.id ON DELETE CASCADE), event_type, payload (JSONB), created_at
- Status constraint: intake_saved | generated
- Transaction: projects + events writes must be atomic

### Database Rules

- Use connection pooling (SQLAlchemy AsyncSession)
- Set query timeouts to prevent long-running queries
- Prevent N+1 queries — use eager loading or explicit joins where needed
- All migrations must have up/down scripts; destructive migrations require approval
- Transaction boundaries: one transaction per use case execution

## Patterns

### 1. Directory Structure (Hexagonal)

```
backend/
├── src/
│   ├── domain/           # Entities, value objects, port interfaces
│   │   ├── entities/
│   │   ├── ports/        # Repository interfaces, service interfaces
│   │   └── values/
│   ├── application/      # Use cases (application services)
│   │   └── usecases/
│   ├── adapters/         # Framework-specific implementations
│   │   ├── api/          # FastAPI routers, request/response models
│   │   ├── persistence/  # SQLAlchemy repository implementations
│   │   └── services/     # Template engine, ZIP packager implementations
│   └── config/           # Settings, dependency injection wiring
├── tests/
│   ├── contract/
│   ├── integration/
│   └── security/
├── migrations/
├── pyproject.toml
└── Dockerfile
```

### 2. Error Handling

- Define domain exceptions (ProjectNotFound, AlreadyGenerated, etc.)
- Map domain exceptions to HTTP status codes in adapter layer
- Use FastAPI exception handlers for consistent error response format

### 3. Input Validation

- Pydantic models for all request/response schemas
- Validate at adapter boundary; domain layer receives validated data

### 4. Database Access

- Repository pattern: port interfaces in domain, SQLAlchemy implementations in adapters
- AsyncSession-based async DB access
- Dependency Injection via FastAPI Depends() to wire adapters to ports

## Anti-patterns

- Direct DB access from route handlers (must go through use case → repository)
- Domain layer importing FastAPI or SQLAlchemy modules
- Missing input validation on request models
- Swallowing exceptions without logging
- Hardcoded configuration values (use environment variables)
- N+1 query patterns — always check query count
- Raw SQL in application code (use SQLAlchemy ORM/Core)
- Missing database indexes on frequently queried columns
- Unbounded queries without pagination
- Storing secrets in database without encryption

## Checklist

### Contract Verification (C-001 ~ C-024)

- [ ] C-001~C-006: POST /intakes contract tests pass
- [ ] C-007~C-011: POST /generate contract tests pass
- [ ] C-012~C-014: GET /projects/:id contract tests pass
- [ ] C-015~C-018: GET /projects/:id/download contract tests pass
- [ ] C-019~C-020: Response format validation tests pass
- [ ] C-021~C-022: Hexagonal architecture structure tests pass
- [ ] C-023~C-024: Health/ready endpoint tests pass

### Integration Verification (I-001 ~ I-012)

- [ ] I-001~I-002: DB connection tests pass
- [ ] I-003~I-005: POST /intakes → DB flow tests pass
- [ ] I-006~I-009: POST /generate → DB flow tests pass
- [ ] I-010: GET /projects/:id → DB flow test passes
- [ ] I-011~I-012: Transaction integrity tests pass

### Security Verification (S-001 ~ S-012)

- [ ] S-001~S-005: Input validation security tests pass
- [ ] S-006~S-008: Information exposure tests pass
- [ ] S-009~S-012: Environment security tests pass

### Testing

- [ ] pytest execution passes with no failures
- [ ] TDD cycle: test committed before implementation
- [ ] All verification IDs covered by automated tests

### Deployment

- [ ] Docker image builds successfully
- [ ] Environment variables configured (no hardcoded secrets)
- [ ] /health and /ready endpoints responding
- [ ] Structured JSON logging with correct fields
- [ ] No secrets or PII in logs
