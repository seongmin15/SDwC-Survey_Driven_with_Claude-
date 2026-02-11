# Project Profile

## Identity

- Project: {{project.name}}
- Stage: MVP
- Architecture: {{architecture.pattern}}
{{#if architecture.internal_style}}- Internal Style: {{architecture.internal_style}}{{/if}}

## Services

{{#if architecture.pattern != microservice}}
{{#each services}}
- {{this}}
{{/each}}
{{/if}}

{{#if architecture.pattern == microservice}}
{{#each service_list}}
- {{service.name}} ({{service.type}})
{{/each}}
{{/if}}

## Tech Stack

{{#if architecture.pattern != microservice}}

{{#if backend}}
### Backend
- Language: {{backend.language}}
- Framework: {{backend.framework}}
{{#if backend.build_tool}}- Build: {{backend.build_tool}}{{/if}}
{{#if backend.databases is not empty}}
- Databases:
{{#each backend.databases}}
  - {{db.engine}} ({{db.role}})
{{/each}}
{{/if}}
- API Style: {{backend.api_style}}
- Auth: {{backend.auth}}
- Deploy: {{backend.deploy_target}}
- Dependencies:
  <!-- AI:ONGOING: Add libraries here as the project progresses -->
{{/if}}

{{#if worker}}
### Worker
- Language: {{worker.language}}
{{#if worker.framework}}- Framework: {{worker.framework}}{{/if}}
{{#if worker.build_tool}}- Build: {{worker.build_tool}}{{/if}}
{{#if worker.queue_system}}- Queue: {{worker.queue_system}}{{/if}}
- Deploy: {{worker.deploy_target}}
- Dependencies:
  <!-- AI:ONGOING: Add libraries here as the project progresses -->
{{/if}}

{{#if web}}
### Web UI
- Language: {{web.language}}
- Framework: {{web.framework}}
{{#if web.build_tool}}- Build: {{web.build_tool}}{{/if}}
{{#if web.css_strategy}}- CSS: {{web.css_strategy}}{{/if}}
- Deploy: {{web.deploy_target}}
- Dependencies:
  <!-- AI:ONGOING: Add libraries here as the project progresses -->
{{/if}}

{{#if mobile}}
### Mobile App
- Platform: {{mobile.platform}}
- Language: {{mobile.language}}
- Framework: {{mobile.framework}}
{{#if mobile.build_tool}}- Build: {{mobile.build_tool}}{{/if}}
- Deploy: {{mobile.deploy_target}}
- Dependencies:
  <!-- AI:ONGOING: Add libraries here as the project progresses -->
{{/if}}

{{#if pipeline}}
### Data Pipeline
- Language: {{pipeline.language}}
- Framework: {{pipeline.framework}}
{{#if pipeline.build_tool}}- Build: {{pipeline.build_tool}}{{/if}}
- Deploy: {{pipeline.deploy_target}}
- Dependencies:
  <!-- AI:ONGOING: Add libraries here as the project progresses -->
{{/if}}

{{/if}}

{{#if architecture.pattern == microservice}}

{{#each service_list}}
### {{service.name}} ({{service.type}})
{{#if service.type == backend_api}}
- Language: {{service.language}}
- Framework: {{service.framework}}
{{#if service.build_tool}}- Build: {{service.build_tool}}{{/if}}
{{#if service.databases is not empty}}
- Databases:
{{#each service.databases}}
  - {{db.engine}} ({{db.role}})
{{/each}}
{{/if}}
- API Style: {{service.api_style}}
- Auth: {{service.auth}}
- Deploy: {{service.deploy_target}}
{{/if}}
{{#if service.type == web_ui}}
- Language: {{service.web_language}}
- Framework: {{service.web_framework}}
{{#if service.web_build_tool}}- Build: {{service.web_build_tool}}{{/if}}
{{#if service.css_strategy}}- CSS: {{service.css_strategy}}{{/if}}
- Deploy: {{service.web_deploy_target}}
{{/if}}
{{#if service.type == worker}}
- Language: {{service.worker_language}}
{{#if service.worker_build_tool}}- Build: {{service.worker_build_tool}}{{/if}}
{{#if service.worker_queue_system}}- Queue: {{service.worker_queue_system}}{{/if}}
- Deploy: {{service.worker_deploy_target}}
{{/if}}
{{#if service.type == mobile_app}}
- Platform: {{service.mobile_platform}}
- Language: {{service.mobile_language}}
- Framework: {{service.mobile_framework}}
{{#if service.mobile_build_tool}}- Build: {{service.mobile_build_tool}}{{/if}}
- Deploy: {{service.mobile_deploy_target}}
{{/if}}
{{#if service.type == data_pipeline}}
- Language: {{service.pipeline_language}}
- Framework: {{service.pipeline_framework}}
{{#if service.pipeline_build_tool}}- Build: {{service.pipeline_build_tool}}{{/if}}
- Deploy: {{service.pipeline_deploy_target}}
{{/if}}
- Dependencies:
  <!-- AI:ONGOING: Add libraries here as the project progresses -->
{{/each}}

{{/if}}

## Collaboration Defaults

- Methodology: {{collaboration.methodology}}
- Timebox: {{collaboration.task_review_minutes}} minutes
- WIP Limit: {{collaboration.wip_limit}}
- Approval Required: true
- Git: {{git.branch_strategy}}

## Artifacts

> **This list is authoritative.**
> AI uses this list to generate service-specific skill files under `skills/`.

{{#if architecture.pattern != microservice}}
{{#each services}}
- {{this}}
{{/each}}
{{/if}}

{{#if architecture.pattern == microservice}}
{{#each service_list}}
- {{service.name}}
{{/each}}
{{/if}}
