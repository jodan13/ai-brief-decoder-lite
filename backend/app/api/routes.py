from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_service
from app.domain.entities import DecodeRun
from app.schemas import BriefDecodeRequest, DecodeRunResponse, ErrorResponse, result_from_json
from app.services.brief_decoder import BriefDecodeService

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/v1/briefs/decode", response_model=DecodeRunResponse)
async def decode_brief(
    request: BriefDecodeRequest,
    service: Annotated[BriefDecodeService, Depends(get_service)],
) -> DecodeRunResponse:
    run = await service.decode(request.text)
    return _to_response(run)


@router.get(
    "/v1/briefs/runs/{run_id}",
    response_model=DecodeRunResponse,
    responses={404: {"model": ErrorResponse}},
)
async def get_run(
    run_id: UUID,
    service: Annotated[BriefDecodeService, Depends(get_service)],
) -> DecodeRunResponse:
    run = await service.get_run(run_id)
    if run is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error_code="run_not_found",
                message="Decode run was not found.",
            ).model_dump(mode="json"),
        )
    return _to_response(run)


def _to_response(typed_run: DecodeRun) -> DecodeRunResponse:
    return DecodeRunResponse(
        run_id=typed_run.id,
        status=typed_run.status,
        input_text=typed_run.input_text,
        structured_result=result_from_json(typed_run.structured_result),
        raw_provider_output=typed_run.raw_provider_output,
        safe_error_code=typed_run.safe_error_code,
        safe_error_message=typed_run.safe_error_message,
        created_at=typed_run.created_at,
        updated_at=typed_run.updated_at,
    )
