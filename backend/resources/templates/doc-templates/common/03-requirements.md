# Requirements

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

## Functional Requirements

{{#each scope.in_scope}}
- {{this}}
{{/each}}

{{#if architecture.pattern != microservice}}

{{#if backend}}
### backend_api

- API Style: {{backend.api_style}}
- Auth: {{backend.auth}}
- Endpoints:

{{backend.main_endpoints}}

{{#if backend.main_entities}}
- Entities:

{{backend.main_entities}}
{{/if}}
{{/if}}

{{#if worker}}
### worker

- Language: {{worker.language}}
{{#if worker.queue_system}}- Queue: {{worker.queue_system}}{{/if}}
- Description:

{{worker.description}}
{{/if}}

{{#if web}}
### web_ui

- Pages:

{{web.main_pages}}

- Flow:

{{web.page_flow}}

{{#if web.connected_api}}- Connected API: {{web.connected_api}}{{/if}}
{{/if}}

{{/if}}

{{#if architecture.pattern == microservice}}

{{#each service_list}}
### {{service.name}} ({{service.type}})

{{#if service.type == backend_api}}
- Language: {{service.language}} / {{service.framework}}
- API Style: {{service.api_style}}
- Auth: {{service.auth}}
- Endpoints:

{{service.main_endpoints}}

{{#if service.main_entities}}
- Entities:

{{service.main_entities}}
{{/if}}
{{/if}}

{{#if service.type == web_ui}}
- Language: {{service.web_language}} / {{service.web_framework}}
- Pages:

{{service.main_pages}}

- Flow:

{{service.page_flow}}

{{#if service.connected_api}}- Connected API: {{service.connected_api}}{{/if}}
{{/if}}

{{#if service.type == worker}}
- Language: {{service.worker_language}}
- Description:

{{service.worker_description}}
{{/if}}

{{/each}}

{{/if}}

## Non-Functional Requirements

- Architecture: {{architecture.pattern}}
- Deployment: {{deployment.initial}}
- Observability: {{#if observability.included_in_mvp}}포함{{else}}최소 (health/ready만){{/if}}

## Tech Stack

{{#if architecture.pattern != microservice}}

| Layer | Technology |
|-------|-----------|
{{#if backend}}
| Backend Language | {{backend.language}} |
| Backend Framework | {{backend.framework}} |
{{#each backend.databases}}
| Database ({{db.role}}) | {{db.engine}} |
{{/each}}
| Backend Deploy | {{backend.deploy_target}} |
{{/if}}
{{#if worker}}
| Worker Language | {{worker.language}} |
{{#if worker.framework}}| Worker Framework | {{worker.framework}} |{{/if}}
{{#if worker.queue_system}}| Worker Queue | {{worker.queue_system}} |{{/if}}
| Worker Deploy | {{worker.deploy_target}} |
{{/if}}
{{#if web}}
| Frontend Language | {{web.language}} |
| Frontend Framework | {{web.framework}} |
{{#if web.css_strategy}}| CSS | {{web.css_strategy}} |{{/if}}
| Frontend Deploy | {{web.deploy_target}} |
{{/if}}
| Infra | {{deployment.initial}} |

{{/if}}

{{#if architecture.pattern == microservice}}

| Service | Language | Framework | Database | Deploy |
|---------|---------|-----------|----------|--------|
{{#each service_list}}
{{#if service.type == backend_api}}| {{service.name}} | {{service.language}} | {{service.framework}} | {{#each service.databases}}{{db.engine}}{{#unless @last}}, {{/unless}}{{/each}} | {{service.deploy_target}} |{{/if}}
{{#if service.type == web_ui}}| {{service.name}} | {{service.web_language}} | {{service.web_framework}} | — | {{service.web_deploy_target}} |{{/if}}
{{#if service.type == worker}}| {{service.name}} | {{service.worker_language}} | — | — | {{service.worker_deploy_target}} |{{/if}}
{{/each}}

| Infra | {{deployment.initial}} |

{{/if}}
