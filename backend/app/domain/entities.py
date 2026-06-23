from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.types import RunStatus, SafeErrorCode

type JsonValue = str | int | float | bool | None | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]


@dataclass(frozen=True)
class DecodeRun:
    id: UUID
    status: RunStatus
    input_text: str
    structured_result: JsonObject | None
    raw_provider_output: str | None
    safe_error_code: SafeErrorCode | None
    safe_error_message: str | None
    created_at: datetime
    updated_at: datetime
