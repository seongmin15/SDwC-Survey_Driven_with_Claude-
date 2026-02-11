# Deployment

## Infrastructure

- Orchestration: {{deployment.initial}}
- Reason: {{deployment.initial_reason}}
{{#if deployment.future}}
- Future: {{#each deployment.future}}{{this}}{{#unless @last}}, {{/unless}}{{/each}}
{{/if}}

## Service Deployment

{{#if architecture.pattern != microservice}}

{{#if backend}}
### backend_api

- Deploy Target: {{backend.deploy_target}}
- Language: {{backend.language}}
- Framework: {{backend.framework}}

| Variable | Required | Description |
|----------|----------|-------------|
{{#each backend.databases}}
| {{db.engine | upper}}_URL | yes | {{db.engine}} ({{db.role}}) 연결 문자열 |
{{/each}}
| HOST | no | 서버 바인딩 호스트 |
| PORT | no | 서버 포트 |
{{/if}}

{{#if worker}}
### worker

- Deploy Target: {{worker.deploy_target}}
- Language: {{worker.language}}
{{#if worker.framework}}- Framework: {{worker.framework}}{{/if}}
{{#if worker.queue_system}}- Queue: {{worker.queue_system}}{{/if}}

| Variable | Required | Description |
|----------|----------|-------------|
{{#if worker.queue_system}}| QUEUE_URL | yes | {{worker.queue_system}} 연결 문자열 |{{/if}}
{{#each backend.databases}}
| {{db.engine | upper}}_URL | yes | {{db.engine}} ({{db.role}}) 연결 문자열 |
{{/each}}
<!-- AI:INIT: Fill additional worker environment variables during initialization -->
{{/if}}

{{#if web}}
### web_ui

- Deploy Target: {{web.deploy_target}}
- Framework: {{web.framework}}

| Variable | Required | Description |
|----------|----------|-------------|
{{#if web.connected_api}}| API_URL | yes | backend_api 엔드포인트 URL |{{/if}}
{{/if}}

{{#if mobile}}
### mobile_app

- Deploy Target: {{mobile.deploy_target}}
- Framework: {{mobile.framework}}

| Variable | Required | Description |
|----------|----------|-------------|
{{#if mobile.connected_api}}| API_URL | yes | backend_api 엔드포인트 URL |{{/if}}
<!-- AI:INIT: Fill additional mobile environment variables during initialization -->
{{/if}}

{{#if pipeline}}
### data_pipeline

- Deploy Target: {{pipeline.deploy_target}}
- Framework: {{pipeline.framework}}

| Variable | Required | Description |
|----------|----------|-------------|
<!-- AI:INIT: Fill pipeline environment variables during initialization -->
{{/if}}

{{/if}}

{{#if architecture.pattern == microservice}}

{{#each service_list}}
### {{service.name}} ({{service.type}})

{{#if service.type == backend_api}}
- Deploy Target: {{service.deploy_target}}
- Language: {{service.language}}
- Framework: {{service.framework}}

| Variable | Required | Description |
|----------|----------|-------------|
{{#each service.databases}}
| {{db.engine | upper}}_URL | yes | {{db.engine}} ({{db.role}}) 연결 문자열 |
{{/each}}
| HOST | no | 서버 바인딩 호스트 |
| PORT | no | 서버 포트 |
{{/if}}

{{#if service.type == web_ui}}
- Deploy Target: {{service.web_deploy_target}}
- Framework: {{service.web_framework}}

| Variable | Required | Description |
|----------|----------|-------------|
{{#if service.connected_api}}| API_URL | yes | {{service.connected_api}} 엔드포인트 URL |{{/if}}
{{/if}}

{{#if service.type == worker}}
- Deploy Target: {{service.worker_deploy_target}}
- Language: {{service.worker_language}}

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | <!-- AI:INIT: Fill worker environment variables during initialization --> |
{{/if}}

{{#if service.type == mobile_app}}
- Deploy Target: {{service.mobile_deploy_target}}
- Framework: {{service.mobile_framework}}

| Variable | Required | Description |
|----------|----------|-------------|
{{#if service.mobile_connected_api}}| API_URL | yes | {{service.mobile_connected_api}} 엔드포인트 URL |{{/if}}
{{/if}}

{{#if service.type == data_pipeline}}
- Deploy Target: {{service.pipeline_deploy_target}}
- Framework: {{service.pipeline_framework}}

| Variable | Required | Description |
|----------|----------|-------------|
<!-- AI:INIT: Fill pipeline environment variables during initialization -->
{{/if}}

{{/each}}

{{/if}}

## Health Checks

| Service | Endpoint | Expected |
|---------|----------|----------|
{{#if architecture.pattern != microservice}}
{{#each services}}
| {{this}} | /health | 200 OK |
| {{this}} | /ready | 200 OK |
{{/each}}
{{/if}}
{{#if architecture.pattern == microservice}}
{{#each service_list}}
| {{service.name}} | /health | 200 OK |
| {{service.name}} | /ready | 200 OK |
{{/each}}
{{/if}}

## Deployment Checklist

- [ ] 이미지 빌드 성공
- [ ] 환경변수 설정 완료
- [ ] Health check 응답 확인
- [ ] 시크릿이 이미지/코드에 미포함 확인
