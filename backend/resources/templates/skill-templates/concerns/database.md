# Concern: Database

---
type: concern
name: database
condition: "databases[] is not empty"
inject_into:
  - section: Rules
  - section: Anti-patterns
description: Injects database rules into service skills that use a database.
---

## Rules Injection

{{generate}}
Based on {{detect:tech_stack → database}}:
- Connection pool configuration rules
- Query timeout rules
- N+1 query prevention rules
- Migration execution rules (always up/down, approval for destructive changes)
- Transaction boundary rules
{{/generate}}

## Anti-patterns Injection

{{generate}}
Based on {{detect:tech_stack → database}}:
- Raw SQL in application code (bypass ORM/query builder)
- Missing database indexes on frequently queried columns
- Unbounded queries without pagination
- Storing secrets in database without encryption
{{/generate}}
