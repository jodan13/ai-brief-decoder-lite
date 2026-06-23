from __future__ import annotations

import json
from json import JSONDecodeError
from uuid import UUID

from pydantic import ValidationError

from app.domain.entities import DecodeRun
from app.providers.brief_decode import BriefDecodeProvider, ProviderError
from app.repositories.decode_runs import DecodeRunRepository
from app.schemas import StructuredBriefResult, result_to_json

INVALID_PROVIDER_MESSAGE = "Provider returned output that does not match the expected brief schema."
PROVIDER_ERROR_MESSAGE = "Brief decode provider failed."


class BriefDecodeService:
    def __init__(self, repository: DecodeRunRepository, provider: BriefDecodeProvider) -> None:
        self._repository = repository
        self._provider = provider

    async def decode(self, text: str) -> DecodeRun:
        run = await self._repository.create_running(text)
        raw_output: str | None = None

        try:
            raw_output = await self._provider.decode(text)
            structured = parse_provider_output(raw_output)
        except ProviderError:
            return await self._repository.mark_failed(
                run.id,
                "provider_error",
                PROVIDER_ERROR_MESSAGE,
                raw_output,
            )
        except (JSONDecodeError, ValidationError):
            return await self._repository.mark_failed(
                run.id,
                "invalid_provider_output",
                INVALID_PROVIDER_MESSAGE,
                raw_output,
            )

        return await self._repository.mark_succeeded(run.id, result_to_json(structured), raw_output)

    async def get_run(self, run_id: UUID) -> DecodeRun | None:
        return await self._repository.get_by_id(run_id)


def parse_provider_output(raw_output: str) -> StructuredBriefResult:
    decoded = json.loads(raw_output)
    return StructuredBriefResult.model_validate(decoded)
