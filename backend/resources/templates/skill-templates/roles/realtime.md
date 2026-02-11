# SKILL-{{service_name}}.md

---
name: "{{service_name}}"
type: role
role: realtime
doc_range: "{{doc_range}}"
concerns: [testing, deploy]
source_docs:
  - "{{X0}}-realtime-contract.md"
  - "{{X1}}-realtime-verification.md"
---

{{fixed}}
Service: {{project_name}}
Artifacts: {{source:00-project-profile.md → artifacts}}
Primary Stack: {{detect:tech_stack → realtime}}

Execution Policy:
- Approval Required: true
- Git Flow: {{@integration_branch}}
{{/fixed}}

## Context

- Project: {{project_name}}
- Tech stack: {{detect:tech_stack → realtime}}
- Protocol: {{source:X0-realtime-contract.md → protocol}}
{{cross_cutting}}

## Rules

{{generate}}
Extract from realtime contract:
- Connection lifecycle (connect, reconnect, disconnect)
- Message format and channel definitions
- Authentication for WebSocket/SSE connections
- Rate limiting and backpressure rules
{{/generate}}

## Patterns

{{generate}}
Generate recommended patterns for realtime services:

1. Connection management (heartbeat, reconnection)
2. Message serialization and validation
3. Room/channel architecture
4. Error handling and graceful degradation
{{/generate}}

## Anti-patterns

{{generate}}
Realtime-specific anti-patterns:
- No reconnection strategy
- Unbounded message queues per connection
- Missing heartbeat/ping-pong
- Broadcasting without channel isolation
{{/generate}}

## Checklist

{{checklist:X1-realtime-verification.md}}

<!-- concern:testing injection point -->
<!-- concern:deploy injection point -->
