"""Orchestrates full document generation from intake_data."""

from pathlib import Path
from typing import Any

import yaml

from src.application.services.template_matcher import TEMPLATES_DIR, TemplateMatcher
from src.application.services.template_processor import TemplateProcessor


def _str_representer(dumper: yaml.Dumper, data: str) -> yaml.ScalarNode:
    """Use block scalar style for multi-line strings."""
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, _str_representer)


class DocumentGenerator:
    def __init__(self, templates_dir: Path | None = None) -> None:
        self._templates_dir = templates_dir or TEMPLATES_DIR
        self._matcher = TemplateMatcher(self._templates_dir)
        self._processor = TemplateProcessor()

    def generate(self, intake_data: dict[str, Any]) -> dict[str, str]:
        """Generate all project files from intake_data.

        Returns dict of {output_path: rendered_content}.
        """
        files: dict[str, str] = {}

        # 1. Match and render doc-templates
        mappings = self._matcher.match(intake_data)
        for mapping in mappings:
            template_path = self._templates_dir / "doc-templates" / mapping.template_path
            template_content = template_path.read_text(encoding="utf-8")
            rendered = self._processor.render(template_content, intake_data)
            files[mapping.output_path] = rendered

        # 2. Generate CLAUDE.md from CLAUDE_BASE.md
        claude_base_path = self._templates_dir / "CLAUDE_BASE.md"
        if claude_base_path.exists():
            claude_template = claude_base_path.read_text(encoding="utf-8")
            files["CLAUDE.md"] = self._processor.render(claude_template, intake_data)

        # 3. Copy skill-templates as-is to .sdwc/skill-templates/
        skill_dir = self._templates_dir / "skill-templates"
        if skill_dir.exists():
            for f in skill_dir.rglob("*"):
                if f.is_file():
                    rel = f.relative_to(skill_dir)
                    output_path = f".sdwc/skill-templates/{rel.as_posix()}"
                    files[output_path] = f.read_text(encoding="utf-8")

        # 4. Save intake_data as YAML
        files["docs/intake_data.yaml"] = yaml.dump(
            intake_data,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )

        return files
