# Concern: Deploy

---
type: concern
name: deploy
condition: always
inject_into:
  - section: Checklist
description: Injects deployment and infrastructure checklist items into service skills.
---

## Checklist Injection

{{generate}}
Based on {{source:07-deployment.md}}:
- Build artifact generation verified
- Environment variables configured (no hardcoded secrets)
- Health check endpoints responding
- Docker image builds successfully (if applicable)

Based on {{source:08-observability.md}}:
- Structured logging format and level rules
- Metrics collection configuration verified
- No secrets or PII in logs
{{/generate}}
