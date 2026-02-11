# Deployment

## Infrastructure

- Orchestration: docker_compose
- Reason: 초기에는 단일 서버로 충분하고 설정이 간단해서.

## Service Deployment

### backend_api

- Deploy Target: docker
- Language: python
- Framework: fastapi

| Variable | Required | Description |
|----------|----------|-------------|
| POSTGRESQL_URL | yes | postgresql (primary) 연결 문자열 |

| HOST | no | 서버 바인딩 호스트 |
| PORT | no | 서버 포트 |

### web_ui

- Deploy Target: same_server
- Framework: react

| Variable | Required | Description |
|----------|----------|-------------|
| API_URL | yes | backend_api 엔드포인트 URL |

## Health Checks

| Service | Endpoint | Expected |
|---------|----------|----------|

| backend_api | /health | 200 OK |
| backend_api | /ready | 200 OK |
| web_ui | /health | 200 OK |
| web_ui | /ready | 200 OK |

## Deployment Checklist

- [ ] 이미지 빌드 성공
- [ ] 환경변수 설정 완료
- [ ] Health check 응답 확인
- [ ] 시크릿이 이미지/코드에 미포함 확인
