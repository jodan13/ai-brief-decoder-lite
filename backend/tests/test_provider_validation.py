from __future__ import annotations

import json
from json import JSONDecodeError

import pytest
from pydantic import ValidationError

from app.providers.brief_decode import FakeBriefDecodeProvider
from app.services.brief_decoder import parse_provider_output


@pytest.mark.asyncio
async def test_structured_output_validation_success() -> None:
    provider = FakeBriefDecodeProvider()

    result = parse_provider_output(await provider.decode("Build a concise project brief"))

    assert result.summary.startswith("Decoded brief for:")
    assert result.risks[0].severity == "medium"


def test_invalid_severity_validation_failure() -> None:
    raw_output = json.dumps(
        {
            "summary": "Summary",
            "goals": [],
            "deliverables": [],
            "constraints": [],
            "risks": [{"risk": "Scope", "severity": "critical", "reason": "Invalid enum"}],
            "clarifying_questions": [],
            "recommended_next_action": "Ask a question",
        }
    )

    with pytest.raises(ValidationError):
        parse_provider_output(raw_output)


def test_malformed_json_validation_failure() -> None:
    with pytest.raises(JSONDecodeError):
        parse_provider_output('{"summary": "broken",')
