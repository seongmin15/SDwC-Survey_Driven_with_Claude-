# Architecture

## Overview

- Pattern: monolith
- Reason: 서비스가 2개(backend_api, web_ui)뿐이고 MVP 단계라 단일 배포가 효율적.
- Internal Style: hexagonal
- Deployment: docker_compose

## Component Diagram

```mermaid
C4Component
    title SDwC — Component Diagram

    Person(user, "사용자", "1인 개발자")

    Container_Boundary(frontend, "web_ui [React / TypeScript / Tailwind]") {
        Component(pages, "Pages", "React", "Survey · Generate · Complete")
        Component(apiClient, "API Client", "TypeScript", "backend_api REST 호출 래퍼")
    }

    Container_Boundary(backend, "backend_api [FastAPI / Python]") {
        Component(routes, "API Routes", "FastAPI Router", "/intakes · /generate · /projects")
        Component(usecases, "Use Cases", "Python", "비즈니스 로직 오케스트레이션")
        Component(domain, "Domain", "Python", "엔티티 · 포트(인터페이스)")
        Component(templateEngine, "Template Engine", "Python", "intake 데이터 + doc-templates → 문서 렌더링")
        Component(zipPackager, "ZIP Packager", "Python", "문서 ZIP 패키징")
        Component(repos, "Repository Adapters", "SQLAlchemy", "PostgreSQL 접근 구현체")
    }

    ContainerDb(db, "PostgreSQL", "primary", "projects · events")

    Rel(user, pages, "설문 작성 / 생성 / 다운로드")
    Rel(pages, apiClient, "사용자 액션 전달")
    Rel(apiClient, routes, "REST / JSON", "HTTP")
    Rel(routes, usecases, "요청 처리 위임")
    Rel(usecases, domain, "도메인 로직 호출")
    Rel(usecases, templateEngine, "문서 생성 요청")
    Rel(templateEngine, zipPackager, "렌더링 결과 전달")
    Rel(usecases, repos, "데이터 조회 / 저장")
    Rel(repos, db, "SQL", "TCP")
```

## Services

- **backend_api**
- **web_ui**

## Tech Stack

| Layer | Technology |
|-------|-----------|

| Backend Language | python |
| Backend Framework | fastapi |
| API Style | rest |
| Database (primary) | postgresql |

| Backend Deploy | docker |

| Frontend Language | typescript |
| Frontend Framework | react |
| CSS | tailwind |
| Frontend Deploy | same_server |

| Infra | docker_compose |

## Service Details

### backend_api

- Language: python
- Framework: fastapi
- API Style: rest
- Auth: none

- Databases:
  - postgresql — primary

- Deploy: docker

#### Endpoints

POST /intakes — 설문 데이터 저장
POST /generate — 문서 생성 트리거
GET /projects/:id — 프로젝트 메타 조회
GET /projects/:id/download — ZIP 다운로드

#### Data Entities

projects — 프로젝트 (설문 데이터 + 생성 상태)
events — 생성 이벤트 이력

### web_ui

- Language: typescript
- Framework: react
- CSS: tailwind
- Connected API: backend_api
- Deploy: same_server

#### Pages

Survey — 설문 입력 페이지
Generate — 문서 생성 페이지
Complete — 프로젝트 URL 안내 페이지

