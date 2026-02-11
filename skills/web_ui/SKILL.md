Service: sdwc
Artifacts: backend_api, web_ui
Primary Stack: TypeScript / React / Tailwind / pnpm

Execution Policy:
- Approval Required: true
- Git Flow: develop

## Context

- Project: sdwc
- UI framework: TypeScript / React / Tailwind CSS
- User flow: Survey → Generate → Complete (URL copy / ZIP download)
- Deployment: Docker Compose (same_server as backend_api)
- Observability: /health + /ready endpoints

## Rules

### Page Rules

- **Survey** (`/`): landing page, dynamic form based on intake_schema.yaml, calls POST /intakes on submit
- **Generate** (`/generate/{project_id}`): auto-triggers POST /generate on entry, shows progress
- **Complete** (`/complete/{project_id}`): displays project URL, ZIP download button, URL copy button
- Flow: Survey → Generate → Complete; no skipping steps
- Entry conditions enforced: invalid/missing project_id redirects to Survey
- Direct URL access: validate project state and redirect accordingly
- All pages must handle 4 states: idle, loading, success, error

### Navigation Rules

- Back button (Generate → Survey): show fresh empty form
- Back button (Complete → Generate): redirect to Complete if already generated
- Unknown routes: redirect to Survey (`/`)
- Browser refresh: restore state from URL (project_id) via API re-call

## Patterns

### 1. Directory Structure

```
frontend/
├── src/
│   ├── pages/          # Survey, Generate, Complete page components
│   ├── components/     # Shared UI components (Layout, ErrorMessage, LoadingSpinner)
│   ├── hooks/          # Custom hooks (useApi, useProject)
│   ├── api/            # API client layer (fetch wrapper)
│   ├── types/          # TypeScript type definitions
│   └── utils/          # Helper functions
├── public/
├── tests/
│   └── e2e/
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── vite.config.ts
└── Dockerfile
```

### 2. State Management

- Server state: React Query (TanStack Query) for API data fetching and caching
- Local state: useState/useReducer for form state and UI state
- No global state store needed for MVP (3 pages, linear flow)

### 3. API Communication

- Centralized API client in `api/` directory
- Base URL from environment variable (API_URL)
- Consistent error handling: catch API errors → return typed error objects

### 4. Form Handling

- Dynamic form generation based on intake_schema.yaml structure
- Client-side validation before API submission
- Error display per field with aria-describedby linkage

## Anti-patterns

- Direct API calls from page components (must use api/ client layer)
- Global state for local-only data (form inputs, loading flags)
- Missing loading/error states on any page
- Hardcoded API URLs (must use environment variable)
- Uncontrolled form inputs (use controlled components)
- Ignoring accessibility (missing labels, aria attributes, focus management)

## Checklist

### E2E Verification (E-001 ~ E-015)

- [ ] E-001~E-003: Happy path full flow tests pass
- [ ] E-004~E-005: Form validation tests pass
- [ ] E-006~E-009: Error handling tests pass
- [ ] E-010~E-013: Navigation tests pass
- [ ] E-014~E-015: Re-entry tests pass

### Accessibility Verification (A-001 ~ A-017)

- [ ] A-001~A-007: Survey page accessibility tests pass
- [ ] A-008~A-010: Generate page accessibility tests pass
- [ ] A-011~A-013: Complete page accessibility tests pass
- [ ] A-014~A-016: Color & contrast tests pass
- [ ] A-017: Focus indicator test passes

### Visual Verification (V-001 ~ V-016)

- [ ] V-001~V-006: Survey page visual tests pass
- [ ] V-007~V-008: Generate page visual tests pass
- [ ] V-009~V-010: Complete page visual tests pass
- [ ] V-011~V-012: Layout consistency tests pass
- [ ] V-013~V-016: Browser compatibility tests pass

### Testing

- [ ] Test runner execution passes with no failures
- [ ] TDD cycle: test committed before implementation
- [ ] All verification IDs covered by automated tests

### Deployment

- [ ] Docker image builds successfully
- [ ] Environment variables configured (API_URL set)
- [ ] /health and /ready endpoints responding
- [ ] No secrets or PII in logs
