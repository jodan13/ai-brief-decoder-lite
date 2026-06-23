"""create decode_runs table

Revision ID: 202606230001
Revises:
Create Date: 2026-06-23 00:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "202606230001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "decode_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("input_text", sa.Text(), nullable=False),
        sa.Column("structured_result", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("raw_provider_output", sa.Text(), nullable=True),
        sa.Column("safe_error_code", sa.String(length=64), nullable=True),
        sa.Column("safe_error_message", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_decode_runs_created_at", "decode_runs", ["created_at"])
    op.create_index("ix_decode_runs_status", "decode_runs", ["status"])


def downgrade() -> None:
    op.drop_index("ix_decode_runs_status", table_name="decode_runs")
    op.drop_index("ix_decode_runs_created_at", table_name="decode_runs")
    op.drop_table("decode_runs")
