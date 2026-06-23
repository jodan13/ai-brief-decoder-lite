from __future__ import annotations

from typing import cast
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.deps import get_service
from app.main import create_app
from app.providers.brief_decode import FakeBriefDecodeProvider
from app.services.brief_decoder import BriefDecodeService
from tests.fakes import InMemoryDecodeRunRepository


@pytest.mark.asyncio
async def test_decode_brief_happy_path_with_fake_provider() -> None:
    app = create_app()
    repository = InMemoryDecodeRunRepository()
    service = BriefDecodeService(repository, FakeBriefDecodeProvider())
    app.dependency_overrides[get_service] = lambda: service

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/v1/briefs/decode", json={"text": "Launch a landing page"})

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "succeeded"
        assert body["structured_result"]["recommended_next_action"]
        run_id = UUID(cast(str, body["run_id"]))

        get_response = await client.get(f"/v1/briefs/runs/{run_id}")
        assert get_response.status_code == 200
        assert get_response.json()["run_id"] == str(run_id)


@pytest.mark.asyncio
async def test_decode_brief_returns_safe_failure_for_invalid_provider_output() -> None:
    app = create_app()
    repository = InMemoryDecodeRunRepository()
    service = BriefDecodeService(repository, FakeBriefDecodeProvider("fake_invalid_severity"))
    app.dependency_overrides[get_service] = lambda: service

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/v1/briefs/decode", json={"text": "Create a risky plan"})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "failed"
    assert body["safe_error_code"] == "invalid_provider_output"
    assert body["safe_error_message"] == (
        "Provider returned output that does not match the expected brief schema."
    )
    assert body["structured_result"] is None
    assert "critical" in body["raw_provider_output"]
