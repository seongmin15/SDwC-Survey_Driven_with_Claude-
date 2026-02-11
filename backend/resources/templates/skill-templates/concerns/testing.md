# Concern: Testing

---
type: concern
name: testing
condition: always
inject_into:
  - section: Checklist
description: Injects testing checklist items into service skills.
---

## Checklist Injection

{{generate}}
Based on {{detect:tech_stack}}:
- Test framework execution command for the detected stack
- Coverage threshold compliance (if defined)
- Mock/stub alignment with actual dependencies
- TDD cycle compliance: test committed before implementation
- All verification IDs (C-/I-/S-/E-/A-/V-) covered by tests
{{/generate}}
