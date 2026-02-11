"""
Security tests for environment configuration.
Verification IDs: S-009, S-010, S-011, S-012
"""
import re
from pathlib import Path

import pytest

# Project root directories
PROJECT_ROOT = Path(__file__).resolve().parents[3]  # SDwC/
BACKEND_ROOT = PROJECT_ROOT / "backend"
BACKEND_SRC = BACKEND_ROOT / "src"


# ── S-009: No hardcoded secrets in source code ──


SECRET_PATTERNS = [
    re.compile(r'(?:password|passwd|pwd)\s*=\s*["\'][^"\']+["\']', re.IGNORECASE),
    re.compile(r'(?:secret|api_key|apikey|token)\s*=\s*["\'][^"\']+["\']', re.IGNORECASE),
    re.compile(r'(?:aws_access_key|aws_secret)\s*=\s*["\'][^"\']+["\']', re.IGNORECASE),
    re.compile(r'postgresql://\w+:\w+@', re.IGNORECASE),
]

# Patterns that are acceptable (e.g., environment variable lookups, test fixtures)
ALLOWLIST_PATTERNS = [
    re.compile(r'(?:os\.environ|getenv|get_settings|BaseSettings|Field\()', re.IGNORECASE),
    re.compile(r'(?:POSTGRESQL_URL|DATABASE_URL)\s*:', re.IGNORECASE),  # Pydantic field declaration
    re.compile(r'#\s*', re.IGNORECASE),  # Comments
    re.compile(r'(?:example|placeholder|dummy|test|fake)', re.IGNORECASE),
]


def _scan_source_for_secrets():
    """Scan all Python source files for hardcoded secrets."""
    violations = []
    for py_file in BACKEND_SRC.rglob("*.py"):
        lines = py_file.read_text(encoding="utf-8").splitlines()
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(stripped):
                    # Check if it matches any allowlist pattern
                    if any(ap.search(stripped) for ap in ALLOWLIST_PATTERNS):
                        continue
                    violations.append(f"{py_file.relative_to(PROJECT_ROOT)}:{line_num}: {stripped}")
    return violations


def test_no_hardcoded_secrets_in_source():
    """S-009: No hardcoded secrets exist in backend source code."""
    violations = _scan_source_for_secrets()
    assert violations == [], f"Hardcoded secrets found:\n" + "\n".join(violations)


# ── S-010: Docker image excludes .env ──


def test_dockerignore_excludes_env():
    """S-010: .dockerignore must include .env to prevent it from being copied into Docker image."""
    dockerignore = BACKEND_ROOT / ".dockerignore"
    assert dockerignore.exists(), "backend/.dockerignore does not exist"

    content = dockerignore.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]

    env_excluded = any(
        line in (".env", ".env*", ".env.*", "*.env") for line in lines
    )
    assert env_excluded, f".env is not excluded in backend/.dockerignore. Lines: {lines}"


# ── S-011: No secrets/PII in log output ──


LOG_SENSITIVE_PATTERNS = [
    re.compile(r'(?:logging|logger|log)\.\w+\(.*(?:password|secret|token|api_key|credential)', re.IGNORECASE),
    re.compile(r'print\(.*(?:password|secret|token|api_key|credential)', re.IGNORECASE),
]


def _scan_source_for_log_secrets():
    """Scan source files for logging statements that might include sensitive data."""
    violations = []
    for py_file in BACKEND_SRC.rglob("*.py"):
        lines = py_file.read_text(encoding="utf-8").splitlines()
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            for pattern in LOG_SENSITIVE_PATTERNS:
                if pattern.search(stripped):
                    violations.append(f"{py_file.relative_to(PROJECT_ROOT)}:{line_num}: {stripped}")
    return violations


def test_no_secrets_in_log_statements():
    """S-011: Log statements must not include secrets or PII."""
    violations = _scan_source_for_log_secrets()
    assert violations == [], f"Sensitive data in log statements:\n" + "\n".join(violations)


# ── S-012: .gitignore includes required entries ──


REQUIRED_GITIGNORE_ENTRIES = [".env", "__pycache__/", "node_modules/"]


def test_gitignore_includes_required_entries():
    """S-012: .gitignore must include .env, __pycache__/, node_modules/."""
    gitignore = PROJECT_ROOT / ".gitignore"
    assert gitignore.exists(), ".gitignore does not exist"

    content = gitignore.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines()]

    for entry in REQUIRED_GITIGNORE_ENTRIES:
        assert entry in lines, f"Missing required entry in .gitignore: {entry}"
