# Docker Compose Template

> 이 문서는 프로젝트 시작 시 AI가 상세를 채웁니다.

## Overview

- Orchestration: docker_compose
- Reason: 초기에는 단일 서버로 충분하고 설정이 간단해서.

## Services

### backend_api

```yaml
backend_api:
  build:
    context: ./backend
    dockerfile: Dockerfile
  ports:
    - "8000:8000"
  environment:
    - POSTGRESQL_URL=postgresql://sdwc:sdwc@postgres:5432/sdwc
    - HOST=0.0.0.0
    - PORT=8000
  depends_on:
    postgres:
      condition: service_healthy
  volumes:
    - ./backend:/app
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    interval: 10s
    timeout: 5s
    retries: 3
    start_period: 10s
```

### web_ui

```yaml
web_ui:
  build:
    context: ./frontend
    dockerfile: Dockerfile
  ports:
    - "3000:3000"
  environment:
    - API_URL=http://backend_api:8000
  depends_on:
    - backend_api
  volumes:
    - ./frontend:/app
    - /app/node_modules
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
    interval: 10s
    timeout: 5s
    retries: 3
    start_period: 15s
```

### Database Services

```yaml
postgres:
  image: postgres:16-alpine
  environment:
    - POSTGRES_USER=sdwc
    - POSTGRES_PASSWORD=sdwc
    - POSTGRES_DB=sdwc
  volumes:
    - pgdata:/var/lib/postgresql/data
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U sdwc"]
    interval: 5s
    timeout: 3s
    retries: 5
```

## docker-compose.yml Skeleton

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=sdwc
      - POSTGRES_PASSWORD=sdwc
      - POSTGRES_DB=sdwc
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U sdwc"]
      interval: 5s
      timeout: 3s
      retries: 5

  backend_api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - POSTGRESQL_URL=postgresql://sdwc:sdwc@postgres:5432/sdwc
      - HOST=0.0.0.0
      - PORT=8000
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 10s

  web_ui:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - API_URL=http://backend_api:8000
    depends_on:
      - backend_api
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 15s

volumes:
  pgdata:
```

## Development Overrides

```yaml
# docker-compose.override.yml
services:
  backend_api:
    volumes:
      - ./backend:/app
    environment:
      - DEBUG=true
      - LOG_LEVEL=DEBUG
    ports:
      - "8000:8000"
      - "5678:5678"  # debugpy

  web_ui:
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
```

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
