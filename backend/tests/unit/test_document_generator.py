"""Unit tests for the document generator."""

from pathlib import Path

import pytest

from src.application.services.document_generator import DocumentGenerator

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "resources" / "templates"

SAMPLE_INTAKE = {
    "project": {"name": "test-app", "description": "A test app\n", "target_users": "devs\n", "core_value": "fast\n"},
    "scope": {
        "in_scope": ["feature A", "feature B"],
        "out_of_scope": "nothing\n",
        "success_criteria": "works\n",
    },
    "architecture": {"pattern": "monolith", "pattern_reason": "simple\n", "internal_style": "hexagonal", "internal_style_reason": "testable\n"},
    "services": ["backend_api", "web_ui"],
    "backend": {
        "language": "python",
        "framework": "fastapi",
        "framework_reason": "fast\n",
        "build_tool": "poetry",
        "build_tool_reason": "good\n",
        "databases": [{"engine": "postgresql", "role": "primary", "reason": "solid\n"}],
        "api_style": "rest",
        "auth": "none",
        "deploy_target": "docker",
        "main_endpoints": "POST /intakes\nGET /health\n",
        "main_entities": "projects\nevents\n",
    },
    "web": {
        "language": "typescript",
        "framework": "react",
        "framework_reason": "popular\n",
        "css_strategy": "tailwind",
        "build_tool": "pnpm",
        "build_tool_reason": "fast\n",
        "main_pages": "Survey\nGenerate\nComplete\n",
        "page_flow": "Survey → Generate → Complete\n",
        "deploy_target": "same_server",
        "connected_api": "backend_api",
    },
    "collaboration": {
        "methodology": "kanban",
        "task_review_minutes": 30,
        "wip_limit": 2,
        "use_subagent": False,
        "model_routing": "opus_sonnet",
        "tdd": True,
    },
    "git": {"branch_strategy": "master_develop_task", "pr_by": "user"},
    "deployment": {"initial": "docker_compose", "initial_reason": "simple\n"},
    "observability": {"included_in_mvp": False},
    "extensions": {"notion_enabled": False, "future_plans": "CLI\n"},
}


@pytest.fixture
def generator():
    return DocumentGenerator(TEMPLATES_DIR)


class TestDocumentGeneration:
    def test_generates_claude_md(self, generator):
        files = generator.generate(SAMPLE_INTAKE)
        assert "CLAUDE.md" in files
        assert "# CLAUDE.md" in files["CLAUDE.md"]

    def test_generates_common_docs(self, generator):
        files = generator.generate(SAMPLE_INTAKE)
        assert "docs/00-project-profile.md" in files
        assert "docs/09-task-backlog.md" in files
        assert "docs/999-roadmap-extensions.md" in files

    def test_generates_conditional_10_doc(self, generator):
        files = generator.generate(SAMPLE_INTAKE)
        assert "docs/10-docker-compose-template.md" in files

    def test_generates_backend_docs(self, generator):
        files = generator.generate(SAMPLE_INTAKE)
        assert "docs/20-api-contract.md" in files
        assert "docs/21-data-design.md" in files

    def test_generates_web_docs(self, generator):
        files = generator.generate(SAMPLE_INTAKE)
        assert "docs/30-user-flow.md" in files

    def test_generates_skill_templates(self, generator):
        files = generator.generate(SAMPLE_INTAKE)
        skill_files = [k for k in files if k.startswith(".sdwc/skill-templates/")]
        assert len(skill_files) > 0
        assert ".sdwc/skill-templates/_meta.md" in files

    def test_generates_intake_data_yaml(self, generator):
        files = generator.generate(SAMPLE_INTAKE)
        assert "docs/intake_data.yaml" in files
        content = files["docs/intake_data.yaml"]
        assert "test-app" in content

    def test_variable_substitution_in_docs(self, generator):
        files = generator.generate(SAMPLE_INTAKE)
        profile = files["docs/00-project-profile.md"]
        assert "test-app" in profile
        assert "{{project.name}}" not in profile

    def test_conditional_blocks_in_claude_md(self, generator):
        files = generator.generate(SAMPLE_INTAKE)
        claude = files["CLAUDE.md"]
        # TDD is true → should have TDD section
        assert "TDD" in claude
        # model_routing is opus_sonnet → should have Model Routing section
        assert "Model Routing" in claude
        # use_subagent is false → should NOT have Sub-Agent section
        assert "Sub-Agent Policy" not in claude

    def test_branch_strategy_in_claude_md(self, generator):
        files = generator.generate(SAMPLE_INTAKE)
        claude = files["CLAUDE.md"]
        # master_develop_task → should have develop branch references
        assert "develop" in claude
        # Should NOT have main_feature or trunk specific sections
        assert "main_feature" not in claude.replace("master_develop_task", "")

    def test_no_msa_docs_for_monolith(self, generator):
        files = generator.generate(SAMPLE_INTAKE)
        service_docs = [k for k in files if "docs/services/" in k]
        assert len(service_docs) == 0

    def test_no_residual_handlebars_in_common_docs(self, generator):
        """Verify no unsubstituted {{...}} remain (except AI comments)."""
        import re
        files = generator.generate(SAMPLE_INTAKE)
        tag_re = re.compile(r"\{\{.*?\}\}")
        for path, content in files.items():
            if not path.startswith("docs/") and path != "CLAUDE.md":
                continue
            if path == "docs/intake_data.yaml":
                continue
            matches = tag_re.findall(content)
            assert len(matches) == 0, f"Residual tags in {path}: {matches}"
