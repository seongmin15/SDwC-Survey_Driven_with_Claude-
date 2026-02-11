# Docker Compose Template

> 이 문서는 프로젝트 시작 시 AI가 상세를 채웁니다.

## Overview

- Orchestration: docker_compose
- Reason: {{deployment.initial_reason}}

## Services

{{#each services}}
### {{this}}

<!-- AI:INIT: Based on this service's deploy_target and tech stack from docs/04-architecture.md,
     define the docker-compose service block including:
     - image or build context
     - ports mapping
     - environment variables (reference docs/07-deployment.md)
     - depends_on (service startup order)
     - volumes (if needed for development hot-reload)
     - healthcheck (reference docs/07-deployment.md Health Checks)
-->

{{/each}}

### Database Services

<!-- AI:INIT: Based on docs/21-data-design.md (if databases exist),
     define database service blocks including:
     - image and version tag
     - environment variables (credentials)
     - volumes (data persistence)
     - healthcheck
-->

## docker-compose.yml Skeleton

<!-- AI:INIT: Generate a complete docker-compose.yml skeleton combining all services above.
     Include:
     - version (if needed)
     - services (all application + database services)
     - networks (default bridge is fine for MVP)
     - volumes (named volumes for DB persistence)
     Format as a ```yaml code block.
-->

## Development Overrides

<!-- AI:INIT: Define docker-compose.override.yml for local development:
     - Volume mounts for source code (hot-reload)
     - Debug ports
     - Environment variable overrides (DEBUG=true, etc.)
-->

## Commands

```bash
# 전체 스택 시작
docker compose up -d

# 로그 확인
docker compose logs -f

# 전체 중지
docker compose down

# DB 볼륨 포함 초기화
docker compose down -v
```
