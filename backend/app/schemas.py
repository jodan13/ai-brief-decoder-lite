from __future__ import annotations

from datetime import datetime
from typing import cast
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities import JsonObject
from app.domain.types import RunStatus, SafeErrorCode, Severity


class BriefDecodeRequest(BaseModel):
    text: str = Field(min_length=1)


class RiskItem(BaseModel):
    risk: str
    severity: Severity
    reason: str


class StructuredBriefResult(BaseModel):
    summary: str
    goals: list[str]
    deliverables: list[str]
    constraints: list[str]
    risks: list[RiskItem]
    clarifying_questions: list[str]
    recommended_next_action: str


class DecodeRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    run_id: UUID
    status: RunStatus
    input_text: str
    structured_result: StructuredBriefResult | None
    raw_provider_output: str | None
    safe_error_code: SafeErrorCode | None
    safe_error_message: str | None
    created_at: datetime
    updated_at: datetime


class ErrorResponse(BaseModel):
    error_code: SafeErrorCode
    message: str
    run_id: UUID | None = None


def result_to_json(result: StructuredBriefResult) -> JsonObject:
    return cast(JsonObject, result.model_dump(mode="json"))


def result_from_json(value: JsonObject | None) -> StructuredBriefResult | None:
    if value is None:
        return None
    return StructuredBriefResult.model_validate(value)
