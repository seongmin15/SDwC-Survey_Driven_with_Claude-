"""Initial schema: projects and events tables

Revision ID: 001
Revises:
Create Date: 2026-02-11
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("project_name", sa.String(100), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("intake_data", JSONB, nullable=False),
        sa.Column("zip_path", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("status IN ('intake_saved', 'generated')", name="chk_projects_status"),
    )
    op.create_index("idx_projects_status", "projects", ["status"])

    op.create_table(
        "events",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("project_id", UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("payload", JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_events_project_id", "events", ["project_id"])
    op.create_index("idx_events_event_type", "events", ["event_type"])


def downgrade() -> None:
    op.drop_index("idx_events_event_type", table_name="events")
    op.drop_index("idx_events_project_id", table_name="events")
    op.drop_table("events")
    op.drop_index("idx_projects_status", table_name="projects")
    op.drop_table("projects")
