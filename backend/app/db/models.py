from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.domain.entities import JsonObject


class Base(DeclarativeBase):
    pass


class DecodeRunModel(Base):
    __tablename__ = "decode_runs"

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    input_text: Mapped[str] = mapped_column(Text, nullable=False)
    structured_result: Mapped[JsonObject | None] = mapped_column(JSONB, nullable=True)
    raw_provider_output: Mapped[str | None] = mapped_column(Text, nullable=True)
    safe_error_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    safe_error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
