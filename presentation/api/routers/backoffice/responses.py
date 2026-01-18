import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from application.dto.responses.response_response import ResponseResponse
from infrastructure.config import get_get_responses_use_case
from presentation.api.middleware.auth import get_current_backoffice_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("", response_model=list[ResponseResponse])
async def get_responses(
    form_id: str | None = None,
    current_user: Annotated[str, Depends(get_current_backoffice_user)] = "",  # noqa: ARG001
) -> list[ResponseResponse]:
    try:
        use_case = get_get_responses_use_case()
        return await use_case.execute(form_id)
    except Exception as e:
        logger.exception(
            "Unexpected error getting responses",
            extra={"form_id": form_id, "error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from None
