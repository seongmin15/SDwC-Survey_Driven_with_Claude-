# Worker Verification — Performance

> 이 문서는 프로젝트 시작 시 AI가 테스트 케이스를 채웁니다.

## Overview

Worker의 처리 성능과 확장성을 검증하는 테스트 명세입니다.

## Test Categories

### 처리량 (Throughput)

<!-- AI:INIT: During initialization, fill test cases:
     - Messages per second under normal load
     - Sustained processing over extended period
     - Batch size optimization (if applicable)
-->

| ID | Scenario | Input | Expected | Status |
|----|----------|-------|----------|--------|

### 지연 시간 (Latency)

<!-- AI:INIT: During initialization, fill test cases:
     - End-to-end latency: message published → processing complete
     - Processing time per message
     - Queue wait time under load
-->

| ID | Scenario | Input | Expected | Status |
|----|----------|-------|----------|--------|

### 리소스 사용 (Resource Usage)

<!-- AI:INIT: During initialization, fill test cases:
     - Memory usage under sustained load
     - CPU utilization pattern
     - DB connection pool usage
     - Network I/O pattern
-->

| ID | Scenario | Input | Expected | Status |
|----|----------|-------|----------|--------|

### 확장성 (Scalability)

<!-- AI:INIT: During initialization, fill test cases:
     - Consumer instance scaling (1 → N)
     - Partition rebalancing behavior
     - Linear throughput increase with additional consumers
-->

| ID | Scenario | Input | Expected | Status |
|----|----------|-------|----------|--------|
