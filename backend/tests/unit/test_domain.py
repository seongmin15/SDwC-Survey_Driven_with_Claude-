"""
Unit tests for Domain layer.
Verification IDs: C-021, C-022
"""
import ast
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pytest

DOMAIN_ROOT = Path(__file__).resolve().parents[2] / "src" / "domain"
FORBIDDEN_MODULES = {"fastapi", "sqlalchemy", "uvicorn", "httpx", "psycopg", "alembic"}
FORBIDDEN_ADAPTER_PREFIXES = {"src.adapters", "src.config"}


class TestDomainNoDependency:
    """C-021: Domain 레이어가 FastAPI/SQLAlchemy import 없음"""

    def _collect_imports(self, filepath: Path) -> list[str]:
        """Parse a Python file and return all imported module names."""
        source = filepath.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(filepath))
        modules = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    modules.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    modules.append(node.module)
        return modules

    def test_domain_has_no_framework_imports(self):
        """C-021: Domain 레이어 파일에서 FastAPI/SQLAlchemy import가 없어야 한다."""
        violations = []
        for py_file in DOMAIN_ROOT.rglob("*.py"):
            if py_file.name == "__init__.py" and py_file.stat().st_size == 0:
                continue
            for module in self._collect_imports(py_file):
                top_level = module.split(".")[0]
                if top_level in FORBIDDEN_MODULES:
                    violations.append(f"{py_file.relative_to(DOMAIN_ROOT)}: {module}")
        assert violations == [], f"Forbidden imports in domain layer: {violations}"

    def test_domain_has_no_adapter_imports(self):
        """C-022: Domain 레이어는 adapters/config에 의존하지 않아야 한다."""
        violations = []
        for py_file in DOMAIN_ROOT.rglob("*.py"):
            if py_file.name == "__init__.py" and py_file.stat().st_size == 0:
                continue
            for module in self._collect_imports(py_file):
                for prefix in FORBIDDEN_ADAPTER_PREFIXES:
                    if module.startswith(prefix):
                        violations.append(f"{py_file.relative_to(DOMAIN_ROOT)}: {module}")
        assert violations == [], f"Domain depends on outer layers: {violations}"


class TestProjectEntity:
    """Project 엔티티 테스트"""

    def test_create_project(self):
        from src.domain.entities.project import Project

        now = datetime.now(timezone.utc)
        project = Project(
            id=uuid.uuid4(),
            project_name="test-project",
            status="intake_saved",
            intake_data={"project": {"name": "test-project"}},
            zip_path=None,
            created_at=now,
            generated_at=None,
        )
        assert project.project_name == "test-project"
        assert project.status == "intake_saved"
        assert project.zip_path is None
        assert project.generated_at is None

    def test_project_fields_match_spec(self):
        """Project 엔티티 필드가 data-design 스펙과 일치한다."""
        from src.domain.entities.project import Project
        import dataclasses

        field_names = {f.name for f in dataclasses.fields(Project)}
        expected = {"id", "project_name", "status", "intake_data", "zip_path", "created_at", "generated_at"}
        assert field_names == expected


class TestEventEntity:
    """Event 엔티티 테스트"""

    def test_create_event(self):
        from src.domain.entities.event import Event

        now = datetime.now(timezone.utc)
        event = Event(
            id=uuid.uuid4(),
            project_id=uuid.uuid4(),
            event_type="intake_saved",
            payload={"key": "value"},
            created_at=now,
        )
        assert event.event_type == "intake_saved"
        assert event.payload == {"key": "value"}

    def test_event_fields_match_spec(self):
        """Event 엔티티 필드가 data-design 스펙과 일치한다."""
        from src.domain.entities.event import Event
        import dataclasses

        field_names = {f.name for f in dataclasses.fields(Event)}
        expected = {"id", "project_id", "event_type", "payload", "created_at"}
        assert field_names == expected


class TestRepositoryPorts:
    """Repository 포트(인터페이스) 테스트"""

    def test_project_repository_is_abstract(self):
        from src.domain.ports.repositories import ProjectRepository
        with pytest.raises(TypeError):
            ProjectRepository()

    def test_project_repository_has_required_methods(self):
        from src.domain.ports.repositories import ProjectRepository
        import inspect

        methods = {name for name, _ in inspect.getmembers(ProjectRepository, predicate=inspect.isfunction)}
        assert "create" in methods
        assert "get_by_id" in methods
        assert "update_status" in methods

    def test_event_repository_is_abstract(self):
        from src.domain.ports.repositories import EventRepository
        with pytest.raises(TypeError):
            EventRepository()

    def test_event_repository_has_required_methods(self):
        from src.domain.ports.repositories import EventRepository
        import inspect

        methods = {name for name, _ in inspect.getmembers(EventRepository, predicate=inspect.isfunction)}
        assert "create" in methods
        assert "list_by_project_id" in methods


class TestDomainExceptions:
    """도메인 예외 테스트"""

    def test_project_not_found(self):
        from src.domain.exceptions import ProjectNotFound
        exc = ProjectNotFound(project_id=uuid.uuid4())
        assert "project_id" in str(exc) or hasattr(exc, "project_id")

    def test_already_generated(self):
        from src.domain.exceptions import AlreadyGenerated
        exc = AlreadyGenerated(project_id=uuid.uuid4())
        assert isinstance(exc, Exception)

    def test_not_yet_generated(self):
        from src.domain.exceptions import NotYetGenerated
        exc = NotYetGenerated(project_id=uuid.uuid4())
        assert isinstance(exc, Exception)
