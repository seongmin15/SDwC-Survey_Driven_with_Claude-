# Pipeline Design

> 이 문서는 프로젝트 시작 시 AI가 상세를 채웁니다.

## Overview

{{#if architecture.pattern != microservice}}
- Language: {{pipeline.language}}
- Framework: {{pipeline.framework}}
- Deploy: {{pipeline.deploy_target}}
{{/if}}
{{#if architecture.pattern == microservice}}
- Language: {{service.pipeline_language}}
- Framework: {{service.pipeline_framework}}
- Deploy: {{service.pipeline_deploy_target}}
{{/if}}

## Pipeline Description

{{#if architecture.pattern != microservice}}
{{pipeline.description}}
{{/if}}
{{#if architecture.pattern == microservice}}
{{service.pipeline_description}}
{{/if}}

## DAG / Flow Structure

<!-- AI:INIT: During initialization, define pipeline structure:
     - Pipeline stages (Extract → Transform → Load or similar)
     - Stage dependencies (DAG structure)
     - Parallel vs sequential execution paths
     - Branching/conditional paths (if applicable)
-->

## Data Sources

<!-- AI:INIT: During initialization, define input sources:
     - Source name, type (DB, API, file, stream)
     - Connection details (host, credentials reference)
     - Data format (CSV, JSON, Parquet, DB table)
     - Volume estimate (rows/day, GB/day)
     - Freshness requirement (real-time, hourly, daily)
-->

## Data Sinks

<!-- AI:INIT: During initialization, define output destinations:
     - Destination name, type (DB, data warehouse, file, API)
     - Write mode (append, upsert, overwrite)
     - Partitioning strategy (date, key-based)
     - Retention policy
-->

## Scheduling

<!-- AI:INIT: During initialization, define scheduling:
     - Schedule (cron expression, event-triggered, manual)
     - Dependency on upstream data availability
     - SLA (expected completion time)
     - Backfill strategy (how to reprocess historical data)
-->

## Error Handling

<!-- AI:INIT: During initialization, define error handling:
     - Stage-level retry policy
     - Partial failure handling (skip bad records vs fail entire batch)
     - Alerting (on failure, SLA breach, data quality issue)
     - Manual intervention procedures
-->
