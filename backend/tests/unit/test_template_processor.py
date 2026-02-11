"""Unit tests for the custom Handlebars-like template processor."""

import pytest

from src.application.services.template_processor import TemplateProcessor


@pytest.fixture
def processor():
    return TemplateProcessor()


class TestSimpleVariables:
    def test_simple_substitution(self, processor):
        result = processor.render("Hello {{project.name}}!", {"project": {"name": "sdwc"}})
        assert result == "Hello sdwc!"

    def test_nested_path(self, processor):
        ctx = {"backend": {"databases": [{"engine": "pg"}]}}
        result = processor.render("Lang: {{backend.language}}", ctx)
        assert result == "Lang: "

    def test_missing_variable_renders_empty(self, processor):
        result = processor.render("{{missing.path}}", {})
        assert result == ""

    def test_multiline_string_strips_trailing_newline(self, processor):
        ctx = {"project": {"description": "A cool project\n"}}
        result = processor.render("{{project.description}}", ctx)
        assert result == "A cool project"


class TestIfBlocks:
    def test_truthy_if_present(self, processor):
        result = processor.render("{{#if backend}}yes{{/if}}", {"backend": {"lang": "py"}})
        assert result == "yes"

    def test_truthy_if_absent(self, processor):
        result = processor.render("{{#if backend}}yes{{/if}}", {})
        assert result == ""

    def test_truthy_if_empty_string(self, processor):
        result = processor.render("{{#if val}}yes{{/if}}", {"val": ""})
        assert result == ""

    def test_truthy_if_empty_list(self, processor):
        result = processor.render("{{#if items}}yes{{/if}}", {"items": []})
        assert result == ""

    def test_equality(self, processor):
        ctx = {"architecture": {"pattern": "monolith"}}
        result = processor.render(
            "{{#if architecture.pattern == monolith}}mono{{/if}}", ctx
        )
        assert result == "mono"

    def test_equality_no_match(self, processor):
        ctx = {"architecture": {"pattern": "monolith"}}
        result = processor.render(
            "{{#if architecture.pattern == microservice}}msa{{/if}}", ctx
        )
        assert result == ""

    def test_inequality(self, processor):
        ctx = {"architecture": {"pattern": "monolith"}}
        result = processor.render(
            "{{#if architecture.pattern != microservice}}not-msa{{/if}}", ctx
        )
        assert result == "not-msa"

    def test_is_not_empty_with_list(self, processor):
        ctx = {"backend": {"databases": [{"engine": "pg"}]}}
        result = processor.render(
            "{{#if backend.databases is not empty}}has-db{{/if}}", ctx
        )
        assert result == "has-db"

    def test_is_not_empty_with_empty_list(self, processor):
        ctx = {"backend": {"databases": []}}
        result = processor.render(
            "{{#if backend.databases is not empty}}has-db{{/if}}", ctx
        )
        assert result == ""

    def test_inline_conditional(self, processor):
        ctx = {"architecture": {"internal_style": "hexagonal"}}
        result = processor.render(
            "{{#if architecture.internal_style}}- Style: {{architecture.internal_style}}{{/if}}",
            ctx,
        )
        assert result == "- Style: hexagonal"

    def test_nested_if(self, processor):
        ctx = {"backend": {"build_tool": "poetry", "build_tool_reason": "good"}}
        template = "{{#if backend}}{{#if backend.build_tool}}{{backend.build_tool}}{{/if}}{{/if}}"
        assert processor.render(template, ctx) == "poetry"


class TestEachBlocks:
    def test_each_strings(self, processor):
        ctx = {"services": ["backend_api", "web_ui"]}
        result = processor.render(
            "{{#each services}}- {{this}}\n{{/each}}", ctx
        )
        assert result == "- backend_api\n- web_ui\n"

    def test_each_dicts_with_db(self, processor):
        ctx = {"backend": {"databases": [
            {"engine": "postgresql", "role": "primary", "reason": "good"},
        ]}}
        result = processor.render(
            "{{#each backend.databases}}{{db.engine}} ({{db.role}}){{/each}}", ctx
        )
        assert result == "postgresql (primary)"

    def test_each_with_last(self, processor):
        ctx = {"services": ["a", "b", "c"]}
        result = processor.render(
            "{{#each services}}{{this}}{{#unless @last}}, {{/unless}}{{/each}}", ctx
        )
        assert result == "a, b, c"

    def test_each_empty_list(self, processor):
        result = processor.render("{{#each items}}x{{/each}}", {"items": []})
        assert result == ""

    def test_each_service_list_msa(self, processor):
        ctx = {"service_list": [
            {"name": "auth", "type": "backend_api"},
            {"name": "web", "type": "web_ui"},
        ]}
        result = processor.render(
            "{{#each service_list}}{{service.name}}:{{service.type}}\n{{/each}}", ctx
        )
        assert result == "auth:backend_api\nweb:web_ui\n"


class TestSpecialVariables:
    def test_adr_number_auto_increments(self, processor):
        result = processor.render(
            "ADR-{{@adr_number}} ADR-{{@adr_number}} ADR-{{@adr_number}}", {}
        )
        assert result == "ADR-002 ADR-003 ADR-004"

    def test_next_adr(self, processor):
        result = processor.render(
            "{{@adr_number}} next:{{@next_adr}}", {}
        )
        assert result == "002 next:003"

    def test_integration_branch_master_develop(self, processor):
        ctx = {"git": {"branch_strategy": "master_develop_task"}}
        result = processor.render("{{@integration_branch}}", ctx)
        assert result == "develop"

    def test_integration_branch_main_feature(self, processor):
        ctx = {"git": {"branch_strategy": "main_feature"}}
        result = processor.render("{{@integration_branch}}", ctx)
        assert result == "main"

    def test_integration_branch_trunk(self, processor):
        ctx = {"git": {"branch_strategy": "trunk"}}
        result = processor.render("{{@integration_branch}}", ctx)
        assert result == "main"

    def test_integration_branch_gitflow(self, processor):
        ctx = {"git": {"branch_strategy": "gitflow"}}
        result = processor.render("{{@integration_branch}}", ctx)
        assert result == "develop"


class TestAIComments:
    def test_ai_init_comment_preserved(self, processor):
        template = "before\n<!-- AI:INIT: fill this -->\nafter"
        result = processor.render(template, {})
        assert "<!-- AI:INIT: fill this -->" in result

    def test_ai_ongoing_comment_preserved(self, processor):
        template = "<!-- AI:ONGOING: Add libraries here -->"
        result = processor.render(template, {})
        assert "<!-- AI:ONGOING: Add libraries here -->" in result


class TestPostProcessing:
    def test_http_method_spacing(self, processor):
        result = processor.render("GET  /health\nPOST  /intakes", {})
        assert result == "GET /health\nPOST /intakes"

    def test_single_space_preserved(self, processor):
        result = processor.render("GET /health", {})
        assert result == "GET /health"

    def test_excessive_blank_lines_collapsed(self, processor):
        result = processor.render("a\n\n\n\n\nb", {})
        assert result == "a\n\n\nb"


class TestComplexTemplate:
    def test_full_project_profile_snippet(self, processor):
        ctx = {
            "project": {"name": "sdwc"},
            "architecture": {"pattern": "monolith", "internal_style": "hexagonal"},
            "services": ["backend_api", "web_ui"],
            "backend": {
                "language": "python",
                "framework": "fastapi",
                "databases": [{"engine": "postgresql", "role": "primary", "reason": "good"}],
                "api_style": "rest",
                "auth": "none",
                "deploy_target": "docker",
            },
        }
        template = """# {{project.name}}
{{#if architecture.pattern != microservice}}
{{#each services}}
- {{this}}
{{/each}}
{{/if}}
{{#if backend}}
- Language: {{backend.language}}
{{#if backend.databases is not empty}}
{{#each backend.databases}}
  - {{db.engine}} ({{db.role}})
{{/each}}
{{/if}}
{{/if}}"""
        result = processor.render(template, ctx)
        assert "# sdwc" in result
        assert "- backend_api" in result
        assert "- web_ui" in result
        assert "- Language: python" in result
        assert "- postgresql (primary)" in result
