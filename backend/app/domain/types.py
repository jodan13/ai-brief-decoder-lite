from __future__ import annotations

from typing import Literal

type Severity = Literal["low", "medium", "high"]
type RunStatus = Literal["running", "succeeded", "failed"]
type SafeErrorCode = Literal["invalid_provider_output", "provider_error", "run_not_found"]
type ProviderMode = Literal[
    "fake_success",
    "fake_invalid_severity",
    "fake_malformed_json",
    "fake_missing_fields",
    "fake_provider_error",
]
