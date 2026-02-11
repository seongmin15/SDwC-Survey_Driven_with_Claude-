# Worker Data Flow

> 이 문서는 프로젝트 시작 시 AI가 상세를 채웁니다.

## Input Schema

> Worker가 소비하는 메시지/데이터의 구조를 정의합니다.

<!-- AI:INIT: During initialization, define input data:
     - Source (queue topic, schedule trigger, API webhook)
     - Message/payload schema with field descriptions
     - Example payload (JSON)
     - Validation rules (required fields, format constraints)
-->

## Output Schema

> Worker가 처리 후 생성하는 결과물의 구조를 정의합니다.

<!-- AI:INIT: During initialization, define output data:
     - Destination (DB table, output queue, file, API)
     - Output schema with field descriptions
     - Mapping: input fields → output fields
     - Enrichment: fields added during processing
-->

## Data Flow Diagram

<!-- AI:INIT: During initialization, draw the end-to-end data flow:
     Source → [Queue/Schedule] → Worker → [Processing] → Destination
     Include branching paths for success/failure
-->

## Idempotency

> 동일한 메시지가 재처리되어도 결과가 동일해야 합니다.

<!-- AI:INIT: During initialization, define:
     - Idempotency key (which field uniquely identifies a message)
     - Dedup mechanism (DB unique constraint, Redis set, hash check)
     - At-least-once vs exactly-once semantics and the chosen approach
-->

## Backpressure

<!-- AI:INIT: During initialization, define how the worker handles overload:
     - Rate limiting strategy
     - Queue depth monitoring
     - Scaling trigger (if applicable)
     - Graceful degradation behavior
-->
