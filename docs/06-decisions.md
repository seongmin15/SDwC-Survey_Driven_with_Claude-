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
- Decision: monolith
- Reason: 서비스가 2개(backend_api, web_ui)뿐이고 MVP 단계라 단일 배포가 효율적.

### ADR-002: Internal Code Architecture

- Status: Accepted
- Context: 서비스 내부 코드 구조 패턴 결정 필요
- Decision: hexagonal
- Reason: 도메인 로직을 프레임워크와 분리하여 테스트성을 높이고 기술 교체에 유리하게 하기 위해.

### ADR-003: Backend Framework

- Status: Accepted
- Context: 백엔드 프레임워크 선정 필요
- Decision: python / fastapi
- Reason: 비동기 지원이 좋고 Python 생태계를 활용할 수 있어서.

### ADR-004: Backend Build Tool

- Status: Accepted
- Context: 백엔드 빌드/의존성 관리 도구 선정 필요
- Decision: poetry
- Reason: 의존성 잠금과 가상환경 관리가 일원화되어 있어서.

### ADR-005: Database — primary

- Status: Accepted
- Context: primary 데이터 저장소 선정 필요
- Decision: postgresql
- Reason: JSONB 지원으로 설문 데이터를 유연하게 저장 가능. 안정성, 확장성.

### ADR-006: Frontend Framework

- Status: Accepted
- Context: 프론트엔드 프레임워크 선정 필요
- Decision: typescript / react
- Reason: 생태계가 풍부하고 동적 폼 구현에 적합.

### ADR-007: Frontend Build Tool

- Status: Accepted
- Context: 프론트엔드 빌드/패키지 도구 선정 필요
- Decision: pnpm
- Reason: 디스크 효율과 설치 속도가 빠름.

### ADR-008: Deployment Strategy

- Status: Accepted
- Context: MVP 배포 환경 결정 필요
- Decision: docker_compose
- Reason: 초기에는 단일 서버로 충분하고 설정이 간단해서.
