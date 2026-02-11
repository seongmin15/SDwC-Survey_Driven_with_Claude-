# Skill Template Rules

> **CRITICAL: All generated SKILL.md files MUST be written entirely in English.**
> **Do NOT write any section in Korean or any other language.**
> **This includes: Context, Rules, Patterns, Anti-patterns, Checklist — all English.**

## Overview

Templates in this directory are skeletons used to generate per-service skill files.
Generated skills are placed at `skills/{service-name}/SKILL.md` for Claude Code to reference.

## Template Syntax

### Variable Substitution

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{project_name}}` | Project name | `SDwC` |
| `{{service_name}}` | Current service name | `backend_api` |
| `{{doc_range}}` | Service doc number range | `20~29` |
| `{{Xn}}` | Nth doc in service range | `{{X0}}`=20, `{{X1}}`=21 |

### Content Injection

| Placeholder | Description |
|-------------|-------------|
| `{{source:filename}}` | Extract key content from docs file |
| `{{source:filename → field}}` | Extract specific field only |
| `{{checklist:filename}}` | Extract checklist items from verification doc |
| `{{cross_cutting}}` | Inject 10-series docs content (if present) |
| `{{detect:attribute}}` | Auto-detect tech stack from docs |

### Block Directives

| Block | Description | Method |
|-------|-------------|--------|
| `{{fixed}}...{{/fixed}}` | Output as-is, never modify. **Place once at file top only.** | Text copy |
| `{{generate}}...{{/generate}}` | AI generates based on docs | AI fill |

## Section Structure

Every skill MUST contain these 5 sections in this order:

```
## Context        Target, usage timing, tech stack
## Rules          Mandatory rules (reject on violation)
## Patterns       Recommended code/design patterns (with examples)
## Anti-patterns  What NOT to do (with reasons)
## Checklist      Pre-completion verification items
```

## Doc Number Ranges

```
00~09   Common conventions (project meta, collaboration, git, backlog)
10~19   Common conditional (deployment templates — docker-compose, k8s, etc.)
20~29   Service 1
30~39   Service 2
40~49   Service 3 ...
90~99   Roadmap/extensions (not a skill generation target)
```

## Composition Rules

Each service skill is composed in this order:

```
1. Select role template (matching service type)
2. Check applicable concerns for that role
3. Inject concern content into designated sections of role template
4. Inject cross_cutting (10-series) content into Context/Rules
5. Substitute {{source}}, {{checklist}} from service doc range
6. Fill {{generate}} blocks via AI
```

## Concern Injection Targets

| Concern | Injection Section | Condition |
|---------|------------------|-----------|
| database | Rules, Anti-patterns | `databases[]` is not empty |
| testing | Checklist | Always |
| deploy | Checklist | Always |
| auth | Rules | `auth != none` |

### Injection Process

1. Locate `<!-- concern:{name} injection point -->` markers in the role template.
2. Check the concern's activation condition (see table above).
3. If condition is met: read `concerns/{name}.md`, extract the section matching the marker's parent heading (e.g., if marker is under `## Rules`, extract `## Rules` content from concern file).
4. Replace the marker with the extracted content.
5. If condition is NOT met: remove the marker comment entirely (do not leave empty markers).
