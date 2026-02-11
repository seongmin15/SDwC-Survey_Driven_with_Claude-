# Decisions

> 아키텍처 및 기술적 의사결정을 기록합니다.
> 새 결정이 내려질 때마다 아래 형식으로 추가합니다.

## Format

```
### ADR-NNN: <제목>
- Status: Proposed | Accepted | Deprecated | Superseded
- Context: 왜 이 결정이 필요했는가
- Decision: 무엇을 결정했는가
- Reason: 선택 이유
```

---

### ADR-001: Architecture Pattern

- Status: Accepted
- Context: 시스템 아키텍처 패턴 결정 필요
- Decision: {{architecture.pattern}}
- Reason: {{architecture.pattern_reason}}

{{#if architecture.internal_style}}
### ADR-{{@adr_number}}: Internal Code Architecture

- Status: Accepted
- Context: 서비스 내부 코드 구조 패턴 결정 필요
- Decision: {{architecture.internal_style}}
{{#if architecture.internal_style_reason}}- Reason: {{architecture.internal_style_reason}}{{/if}}
{{/if}}

{{#if architecture.pattern != microservice}}

{{#if backend}}
### ADR-002: Backend Framework

- Status: Accepted
- Context: 백엔드 프레임워크 선정 필요
- Decision: {{backend.language}} / {{backend.framework}}
- Reason: {{backend.framework_reason}}

{{#if backend.build_tool}}
### ADR-{{@adr_number}}: Backend Build Tool

- Status: Accepted
- Context: 백엔드 빌드/의존성 관리 도구 선정 필요
- Decision: {{backend.build_tool}}
{{#if backend.build_tool_reason}}- Reason: {{backend.build_tool_reason}}{{/if}}
{{/if}}

{{#each backend.databases}}
### ADR-{{@adr_number}}: Database — {{db.role}}

- Status: Accepted
- Context: {{db.role}} 데이터 저장소 선정 필요
- Decision: {{db.engine}}
- Reason: {{db.reason}}
{{/each}}
{{/if}}

{{#if worker}}
### ADR-{{@adr_number}}: Worker Configuration

- Status: Accepted
- Context: Worker 서비스 기술 스택 결정 필요
- Decision: {{worker.language}}{{#if worker.framework}} / {{worker.framework}}{{/if}}{{#if worker.queue_system}} + {{worker.queue_system}}{{/if}}
- Reason: {{worker.description}}

{{#if worker.build_tool}}
### ADR-{{@adr_number}}: Worker Build Tool

- Status: Accepted
- Context: Worker 빌드/의존성 관리 도구 선정 필요
- Decision: {{worker.build_tool}}
{{#if worker.build_tool_reason}}- Reason: {{worker.build_tool_reason}}{{/if}}
{{/if}}
{{/if}}

{{#if web}}
### ADR-{{@adr_number}}: Frontend Framework

- Status: Accepted
- Context: 프론트엔드 프레임워크 선정 필요
- Decision: {{web.language}} / {{web.framework}}
- Reason: {{web.framework_reason}}

{{#if web.build_tool}}
### ADR-{{@adr_number}}: Frontend Build Tool

- Status: Accepted
- Context: 프론트엔드 빌드/패키지 도구 선정 필요
- Decision: {{web.build_tool}}
{{#if web.build_tool_reason}}- Reason: {{web.build_tool_reason}}{{/if}}
{{/if}}
{{/if}}

{{#if mobile}}
### ADR-{{@adr_number}}: Mobile App

- Status: Accepted
- Context: 모바일 앱 기술 스택 결정 필요
- Decision: {{mobile.platform}} / {{mobile.language}} / {{mobile.framework}}
- Reason: {{mobile.framework_reason}}

{{#if mobile.build_tool}}
### ADR-{{@adr_number}}: Mobile Build Tool

- Status: Accepted
- Context: 모바일 빌드/의존성 도구 선정 필요
- Decision: {{mobile.build_tool}}
{{#if mobile.build_tool_reason}}- Reason: {{mobile.build_tool_reason}}{{/if}}
{{/if}}
{{/if}}

{{#if pipeline}}
### ADR-{{@adr_number}}: Data Pipeline

- Status: Accepted
- Context: 데이터 파이프라인 기술 스택 결정 필요
- Decision: {{pipeline.language}} / {{pipeline.framework}}
- Reason: {{pipeline.framework_reason}}

{{#if pipeline.build_tool}}
### ADR-{{@adr_number}}: Pipeline Build Tool

- Status: Accepted
- Context: 파이프라인 빌드/의존성 도구 선정 필요
- Decision: {{pipeline.build_tool}}
{{#if pipeline.build_tool_reason}}- Reason: {{pipeline.build_tool_reason}}{{/if}}
{{/if}}
{{/if}}

{{/if}}

{{#if architecture.pattern == microservice}}

<!-- 서버 생성 시 service_list를 순회하며 ADR-002부터 자동 번호 부여 -->
{{#each service_list}}
### ADR-{{@adr_number}}: {{service.name}} Tech Stack

- Status: Accepted
- Context: {{service.name}} 서비스 기술 스택 결정 필요
{{#if service.type == backend_api}}- Decision: {{service.language}} / {{service.framework}}{{#if service.build_tool}} / {{service.build_tool}}{{/if}} / {{#each service.databases}}{{db.engine}}{{#unless @last}}, {{/unless}}{{/each}}
- Reason: {{service.framework_reason}}{{/if}}
{{#if service.type == web_ui}}- Decision: {{service.web_language}} / {{service.web_framework}}{{#if service.web_build_tool}} / {{service.web_build_tool}}{{/if}}{{/if}}
{{#if service.type == worker}}- Decision: {{service.worker_language}}{{#if service.worker_build_tool}} / {{service.worker_build_tool}}{{/if}}{{/if}}
{{#if service.type == mobile_app}}- Decision: {{service.mobile_platform}} / {{service.mobile_language}} / {{service.mobile_framework}}{{#if service.mobile_build_tool}} / {{service.mobile_build_tool}}{{/if}}{{/if}}
{{#if service.type == data_pipeline}}- Decision: {{service.pipeline_language}} / {{service.pipeline_framework}}{{#if service.pipeline_build_tool}} / {{service.pipeline_build_tool}}{{/if}}{{/if}}

{{/each}}

{{/if}}

### ADR-{{@next_adr}}: Deployment Strategy

- Status: Accepted
- Context: MVP 배포 환경 결정 필요
- Decision: {{deployment.initial}}
- Reason: {{deployment.initial_reason}}
