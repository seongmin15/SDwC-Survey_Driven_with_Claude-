# Roadmap & Extensions

> MVP 범위 밖의 기능은 여기에 기록합니다.
> AI가 개발 중 발견한 개선점도 여기에 제안합니다.

## Out of Scope

{{scope.out_of_scope}}

{{#if deployment.future}}
## Future Deployment

{{#each deployment.future}}
- {{this}}
{{/each}}
{{/if}}

{{#if extensions.future_plans}}
## Planned Extensions

> Out of Scope 항목과 중복되는 항목은 제외합니다. 아래는 추가 확장 계획만 기술합니다.

<!-- AI:INIT: Review the list below and remove any items already listed in "Out of Scope" above.
     Keep only items that are genuinely additional plans beyond the MVP exclusion list.
     If all items are duplicates, write "Out of Scope 항목 참조" and remove this comment.
-->
{{extensions.future_plans}}
{{/if}}

{{#if extensions.notion_enabled}}
## Notion Integration

- 작업 내역 Notion 동기화 예정
{{/if}}

## AI-Discovered Improvements

> 아래는 AI가 개발 중 발견한 개선점입니다. 사용자 승인 후 Backlog로 이동 가능합니다.

*(빈 상태로 시작)*
