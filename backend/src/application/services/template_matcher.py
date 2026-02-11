"""Selects which templates to generate based on intake_data and generation rules."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

TEMPLATES_DIR = Path(__file__).resolve().parents[3] / "resources" / "templates"

SERVICE_TYPE_TO_DIR: dict[str, str] = {
    "backend_api": "backend_api",
    "web_ui": "web_ui",
    "worker": "worker",
    "mobile_app": "mobile_app",
    "data_pipeline": "data_pipeline",
}

DEPLOYMENT_TO_TEMPLATE: dict[str, str] = {
    "docker_compose": "10-docker-compose-template.md",
}


@dataclass
class TemplateMapping:
    template_path: str  # relative to doc-templates/
    output_path: str  # relative to project root


class TemplateMatcher:
    def __init__(self, templates_dir: Path | None = None) -> None:
        self._templates_dir = templates_dir or TEMPLATES_DIR

    def match(self, intake_data: dict[str, Any]) -> list[TemplateMapping]:
        mappings: list[TemplateMapping] = []

        architecture = intake_data.get("architecture", {})
        is_msa = architecture.get("pattern") == "microservice"

        # 3.1 Common documents (always)
        mappings.extend(self._common_docs())

        # 3.1.1 Conditional common docs (10-series)
        mappings.extend(self._conditional_common_docs(intake_data))

        if is_msa:
            mappings.extend(self._msa_service_docs(intake_data))
        else:
            mappings.extend(self._non_msa_service_docs(intake_data))

        return mappings

    def _common_docs(self) -> list[TemplateMapping]:
        common_dir = self._templates_dir / "doc-templates" / "common"
        mappings: list[TemplateMapping] = []
        for f in sorted(common_dir.glob("*.md")):
            if f.name.startswith("10-"):
                continue  # handled by _conditional_common_docs
            mappings.append(TemplateMapping(
                template_path=f"common/{f.name}",
                output_path=f"docs/{f.name}",
            ))
        return mappings

    def _conditional_common_docs(self, intake_data: dict[str, Any]) -> list[TemplateMapping]:
        deployment = intake_data.get("deployment", {})
        initial = deployment.get("initial", "")
        mappings: list[TemplateMapping] = []

        if initial in DEPLOYMENT_TO_TEMPLATE:
            template_name = DEPLOYMENT_TO_TEMPLATE[initial]
            template_file = self._templates_dir / "doc-templates" / "common" / template_name
            if template_file.exists():
                mappings.append(TemplateMapping(
                    template_path=f"common/{template_name}",
                    output_path=f"docs/{template_name}",
                ))

        return mappings

    def _non_msa_service_docs(self, intake_data: dict[str, Any]) -> list[TemplateMapping]:
        services = intake_data.get("services", [])
        backend = intake_data.get("backend", {})
        mappings: list[TemplateMapping] = []

        for service_type in services:
            dir_name = SERVICE_TYPE_TO_DIR.get(service_type)
            if not dir_name:
                continue

            service_dir = self._templates_dir / "doc-templates" / dir_name
            if not service_dir.exists():
                continue

            for f in sorted(service_dir.glob("*.md")):
                # 21-data-design.md only if databases not empty
                if f.name == "21-data-design.md":
                    databases = backend.get("databases", [])
                    if not databases:
                        continue

                mappings.append(TemplateMapping(
                    template_path=f"{dir_name}/{f.name}",
                    output_path=f"docs/{f.name}",
                ))

        return mappings

    def _msa_service_docs(self, intake_data: dict[str, Any]) -> list[TemplateMapping]:
        service_list = intake_data.get("service_list", [])
        mappings: list[TemplateMapping] = []

        for service in service_list:
            service_name = service.get("name", "")
            service_type = service.get("type", "")
            dir_name = SERVICE_TYPE_TO_DIR.get(service_type)
            if not dir_name:
                continue

            service_dir = self._templates_dir / "doc-templates" / dir_name
            if not service_dir.exists():
                continue

            for f in sorted(service_dir.glob("*.md")):
                if f.name == "21-data-design.md":
                    databases = service.get("databases", [])
                    if not databases:
                        continue

                mappings.append(TemplateMapping(
                    template_path=f"{dir_name}/{f.name}",
                    output_path=f"docs/services/{service_name}/{f.name}",
                ))

        return mappings
