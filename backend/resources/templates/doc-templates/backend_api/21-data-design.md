# Data Design

> 이 문서는 프로젝트 시작 시 AI가 상세를 채웁니다.

## Databases

{{#each backend.databases}}
### {{db.engine}} — {{db.role}}

- Engine: {{db.engine}}
- Role: {{db.role}}
- Reason: {{db.reason}}

{{/each}}

## Entities (설문 기준)

{{backend.main_entities}}

---

{{#each backend.databases}}
## {{db.engine}} ({{db.role}}) — Table Details

> 아래 섹션은 프로젝트 시작 시 AI가 채웁니다.
> 이 데이터베이스에 속하는 테이블/컬렉션의 상세를 작성합니다.

<!-- AI:INIT: Based on backend.main_entities, fill tables belonging to {{db.engine}} ({{db.role}}).
     Per table/collection:
     - Column/Field (name, type, nullable, description)
     - Indexes
     - Constraints
     - Relations (FK, CASCADE, etc.)
-->

{{/each}}

## Cross-Database Considerations

> 다중 DB 환경에서의 데이터 정합성과 동기화 전략을 기술합니다.

<!-- AI:INIT: If only one database is configured, write "해당 없음 — 단일 데이터베이스 구성" and remove this comment.
     If multiple databases exist, describe:
     - Which entities live in which database and why
     - Data flow between databases (e.g., ID references across DBs)
     - Consistency strategy (eventual consistency, saga, etc.)
     - Transaction boundaries (which operations are atomic within a single DB)
-->

## Migration Rules

- 모든 마이그레이션은 up/down 양방향으로 작성
- 데이터 삭제가 포함된 마이그레이션은 별도 승인 필요
- 스키마 변경 시 이 문서를 먼저 업데이트
