# Concern: Auth

---
type: concern
name: auth
condition: "auth != none"
inject_into:
  - section: Rules
description: Injects authentication/authorization rules into service skills. Only activated when auth is not 'none'.
---

## Rules Injection

{{generate}}
Extract from auth-related docs:
- Authentication method (JWT, session, OAuth, etc.)
- Authorization model (RBAC, ABAC, etc.)
- Protected endpoints/pages list
- Token management rules (refresh, expiration, storage)
- Authentication failure behavior (redirect, error response)
- Role-based access control matrix
{{/generate}}
