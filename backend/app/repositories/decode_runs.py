from __future__ import annotations

from datetime import UTC, datetime
from typing import Protocol, cast
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DecodeRunModel
from app.domain.entities import DecodeRun, JsonObject
from app.domain.types import RunStatus, SafeErrorCode


class DecodeRunRepository(Protocol):
    async def create_running(self, input_text: str) -> DecodeRun:
        """Create a running decode run."""
        ...

    async def mark_succeeded(
        self,
        run_id: UUID,
        structured_result: JsonObject,
        raw_provider_output: str,
    ) -> DecodeRun:
        """Persist a successful provider result."""
        ...

    async def mark_failed(
        self,
        run_id: UUID,
        error_code: SafeErrorCode,
        error_message: str,
        raw_provider_output: str | None,
    ) -> DecodeRun:
        """Persist a safe failure state."""
        ...

    async def get_by_id(self, run_id: UUID) -> DecodeRun | None:
        """Fetch a saved run."""
        ...


class SqlAlchemyDecodeRunRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_running(self, input_text: str) -> DecodeRun:
        model = DecodeRunModel(id=uuid4(), status="running", input_text=input_text)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return _model_to_entity(model)

    async def mark_succeeded(
        self,
        run_id: UUID,
        structured_result: JsonObject,
        raw_provider_output: str,
    ) -> DecodeRun:
        model = await self._get_model(run_id)
        model.status = "succeeded"
        model.structured_result = structured_result
        model.raw_provider_output = raw_provider_output
        model.safe_error_code = None
        model.safe_error_message = None
        model.updated_at = datetime.now(UTC)
        await self._session.commit()
        await self._session.refresh(model)
        return _model_to_entity(model)

    async def mark_failed(
        self,
        run_id: UUID,
        error_code: SafeErrorCode,
        error_message: str,
        raw_provider_output: str | None,
    ) -> DecodeRun:
        model = await self._get_model(run_id)
        model.status = "failed"
        model.safe_error_code = error_code
        model.safe_error_message = error_message
        model.raw_provider_output = raw_provider_output
        model.updated_at = datetime.now(UTC)
        await self._session.commit()
        await self._session.refresh(model)
        return _model_to_entity(model)

    async def get_by_id(self, run_id: UUID) -> DecodeRun | None:
        model = await self._session.get(DecodeRunModel, run_id)
        if model is None:
            return None
        return _model_to_entity(model)

    async def _get_model(self, run_id: UUID) -> DecodeRunModel:
        result = await self._session.execute(
            select(DecodeRunModel).where(DecodeRunModel.id == run_id)
        )
        model = result.scalar_one()
        return model


def _model_to_entity(model: DecodeRunModel) -> DecodeRun:
    return DecodeRun(
        id=model.id,
        status=cast(RunStatus, model.status),
        input_text=model.input_text,
        structured_result=model.structured_result,
        raw_provider_output=model.raw_provider_output,
        safe_error_code=cast(SafeErrorCode | None, model.safe_error_code),
        safe_error_message=model.safe_error_message,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
