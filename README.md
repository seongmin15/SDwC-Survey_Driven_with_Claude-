# SDwC — Survey-Driven with Claude

설문만 작성하면 AI 협업에 최적화된 프로젝트 문서 패키지(CLAUDE.md, docs/, .sdwc/)를
자동 생성하여 ZIP으로 제공하고, Claude Code가 이를 기반으로 프로젝트를 초기화하는 서비스.

## 핵심 흐름

```
설문 작성 → 문서 생성 → ZIP 다운로드 → Claude Code에서 "프로젝트 시작해"
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python / FastAPI / Poetry |
| Database | PostgreSQL |
| Frontend | TypeScript / React / Tailwind CSS / pnpm |
| Infrastructure | Docker Compose |

## Getting Started

### 사전 요구사항

- Docker & Docker Compose
- Git

### 실행

```bash
# 저장소 클론
git clone <repository-url>
cd sdwc

# 전체 스택 시작
docker compose up -d

# 로그 확인
docker compose logs -f
```

### 접속

- Web UI: http://localhost:3000
- Backend API: http://localhost:8000
- API 문서: http://localhost:8000/docs (FastAPI Swagger)

### 종료

```bash
docker compose down

# DB 볼륨 포함 초기화
docker compose down -v
```

## Project Structure

```
sdwc/
├── backend/          # FastAPI backend (Hexagonal Architecture)
├── frontend/         # React frontend (SPA)
├── docs/             # Project documentation (SSOT)
├── skills/           # Claude Code skill files
├── CLAUDE.md         # AI collaboration rules
├── docker-compose.yml
└── README.md
```

## Development

- **Methodology**: Kanban (WIP Limit: 2)
- **TDD**: Red → Green → Refactor
- **Git**: master / develop / task/* branch strategy
- **Task Backlog**: `docs/09-task-backlog.md`
