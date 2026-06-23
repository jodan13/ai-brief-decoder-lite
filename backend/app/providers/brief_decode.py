from __future__ import annotations

import json
from typing import Protocol

from app.domain.types import ProviderMode


class ProviderError(Exception):
    """Raised when a provider cannot return a usable response."""


class BriefDecodeProvider(Protocol):
    async def decode(self, text: str) -> str:
        """Return the raw provider response as a JSON string."""
        ...


class FakeBriefDecodeProvider:
    def __init__(self, mode: ProviderMode = "fake_success") -> None:
        self._mode = mode

    async def decode(self, text: str) -> str:
        if self._mode == "fake_provider_error":
            raise ProviderError("fake provider failure")
        if self._mode == "fake_malformed_json":
            return '{"summary": "broken",'

        payload: dict[str, object] = {
            "summary": f"Decoded brief for: {text[:80]}",
            "goals": ["Clarify the requested outcome", "Identify deliverables and risks"],
            "deliverables": ["Structured brief summary", "Recommended next action"],
            "constraints": ["Use a deterministic fake provider for local review"],
            "risks": [
                {
                    "risk": "Requirements may be underspecified",
                    "severity": "medium",
                    "reason": "The input can omit scope, timeline, or acceptance criteria.",
                }
            ],
            "clarifying_questions": ["What deadline and success criteria should be used?"],
            "recommended_next_action": (
                "Confirm scope and convert the brief into implementation tasks."
            ),
        }

        if self._mode == "fake_invalid_severity":
            payload["risks"] = [
                {
                    "risk": "Invalid severity from provider",
                    "severity": "critical",
                    "reason": "Used to exercise structured validation.",
                }
            ]
        if self._mode == "fake_missing_fields":
            payload.pop("summary", None)

        return json.dumps(payload, ensure_ascii=False)


class RealLLMProvider:
    async def decode(self, text: str) -> str:
        raise ProviderError("real LLM provider is not configured in stage 1")
