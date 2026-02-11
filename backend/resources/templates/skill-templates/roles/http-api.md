# SKILL-{{service_name}}.md

---
name: "{{service_name}}"
type: role
role: http-api
doc_range: "{{doc_range}}"
concerns: [testing, deploy, database]
source_docs:
  - "{{X0}}-api-contract.md"
  - "{{X1}}-data-design.md"
  - "{{X2}}-api-verification-contract.md"
  - "{{X3}}-api-verification-integration.md"
  - "{{X4}}-api-verification-security.md"
---

{{fixed}}
Service: {{project_name}}
Artifacts: {{source:00-project-profile.md → artifacts}}
Primary Stack: {{detect:tech_stack → backend}}
Database: {{source:X1-data-design.md → databases}}

Execution Policy:
- Approval Required: true
- Git Flow: {{@integration_branch}}
{{/fixed}}

## Context

- Project: {{project_name}}
- Architecture: {{source:04-architecture.md → architecture_style}}
- Tech stack: {{detect:tech_stack → backend}}
- Endpoints: {{source:X0-api-contract.md → endpoints}}
- DB tables: {{source:X1-data-design.md → tables}}
{{cross_cutting}}

## Rules

{{generate}}
Extract from {{source:X0-api-contract.md}}:
- Request/response rules per endpoint
- HTTP method and status code conventions
- Error response format

Extract from {{source:X1-data-design.md}}:
- Table relationships and integrity constraints
- Required fields and constraints

Extract from {{source:03-requirements.md}}: service-specific requirements
{{/generate}}

<!-- concern:database injection point -->

## Patterns

{{generate}}
Generate recommended patterns based on {{detect:tech_stack → backend}}:

1. Directory structure
   - Layer separation criteria and file placement

2. Error handling
   - Error response format and status code mapping

3. Input validation
   - Request schema definition approach

4. Database access
   - Repository pattern and transaction handling

{{#if architecture.internal_style == hexagonal}}
_hint (Hexagonal Architecture):_
- Separate into Domain / Application / Adapter layers
- Domain layer: entities, value objects, repository interfaces (ports)
- Application layer: use cases (application services) orchestrating domain logic
- Adapter layer: framework-specific implementations (FastAPI routes, SQLAlchemy repos, etc.)
- Dependency rule: outer layers depend on inner layers, never the reverse
- Use dependency injection to wire adapters to ports
{{/if}}

{{#if architecture.internal_style == layered}}
_hint (Layered Architecture):_
- Router/Controller → Service → Repository separation
{{/if}}

_hint (FastAPI):_
- Pydantic models for request/response definition
- HTTPException + consistent error response structure
- AsyncSession-based async DB access
- Dependency Injection for service/repository wiring

_hint (Express):_
- Controller → Service → Repository separation
- Zod or Joi for input validation
- Common error handling middleware
- Prisma or TypeORM for DB access

_hint (Spring Boot):_
- Controller → Service → Repository separation
- Jakarta Validation for input validation
- @ControllerAdvice for global error handling
- Spring Data JPA for DB access
{{/generate}}

## Anti-patterns

{{generate}}
Generate anti-patterns based on {{detect:tech_stack → backend}}:
- Direct DB access from route handlers (bypass service layer)
- Missing input validation
- Swallowing exceptions without logging
- Hardcoded configuration values
- N+1 query patterns
{{/generate}}

<!-- concern:database anti-pattern injection point -->

## Checklist

{{checklist:X2-api-verification-contract.md}}

{{checklist:X3-api-verification-integration.md}}

{{checklist:X4-api-verification-security.md}}

<!-- concern:testing injection point -->
<!-- concern:deploy injection point -->
