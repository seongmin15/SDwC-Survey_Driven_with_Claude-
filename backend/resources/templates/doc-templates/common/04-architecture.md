# Architecture

## Overview

- Pattern: {{architecture.pattern}}
- Reason: {{architecture.pattern_reason}}
{{#if architecture.internal_style}}- Internal Style: {{architecture.internal_style}}{{/if}}
- Deployment: {{deployment.initial}}

## Component Diagram

<!-- AI:INIT: Draw a Mermaid C4 Component diagram showing service interactions.
     Include: all services, databases, external connections, and data flow direction.
     Use ```mermaid code block.
-->

{{#if architecture.pattern == modular_monolith}}
## Module Structure

> 아래 섹션은 프로젝트 시작 시 AI가 모듈 경계를 구체화합니다.
> 각 모듈 간 의존성 방향과 공유 인터페이스를 정의합니다.

<!-- AI:INIT: During initialization, define module boundaries based on services and scope.
     Internal style is {{architecture.internal_style}} (if selected).
     Include:
     - Module list with responsibilities
     - Inter-module dependency direction (which module depends on which)
     - Shared interfaces / ports between modules
     - How the internal style applies to the module structure
-->
{{/if}}

## Services

{{#if architecture.pattern != microservice}}
{{#each services}}
- **{{this}}**
{{/each}}
{{/if}}

{{#if architecture.pattern == microservice}}
{{#each service_list}}
- **{{service.name}}** ({{service.type}})
{{/each}}
{{/if}}

## Tech Stack

{{#if architecture.pattern != microservice}}

| Layer | Technology |
|-------|-----------|
{{#if backend}}
| Backend Language | {{backend.language}} |
| Backend Framework | {{backend.framework}} |
| API Style | {{backend.api_style}} |
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
{{#if mobile}}
| Mobile Platform | {{mobile.platform}} |
| Mobile Language | {{mobile.language}} |
| Mobile Framework | {{mobile.framework}} |
| Mobile Deploy | {{mobile.deploy_target}} |
{{/if}}
{{#if pipeline}}
| Pipeline Language | {{pipeline.language}} |
| Pipeline Framework | {{pipeline.framework}} |
| Pipeline Deploy | {{pipeline.deploy_target}} |
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
{{#if service.type == mobile_app}}| {{service.name}} | {{service.mobile_language}} | {{service.mobile_framework}} | — | {{service.mobile_deploy_target}} |{{/if}}
{{#if service.type == data_pipeline}}| {{service.name}} | {{service.pipeline_language}} | {{service.pipeline_framework}} | — | {{service.pipeline_deploy_target}} |{{/if}}
{{/each}}

| Infra | {{deployment.initial}} |

{{/if}}

## Service Details

{{#if architecture.pattern != microservice}}

{{#if backend}}
### backend_api

- Language: {{backend.language}}
- Framework: {{backend.framework}}
- API Style: {{backend.api_style}}
- Auth: {{backend.auth}}
{{#if backend.databases is not empty}}
- Databases:
{{#each backend.databases}}
  - {{db.engine}} — {{db.role}}
{{/each}}
{{/if}}
- Deploy: {{backend.deploy_target}}

#### Endpoints

{{backend.main_endpoints}}

{{#if backend.main_entities}}
#### Data Entities

{{backend.main_entities}}
{{/if}}
{{/if}}

{{#if worker}}
### worker

- Language: {{worker.language}}
{{#if worker.framework}}- Framework: {{worker.framework}}{{/if}}
{{#if worker.queue_system}}- Queue: {{worker.queue_system}}{{/if}}
- Deploy: {{worker.deploy_target}}

#### Description

{{worker.description}}
{{/if}}

{{#if web}}
### web_ui

- Language: {{web.language}}
- Framework: {{web.framework}}
{{#if web.css_strategy}}- CSS: {{web.css_strategy}}{{/if}}
{{#if web.connected_api}}- Connected API: {{web.connected_api}}{{/if}}
- Deploy: {{web.deploy_target}}

#### Pages

{{web.main_pages}}
{{/if}}

{{#if mobile}}
### mobile_app

- Platform: {{mobile.platform}}
- Language: {{mobile.language}}
- Framework: {{mobile.framework}}
{{#if mobile.connected_api}}- Connected API: {{mobile.connected_api}}{{/if}}
- Deploy: {{mobile.deploy_target}}

#### Screens

{{mobile.main_screens}}
{{/if}}

{{#if pipeline}}
### data_pipeline

- Language: {{pipeline.language}}
- Framework: {{pipeline.framework}}
- Deploy: {{pipeline.deploy_target}}

#### Description

{{pipeline.description}}
{{/if}}

{{/if}}

{{#if architecture.pattern == microservice}}

{{#each service_list}}
### {{service.name}} ({{service.type}})

{{#if service.type == backend_api}}
- Language: {{service.language}}
- Framework: {{service.framework}}
- API Style: {{service.api_style}}
- Auth: {{service.auth}}
{{#if service.databases is not empty}}
- Databases:
{{#each service.databases}}
  - {{db.engine}} — {{db.role}}
{{/each}}
{{/if}}
- Deploy: {{service.deploy_target}}

#### Endpoints

{{service.main_endpoints}}

{{#if service.main_entities}}
#### Data Entities

{{service.main_entities}}
{{/if}}
{{/if}}

{{#if service.type == web_ui}}
- Language: {{service.web_language}}
- Framework: {{service.web_framework}}
{{#if service.css_strategy}}- CSS: {{service.css_strategy}}{{/if}}
{{#if service.connected_api}}- Connected API: {{service.connected_api}}{{/if}}
- Deploy: {{service.web_deploy_target}}

#### Pages

{{service.main_pages}}
{{/if}}

{{#if service.type == worker}}
- Language: {{service.worker_language}}
- Deploy: {{service.worker_deploy_target}}

#### Description

{{service.worker_description}}
{{/if}}

{{#if service.type == mobile_app}}
- Platform: {{service.mobile_platform}}
- Language: {{service.mobile_language}}
- Framework: {{service.mobile_framework}}
{{#if service.mobile_connected_api}}- Connected API: {{service.mobile_connected_api}}{{/if}}
- Deploy: {{service.mobile_deploy_target}}

#### Screens

{{service.mobile_main_screens}}
{{/if}}

{{#if service.type == data_pipeline}}
- Language: {{service.pipeline_language}}
- Framework: {{service.pipeline_framework}}
- Deploy: {{service.pipeline_deploy_target}}

#### Description

{{service.pipeline_description}}
{{/if}}

{{/each}}

{{/if}}
