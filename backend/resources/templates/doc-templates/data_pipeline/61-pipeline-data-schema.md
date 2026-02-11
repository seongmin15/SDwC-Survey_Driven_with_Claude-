# Pipeline Data Schema

> 이 문서는 프로젝트 시작 시 AI가 상세를 채웁니다.

## Source Schemas

> 각 데이터 소스의 스키마를 정의합니다.

<!-- AI:INIT: During initialization, define per source:
     - Schema name
     - Fields (name, type, nullable, description)
     - Primary key / unique identifier
     - Volume and update frequency
     - Example record
-->

## Transformation Rules

> 소스 데이터를 목적 형식으로 변환하는 규칙을 정의합니다.

<!-- AI:INIT: During initialization, define transformations:
     - Mapping: source field → target field
     - Type conversions
     - Derived/computed fields (formulas, lookups)
     - Filtering rules (which records to include/exclude)
     - Deduplication logic
     - Aggregation rules (if applicable)
-->

## Target Schemas

> 최종 목적지의 데이터 스키마를 정의합니다.

<!-- AI:INIT: During initialization, define per sink:
     - Schema name
     - Fields (name, type, nullable, description)
     - Indexes and partitions
     - Constraints
     - Example record (after transformation)
-->

## Data Lineage

<!-- AI:INIT: During initialization, trace data lineage:
     - Source field → transformation → target field mapping
     - Which stages modify which fields
     - Audit trail requirements (who changed what, when)
-->

## Schema Evolution

<!-- AI:INIT: During initialization, define schema change strategy:
     - How to handle source schema changes (new column, type change)
     - Backward compatibility rules
     - Migration procedure for target schema changes
-->
