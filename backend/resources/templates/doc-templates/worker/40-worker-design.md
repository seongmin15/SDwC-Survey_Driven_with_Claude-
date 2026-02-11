# Worker Design

> 이 문서는 프로젝트 시작 시 AI가 상세를 채웁니다.

## Overview

{{#if architecture.pattern != microservice}}
- Language: {{worker.language}}
{{#if worker.framework}}- Framework: {{worker.framework}}{{/if}}
{{#if worker.queue_system}}- Queue: {{worker.queue_system}}{{/if}}
- Deploy: {{worker.deploy_target}}
{{/if}}

{{#if architecture.pattern == microservice}}
- Language: {{service.worker_language}}
{{#if service.worker_queue_system}}- Queue: {{service.worker_queue_system}}{{/if}}
- Deploy: {{service.worker_deploy_target}}
{{/if}}

## Description

{{#if architecture.pattern != microservice}}
{{worker.description}}
{{/if}}
{{#if architecture.pattern == microservice}}
{{service.worker_description}}
{{/if}}

## Processing Flow

> 아래 섹션은 프로젝트 시작 시 AI가 구체화합니다.

<!-- AI:INIT: During initialization, describe the processing flow:
     - Trigger mechanism (schedule/cron, event-driven, manual)
     - Message consumption pattern (poll, push, stream)
     - Processing steps (parse → validate → transform → persist)
     - Output destination (DB, another queue, API call, file)
     - Concurrency model (single-threaded, thread pool, partition-based)
-->

## Queue Topology

<!-- AI:INIT: During initialization, describe queue/topic structure:
     - Topic/queue names and their purposes
     - Partition strategy (if applicable)
     - Consumer group configuration
     - Message format (JSON, Avro, Protobuf)
     - Message schema with example payload
-->

## Error Handling

<!-- AI:INIT: During initialization, define error handling strategy:
     - Retry policy (count, backoff, max delay)
     - Dead Letter Queue (DLQ) configuration
     - Poison message handling
     - Alert triggers (consecutive failures, DLQ threshold)
-->

## Scheduling

<!-- AI:INIT: If schedule-based, define:
     - Cron expressions and their meanings
     - Timezone handling
     - Overlap prevention (lock mechanism)
     - Manual trigger support
-->
