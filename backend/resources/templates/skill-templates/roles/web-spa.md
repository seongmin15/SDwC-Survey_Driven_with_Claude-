# SKILL-{{service_name}}.md

---
name: "{{service_name}}"
type: role
role: web-spa
doc_range: "{{doc_range}}"
concerns: [testing, deploy]
source_docs:
  - "{{X0}}-user-flow.md"
  - "{{X1}}-ui-verification-e2e.md"
  - "{{X2}}-ui-verification-accessibility.md"
  - "{{X3}}-ui-verification-visual.md"
---

{{fixed}}
Service: {{project_name}}
Artifacts: {{source:00-project-profile.md → artifacts}}
Primary Stack: {{detect:tech_stack → frontend}}

Execution Policy:
- Approval Required: true
- Git Flow: {{@integration_branch}}
{{/fixed}}

## Context

- Project: {{project_name}}
- UI framework: {{detect:tech_stack → frontend}}
- User flow: {{source:X0-user-flow.md → flow_summary}}
{{cross_cutting}}

## Rules

{{generate}}
Extract from {{source:X0-user-flow.md}}:
- Page list and transition rules
- Entry/exit conditions per page
- User interaction flow

Extract from {{source:03-requirements.md}}: service-specific requirements
{{/generate}}

## Patterns

{{generate}}
Generate recommended patterns based on {{detect:tech_stack → frontend}}:

1. Directory structure
   - Page, component, hook/composable separation criteria

2. State management
   - Server state vs local state separation

3. API communication
   - API client layer structure

4. Form handling
   - Validation and error display

_hint (React):_
- pages/ → components/ → hooks/ → api/ separation
- React Query for server state, useState/useReducer for local state
- fetch wrapper or axios instance for API client isolation
- Per-page states: idle | loading | success | error

_hint (Vue):_
- views/ → components/ → composables/ → api/ separation
- Pinia for global state, ref/reactive for local state
- Centralized Axios instance management
- v-if for state-based UI branching

_hint (Next.js):_
- app/ directory-based routing
- Server Components vs Client Components separation
- Route Handlers for API proxy
- loading.tsx, error.tsx for state handling
{{/generate}}

## Anti-patterns

{{generate}}
Generate anti-patterns based on {{detect:tech_stack → frontend}}:
- Direct API calls from components (bypass API client layer)
- Global state for local-only data
- Missing loading/error states
- Hardcoded API URLs
- Uncontrolled form inputs
{{/generate}}

## Checklist

{{checklist:X1-ui-verification-e2e.md}}

{{checklist:X2-ui-verification-accessibility.md}}

{{checklist:X3-ui-verification-visual.md}}

<!-- concern:testing injection point -->
<!-- concern:deploy injection point -->
