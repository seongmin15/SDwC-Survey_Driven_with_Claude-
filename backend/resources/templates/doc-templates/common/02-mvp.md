# MVP

## MVP Scope

{{#each scope.in_scope}}
- {{this}}
{{/each}}

## Out of Scope

> 아래 항목은 MVP에 포함하지 않으며 `docs/999-roadmap-extensions.md`에 기록됩니다.

{{scope.out_of_scope}}

## Success Criteria

{{scope.success_criteria}}

## Constraints

- Stage: MVP
- Architecture: {{architecture.pattern}}
- Services: {{#each services}}{{this}}{{#unless @last}}, {{/unless}}{{/each}}
- Deployment: {{deployment.initial}}
- Auth: {{backend.auth}}
- Observability: {{#if observability.included_in_mvp}}포함{{else}}최소 (health/ready만){{/if}}
