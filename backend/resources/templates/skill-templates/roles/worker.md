# SKILL-{{service_name}}.md

---
name: "{{service_name}}"
type: role
role: worker
doc_range: "{{doc_range}}"
concerns: [testing, deploy, database]
source_docs:
  - "{{X0}}-worker-contract.md"
  - "{{X1}}-worker-data-design.md"
  - "{{X2}}-worker-verification-contract.md"
  - "{{X3}}-worker-verification-integration.md"
---

{{fixed}}
Service: {{project_name}}
Artifacts: {{source:00-project-profile.md → artifacts}}
Primary Stack: {{detect:tech_stack → worker}}

Execution Policy:
- Approval Required: true
- Git Flow: {{@integration_branch}}
{{/fixed}}

## Context

- Project: {{project_name}}
- Architecture: {{source:04-architecture.md → architecture_style}}
- Tech stack: {{detect:tech_stack → worker}}
- Queue system: {{source:worker_config → queue_system}}
{{cross_cutting}}

## Rules

{{generate}}
Extract from worker contract and requirements:
- Message format and serialization rules
- Retry and dead-letter queue policies
- Idempotency requirements
- Concurrency and ordering guarantees
{{/generate}}

<!-- concern:database injection point -->

## Patterns

{{generate}}
Generate recommended patterns based on {{detect:tech_stack → worker}}:

1. Directory structure
2. Message handler pattern
3. Error handling and retry logic
4. Graceful shutdown

{{#if architecture.internal_style == hexagonal}}
_hint (Hexagonal Architecture):_
- Separate message handlers (adapters) from business logic (domain/ports)
- Queue consumer is an inbound adapter; external calls are outbound adapters
{{/if}}
{{/generate}}

## Anti-patterns

{{generate}}
Worker-specific anti-patterns:
- Unbounded message processing without backpressure
- Missing idempotency checks
- Swallowing errors without dead-letter routing
- Blocking the event loop in async workers
{{/generate}}

<!-- concern:database anti-pattern injection point -->

## Checklist

{{checklist:X2-worker-verification-contract.md}}
{{checklist:X3-worker-verification-integration.md}}

<!-- concern:testing injection point -->
<!-- concern:deploy injection point -->
