from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated, cast

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.db.session import get_session
from app.domain.types import ProviderMode
from app.providers.brief_decode import FakeBriefDecodeProvider
from app.repositories.decode_runs import DecodeRunRepository, SqlAlchemyDecodeRunRepository
from app.services.brief_decoder import BriefDecodeService


def get_provider(settings: Annotated[Settings, Depends(get_settings)]) -> FakeBriefDecodeProvider:
    return FakeBriefDecodeProvider(cast(ProviderMode, settings.provider_mode))


async def get_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AsyncIterator[DecodeRunRepository]:
    yield SqlAlchemyDecodeRunRepository(session)


def get_service(
    repository: Annotated[DecodeRunRepository, Depends(get_repository)],
    provider: Annotated[FakeBriefDecodeProvider, Depends(get_provider)],
) -> BriefDecodeService:
    return BriefDecodeService(repository=repository, provider=provider)
