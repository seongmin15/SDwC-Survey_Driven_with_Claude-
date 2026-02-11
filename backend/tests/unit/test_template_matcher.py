"""Unit tests for the template matcher."""

from pathlib import Path

import pytest

from src.application.services.template_matcher import TemplateMatcher

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "resources" / "templates"


@pytest.fixture
def matcher():
    return TemplateMatcher(TEMPLATES_DIR)


class TestCommonDocs:
    def test_common_docs_always_included(self, matcher):
        intake = {"architecture": {"pattern": "monolith"}, "services": []}
        mappings = matcher.match(intake)
        output_paths = [m.output_path for m in mappings]
        assert "docs/00-project-profile.md" in output_paths
        assert "docs/09-task-backlog.md" in output_paths
        assert "docs/999-roadmap-extensions.md" in output_paths

    def test_common_10_series_excluded_from_common(self, matcher):
        intake = {"architecture": {"pattern": "monolith"}, "services": []}
        mappings = matcher.match(intake)
        output_paths = [m.output_path for m in mappings]
        assert "docs/10-docker-compose-template.md" not in output_paths


class TestConditionalCommon:
    def test_docker_compose_included(self, matcher):
        intake = {
            "architecture": {"pattern": "monolith"},
            "services": [],
            "deployment": {"initial": "docker_compose"},
        }
        mappings = matcher.match(intake)
        output_paths = [m.output_path for m in mappings]
        assert "docs/10-docker-compose-template.md" in output_paths

    def test_no_deployment_no_10_series(self, matcher):
        intake = {"architecture": {"pattern": "monolith"}, "services": []}
        mappings = matcher.match(intake)
        output_paths = [m.output_path for m in mappings]
        for p in output_paths:
            assert not p.startswith("docs/10-")


class TestNonMSAServiceDocs:
    def test_backend_api_docs(self, matcher):
        intake = {
            "architecture": {"pattern": "monolith"},
            "services": ["backend_api"],
            "backend": {"databases": [{"engine": "pg"}]},
        }
        mappings = matcher.match(intake)
        output_paths = [m.output_path for m in mappings]
        assert "docs/20-api-contract.md" in output_paths
        assert "docs/21-data-design.md" in output_paths
        assert "docs/22-api-verification-contract.md" in output_paths

    def test_backend_without_db_skips_21(self, matcher):
        intake = {
            "architecture": {"pattern": "monolith"},
            "services": ["backend_api"],
            "backend": {"databases": []},
        }
        mappings = matcher.match(intake)
        output_paths = [m.output_path for m in mappings]
        assert "docs/20-api-contract.md" in output_paths
        assert "docs/21-data-design.md" not in output_paths

    def test_web_ui_docs(self, matcher):
        intake = {
            "architecture": {"pattern": "monolith"},
            "services": ["web_ui"],
        }
        mappings = matcher.match(intake)
        output_paths = [m.output_path for m in mappings]
        assert "docs/30-user-flow.md" in output_paths
        assert "docs/31-ui-verification-e2e.md" in output_paths

    def test_multiple_services(self, matcher):
        intake = {
            "architecture": {"pattern": "monolith"},
            "services": ["backend_api", "web_ui"],
            "backend": {"databases": [{"engine": "pg"}]},
        }
        mappings = matcher.match(intake)
        output_paths = [m.output_path for m in mappings]
        assert "docs/20-api-contract.md" in output_paths
        assert "docs/30-user-flow.md" in output_paths


class TestMSAServiceDocs:
    def test_msa_per_service_paths(self, matcher):
        intake = {
            "architecture": {"pattern": "microservice"},
            "service_list": [
                {"name": "auth-svc", "type": "backend_api", "databases": [{"engine": "pg"}]},
                {"name": "portal", "type": "web_ui"},
            ],
        }
        mappings = matcher.match(intake)
        output_paths = [m.output_path for m in mappings]
        assert "docs/services/auth-svc/20-api-contract.md" in output_paths
        assert "docs/services/auth-svc/21-data-design.md" in output_paths
        assert "docs/services/portal/30-user-flow.md" in output_paths

    def test_msa_backend_without_db_skips_21(self, matcher):
        intake = {
            "architecture": {"pattern": "microservice"},
            "service_list": [
                {"name": "auth-svc", "type": "backend_api", "databases": []},
            ],
        }
        mappings = matcher.match(intake)
        output_paths = [m.output_path for m in mappings]
        assert "docs/services/auth-svc/20-api-contract.md" in output_paths
        assert "docs/services/auth-svc/21-data-design.md" not in output_paths
