# SKILL-{{service_name}}.md

---
name: "{{service_name}}"
type: role
role: mobile-app
doc_range: "{{doc_range}}"
concerns: [testing, deploy]
source_docs:
  - "{{X0}}-mobile-flow.md"
  - "{{X1}}-mobile-verification-e2e.md"
  - "{{X2}}-mobile-verification-accessibility.md"
  - "{{X3}}-mobile-verification-visual.md"
---

{{fixed}}
Service: {{project_name}}
Artifacts: {{source:00-project-profile.md → artifacts}}
Primary Stack: {{detect:tech_stack → mobile}}

Execution Policy:
- Approval Required: true
- Git Flow: {{@integration_branch}}
{{/fixed}}

## Context

- Project: {{project_name}}
- Platform: {{detect:tech_stack → mobile}}
- User flow: {{source:X0-mobile-flow.md → flow_summary}}
{{cross_cutting}}

## Rules

{{generate}}
Extract from mobile flow and requirements:
- Screen navigation rules
- Offline behavior requirements
- API communication patterns
- Platform-specific guidelines
{{/generate}}

## Patterns

{{generate}}
Generate recommended patterns based on {{detect:tech_stack → mobile}}:

1. Project structure
2. Navigation pattern
3. State management
4. API client layer
{{/generate}}

## Anti-patterns

{{generate}}
Mobile-specific anti-patterns:
- Blocking the main/UI thread
- Excessive network calls without caching
- Ignoring platform lifecycle events
- Hardcoded dimensions instead of responsive layout
{{/generate}}

## Checklist

{{checklist:X1-mobile-verification-e2e.md}}
{{checklist:X2-mobile-verification-accessibility.md}}
{{checklist:X3-mobile-verification-visual.md}}

<!-- concern:testing injection point -->
<!-- concern:deploy injection point -->
