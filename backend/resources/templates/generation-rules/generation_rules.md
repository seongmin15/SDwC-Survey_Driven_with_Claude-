# Generation Rules

> Rules the server follows when generating a project ZIP from intake data.

## 1. Input

- Survey response data conforming to `intake_schema.yaml`.

## 2. Architecture Branch

| Condition | Service Data Structure |
|-----------|----------------------|
| `architecture.pattern != microservice` | `services[]` (type list) + shared config (`backend.*`, `worker.*`, `web.*`) |
| `architecture.pattern == microservice` | `service_list[]` (individual name + type + config per service) |

## 3. Document Generation

### 3.1 Common Documents (always generated)

| Template | Output |
|----------|--------|
| `common/00-project-profile.md` | `docs/00-project-profile.md` |
| `common/00-collaboration-model.md` | `docs/00-collaboration-model.md` |
| `common/01-opportunity.md` | `docs/01-opportunity.md` |
| `common/02-mvp.md` | `docs/02-mvp.md` |
| `common/03-requirements.md` | `docs/03-requirements.md` |
| `common/04-architecture.md` | `docs/04-architecture.md` |
| `common/05-git-workflow.md` | `docs/05-git-workflow.md` |
| `common/06-decisions.md` | `docs/06-decisions.md` |
| `common/07-deployment.md` | `docs/07-deployment.md` |
| `common/08-observability.md` | `docs/08-observability.md` |
| `common/09-task-backlog.md` | `docs/09-task-backlog.md` |
| `common/999-roadmap-extensions.md` | `docs/999-roadmap-extensions.md` |

### 3.1.1 Common Conditional Documents (10-series)

These documents are generated based on `deployment.initial` value, not `services[]`.

| Condition | Template | Output |
|-----------|----------|--------|
| `deployment.initial == docker_compose` | `common/10-docker-compose-template.md` | `docs/10-docker-compose-template.md` |

> **Extension point**: Future deployment targets (k8s, ecs, etc.) follow the same pattern:
> `deployment.initial == {target}` → `common/1N-{target}-template.md` → `docs/1N-{target}-template.md`

### 3.2 Non-MSA — Per-Service Documents

| Condition | Templates | Output |
|-----------|----------|--------|
| `services contains backend_api` | `backend_api/20-*` | `docs/20~24-*.md` |
| `services contains backend_api AND backend.databases is not empty` | `backend_api/21-*` | `docs/21-data-design.md` |
| `services contains web_ui` | `web_ui/30-*` | `docs/30~33-*.md` |
| `services contains worker` | `worker/40-*` | `docs/40~43-*.md` |
| `services contains mobile_app` | `mobile_app/50-*` | `docs/50~53-*.md` |
| `services contains data_pipeline` | `data_pipeline/60-*` | `docs/60~63-*.md` |

### 3.3 MSA — Per-Service Documents

For MSA, generate individual documents for each service in `service_list`.

**Backend API type services:**

| Template | Output |
|----------|--------|
| `backend_api/20-api-contract.md` | `docs/services/{service.name}/20-api-contract.md` |
| `backend_api/21-data-design.md` | `docs/services/{service.name}/21-data-design.md` (when databases not empty) |
| `backend_api/22-api-verification-contract.md` | `docs/services/{service.name}/22-api-verification-contract.md` |
| `backend_api/23-api-verification-integration.md` | `docs/services/{service.name}/23-api-verification-integration.md` |
| `backend_api/24-api-verification-security.md` | `docs/services/{service.name}/24-api-verification-security.md` |

**Web UI type services:**

| Template | Output |
|----------|--------|
| `web_ui/30-user-flow.md` | `docs/services/{service.name}/30-user-flow.md` |
| `web_ui/31~33-*.md` | `docs/services/{service.name}/31~33-*.md` |

**Worker type services:**

| Template | Output |
|----------|--------|
| `worker/40-worker-design.md` | `docs/services/{service.name}/40-worker-design.md` |
| `worker/41-worker-data-flow.md` | `docs/services/{service.name}/41-worker-data-flow.md` |
| `worker/42-worker-verification-reliability.md` | `docs/services/{service.name}/42-worker-verification-reliability.md` |
| `worker/43-worker-verification-performance.md` | `docs/services/{service.name}/43-worker-verification-performance.md` |

**Mobile App type services:**

| Template | Output |
|----------|--------|
| `mobile_app/50-app-design.md` | `docs/services/{service.name}/50-app-design.md` |
| `mobile_app/51-app-data.md` | `docs/services/{service.name}/51-app-data.md` |
| `mobile_app/52-app-verification-e2e.md` | `docs/services/{service.name}/52-app-verification-e2e.md` |
| `mobile_app/53-app-verification-platform.md` | `docs/services/{service.name}/53-app-verification-platform.md` |

**Data Pipeline type services:**

| Template | Output |
|----------|--------|
| `data_pipeline/60-pipeline-design.md` | `docs/services/{service.name}/60-pipeline-design.md` |
| `data_pipeline/61-pipeline-data-schema.md` | `docs/services/{service.name}/61-pipeline-data-schema.md` |
| `data_pipeline/62-pipeline-verification-quality.md` | `docs/services/{service.name}/62-pipeline-verification-quality.md` |
| `data_pipeline/63-pipeline-verification-performance.md` | `docs/services/{service.name}/63-pipeline-verification-performance.md` |

### 3.4 MSA Variable Mapping

Map template variables to per-service data:

| Template Variable | MSA Mapping |
|------------------|-------------|
| `{{backend.build_tool}}` | `{{service.build_tool}}` |
| `{{backend.build_tool_reason}}` | `{{service.build_tool_reason}}` |
| `{{backend.language}}` | `{{service.language}}` |
| `{{backend.framework}}` | `{{service.framework}}` |
| `{{backend.framework_reason}}` | `{{service.framework_reason}}` |
| `{{#each backend.databases}}` | `{{#each service.databases}}` |
| `{{backend.api_style}}` | `{{service.api_style}}` |
| `{{backend.auth}}` | `{{service.auth}}` |
| `{{backend.deploy_target}}` | `{{service.deploy_target}}` |
| `{{web.language}}` | `{{service.web_language}}` |
| `{{web.framework}}` | `{{service.web_framework}}` |
| `{{web.build_tool}}` | `{{service.web_build_tool}}` |
| `{{web.deploy_target}}` | `{{service.web_deploy_target}}` |
| `{{worker.language}}` | `{{service.worker_language}}` |
| `{{worker.deploy_target}}` | `{{service.worker_deploy_target}}` |
| `{{worker.queue_system}}` | `{{service.worker_queue_system}}` |
| `{{worker.build_tool}}` | `{{service.worker_build_tool}}` |
| `{{mobile.platform}}` | `{{service.mobile_platform}}` |
| `{{mobile.language}}` | `{{service.mobile_language}}` |
| `{{mobile.framework}}` | `{{service.mobile_framework}}` |
| `{{mobile.deploy_target}}` | `{{service.mobile_deploy_target}}` |
| `{{mobile.build_tool}}` | `{{service.mobile_build_tool}}` |
| `{{pipeline.language}}` | `{{service.pipeline_language}}` |
| `{{pipeline.framework}}` | `{{service.pipeline_framework}}` |
| `{{pipeline.deploy_target}}` | `{{service.pipeline_deploy_target}}` |
| `{{pipeline.build_tool}}` | `{{service.pipeline_build_tool}}` |

## 4. CLAUDE.md Generation

- Copy `CLAUDE_BASE.md` to `CLAUDE.md`.
- Evaluate all conditional blocks:
  - `{{#if collaboration.use_subagent}}` — Sub-Agent Policy section
  - `{{#if collaboration.model_routing == opus_sonnet}}` — Model Routing section
  - `{{#if collaboration.tdd}}` — TDD Policy section
  - `{{#if collaboration.methodology == scrum}}` — Sprint Policy section
  - `{{#if git.branch_strategy == main_feature}}` / `{{#if git.branch_strategy == master_develop_task}}` — Branch-specific workflow in Task Execution and Project Initialization
  - `{{#if git.pr_by == ai}}` — PR auto-creation in Post-Task Completion (within each branch strategy block)
  - `{{#if git.pr_by == ai}}` — PR auto-creation in Post-Task Completion (within each branch strategy block)

## 5. Skill Templates

- Copy `skill-templates/` to `.sdwc/skill-templates/` as-is.
- Save the resolved intake data (user's survey responses) to `docs/intake_data.yaml`.
  This preserves the original survey answers for reference and future migration.
  - List fields (e.g., `scope.in_scope`) are stored as YAML arrays. Each item is an independent scope entry.
  - Multi-line string fields (e.g., `scope.out_of_scope`, `scope.success_criteria`) MUST use YAML block scalar style (`|`) instead of inline `\n` escapes.
  - List-formatted text fields SHOULD be stored as YAML arrays when each item is independent.

## 6. Variable Substitution

### 6.1 Simple

```
{{field.name}} → value from intake data
```

### 6.2 Conditional Blocks

```
{{#if field}}...{{/if}}
{{#if field == value}}...{{/if}}
{{#if field != value}}...{{/if}}
{{#if field is not empty}}...{{/if}}
```

### 6.3 Iteration

```
{{#each list}}{{this}}{{/each}}
{{#each services}}...{{/each}} → Non-MSA: iterate type list
{{#each service_list}}...{{/each}} → MSA: iterate service instances
{{#each backend.databases}}...{{/each}} → Non-MSA: iterate DB entries
{{#each service.databases}}...{{/each}} → MSA: iterate per-service DB entries
```

### 6.4 HTML Comments (no substitution)

```
<!-- AI:INIT: ... --> → preserved as-is (Claude fills during Project Initialization Step 2)
<!-- AI:ONGOING: ... --> → preserved as-is (Claude fills during development, NOT during init)
```

> **Convention**: All AI comments in doc-templates MUST use one of these two prefixes.
> - `AI:INIT:` — Claude **replaces** the entire comment block with generated content during initialization (Step 2).
> - `AI:ONGOING:` — never filled during initialization; Claude updates these as development progresses.

### 6.5 Post-Processing Normalization

After all substitution is complete, the following normalizations are applied:
- HTTP method spacing: `GET  /path` (multiple spaces) → `GET /path` (single space). Applies to GET, POST, PUT, DELETE, PATCH.

### 6.6 Special Variables

```
{{@adr_number}} → auto-incrementing ADR number
{{@next_adr}} → next available ADR number after all auto-generated entries
{{@integration_branch}} → "develop" (master_develop_task) or "main" (main_feature/trunk)
```

## 7. Service Type → Role Mapping

| Service Type | Role Template |
|-------------|--------------|
| backend_api | `roles/http-api.md` |
| web_ui | `roles/web-spa.md` |
| mobile_app | `roles/mobile-app.md` |
| worker | `roles/worker.md` |
| data_pipeline | `roles/ml-pipeline.md` |

## 8. Concern Activation

| Concern | Non-MSA Condition | MSA Condition |
|---------|------------------|---------------|
| database | `backend.databases is not empty` | Any service has `databases is not empty` |
| testing | Always | Always |
| deploy | Always | Always |
| auth | `backend.auth != none` | Any service has `auth != none` |

## 9. Branch Strategy Mapping

| Strategy | Integration Branch | Task Branch Pattern | Init Branches |
|----------|-------------------|-------------------|---------------|
| `master_develop_task` | `develop` | `task/*` from develop | master → develop |
| `main_feature` | `main` | `task/*` from main | main only |
| `trunk` | `main` | `task/*` from main | main only |
| `gitflow` | `develop` | `feature/*` from develop | master → develop |

## 10. Cross-Service Inference

| Rule | Condition | Inference |
|------|-----------|-----------|
| Event Bus | Non-MSA: `worker.queue_system` is set | Backend API acts as Producer for `worker.queue_system`. Templates should reference this in deployment env vars and architecture diagrams. |
| Event Bus | MSA: `service.worker_queue_system` is set | Other services in `service_list` may act as Producer. `<!-- AI: -->` comments guide Claude to resolve connections during initialization. |
