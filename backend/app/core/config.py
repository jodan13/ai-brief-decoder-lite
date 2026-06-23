from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


@dataclass(frozen=True)
class Settings:
    database_url: str
    provider_mode: str
    cors_origins: tuple[str, ...]
    cors_origin_regex: str | None


@lru_cache
def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://postgres:postgres@localhost:5432/brief_decoder",
        ),
        provider_mode=os.getenv("BRIEF_PROVIDER_MODE", "fake_success"),
        cors_origins=_split_csv(
            os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")
        ),
        cors_origin_regex=os.getenv("CORS_ORIGIN_REGEX", r"^chrome-extension://[a-z]{32}$"),
    )
