from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.domain.entities import DecodeRun, JsonObject
from app.domain.types import SafeErrorCode
from app.repositories.decode_runs import DecodeRunRepository


class InMemoryDecodeRunRepository(DecodeRunRepository):
    def __init__(self) -> None:
        self.runs: dict[UUID, DecodeRun] = {}

    async def create_running(self, input_text: str) -> DecodeRun:
        now = datetime.now(UTC)
        run = DecodeRun(
            id=uuid4(),
            status="running",
            input_text=input_text,
            structured_result=None,
            raw_provider_output=None,
            safe_error_code=None,
            safe_error_message=None,
            created_at=now,
            updated_at=now,
        )
        self.runs[run.id] = run
        return run

    async def mark_succeeded(
        self,
        run_id: UUID,
        structured_result: JsonObject,
        raw_provider_output: str,
    ) -> DecodeRun:
        run = replace(
            self.runs[run_id],
            status="succeeded",
            structured_result=structured_result,
            raw_provider_output=raw_provider_output,
            safe_error_code=None,
            safe_error_message=None,
            updated_at=datetime.now(UTC),
        )
        self.runs[run_id] = run
        return run

    async def mark_failed(
        self,
        run_id: UUID,
        error_code: SafeErrorCode,
        error_message: str,
        raw_provider_output: str | None,
    ) -> DecodeRun:
        run = replace(
            self.runs[run_id],
            status="failed",
            structured_result=None,
            raw_provider_output=raw_provider_output,
            safe_error_code=error_code,
            safe_error_message=error_message,
            updated_at=datetime.now(UTC),
        )
        self.runs[run_id] = run
        return run

    async def get_by_id(self, run_id: UUID) -> DecodeRun | None:
        return self.runs.get(run_id)
