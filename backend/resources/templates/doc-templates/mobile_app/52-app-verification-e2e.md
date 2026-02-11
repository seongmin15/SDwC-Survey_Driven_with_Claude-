# App Verification — E2E

> 이 문서는 프로젝트 시작 시 AI가 테스트 케이스를 채웁니다.

## Overview

앱의 주요 사용자 시나리오를 end-to-end로 검증하는 테스트 명세입니다.

## Test Categories

### 핵심 플로우 (Core Flows)

<!-- AI:INIT: During initialization, fill test cases:
     - Onboarding → Login → Main screen
     - Primary user journey (the main thing the app does)
     - Logout / session expiry handling
-->

| ID | Scenario | Steps | Expected | Status |
|----|----------|-------|----------|--------|

### 네비게이션 (Navigation)

<!-- AI:INIT: During initialization, fill test cases:
     - Tab switching
     - Deep stack navigation and back
     - Deep link handling
     - Gesture navigation (swipe back, pull to refresh)
-->

| ID | Scenario | Steps | Expected | Status |
|----|----------|-------|----------|--------|

### 네트워크 (Network)

<!-- AI:INIT: During initialization, fill test cases:
     - Normal API call → success
     - Network offline → appropriate fallback
     - Slow network → loading states, timeout handling
     - Token expired during request → auto-refresh → retry
-->

| ID | Scenario | Steps | Expected | Status |
|----|----------|-------|----------|--------|

### 플랫폼 특화 (Platform Specific)

<!-- AI:INIT: During initialization, fill test cases:
     - App backgrounding and resuming
     - Push notification tap → correct screen
     - Permission denied → graceful handling
     - Low memory warning → no crash
     - Screen rotation (if supported)
-->

| ID | Scenario | Steps | Expected | Status |
|----|----------|-------|----------|--------|
