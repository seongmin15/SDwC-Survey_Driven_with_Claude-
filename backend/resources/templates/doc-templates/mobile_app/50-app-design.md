# App Design

> 이 문서는 프로젝트 시작 시 AI가 상세를 채웁니다.

## Overview

{{#if architecture.pattern != microservice}}
- Platform: {{mobile.platform}}
- Language: {{mobile.language}}
- Framework: {{mobile.framework}}
- Deploy: {{mobile.deploy_target}}
{{/if}}
{{#if architecture.pattern == microservice}}
- Platform: {{service.mobile_platform}}
- Language: {{service.mobile_language}}
- Framework: {{service.mobile_framework}}
- Deploy: {{service.mobile_deploy_target}}
{{/if}}

## Screen Structure

<!-- AI:INIT: During initialization, define screen hierarchy:
     - Main navigation structure (tab bar, drawer, stack)
     - Screen list with purpose
     - Screen hierarchy (parent → child relationships)
-->

## Navigation Flow

<!-- AI:INIT: During initialization, define navigation:
     - Entry point (splash → onboarding → main)
     - Main flow diagram
     - Deep linking support (if applicable)
     - Back navigation behavior
-->

## API Integration

<!-- AI:INIT: During initialization, define API connection:
     - Base URL configuration (per environment)
     - Authentication flow (token storage, refresh)
     - Offline behavior (cache strategy, sync on reconnect)
     - Error handling (network error → retry/offline mode)
-->

## State Management

<!-- AI:INIT: During initialization, define state architecture:
     - State management approach (Redux, MobX, Provider, etc.)
     - Global state vs local state boundaries
     - Persistence strategy (which state survives app restart)
     - Cache invalidation policy
-->

## Platform Specifics

<!-- AI:INIT: During initialization, define platform-specific concerns:
     - Permissions required (camera, location, notifications, etc.)
     - Push notification setup
     - Background task handling
     - App lifecycle management
-->
