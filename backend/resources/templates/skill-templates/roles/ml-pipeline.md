# SKILL-{{service_name}}.md

---
name: "{{service_name}}"
type: role
role: ml-pipeline
doc_range: "{{doc_range}}"
concerns: [testing, deploy, database]
source_docs:
  - "{{X0}}-pipeline-contract.md"
  - "{{X1}}-pipeline-data-design.md"
  - "{{X2}}-pipeline-verification.md"
---

{{fixed}}
Service: {{project_name}}
Artifacts: {{source:00-project-profile.md → artifacts}}
Primary Stack: {{detect:tech_stack → pipeline}}

Execution Policy:
- Approval Required: true
- Git Flow: {{@integration_branch}}
{{/fixed}}

## Context

- Project: {{project_name}}
- Architecture: {{source:04-architecture.md → architecture_style}}
- Tech stack: {{detect:tech_stack → pipeline}}
{{cross_cutting}}

## Rules

{{generate}}
Extract from pipeline contract and requirements:
- Data source and sink definitions
- Schedule and trigger rules
- Data quality validation rules
- Idempotency and reprocessing policies
{{/generate}}

<!-- concern:database injection point -->

## Patterns

{{generate}}
Generate recommended patterns based on {{detect:tech_stack → pipeline}}:

1. DAG/workflow structure
2. Data validation layer
3. Error handling and alerting
4. Backfill strategy
{{/generate}}

## Anti-patterns

{{generate}}
Pipeline-specific anti-patterns:
- Hardcoded file paths or connection strings
- Missing data validation between stages
- No idempotency (re-runs produce duplicates)
- Unbounded memory usage in data transformations
{{/generate}}

<!-- concern:database anti-pattern injection point -->

## Checklist

{{checklist:X2-pipeline-verification.md}}

<!-- concern:testing injection point -->
<!-- concern:deploy injection point -->
