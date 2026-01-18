import logging

from fastapi import APIRouter, HTTPException, Query, status

from application.dto.responses.form_response import FormResponse
from domain.exceptions import FormNotFoundException
from infrastructure.config import get_get_form_use_case

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{form_id}", response_model=FormResponse)
async def get_form(
    form_id: str,
    campaign: str | None = Query(None, description="Campaign identifier (for reference)"),  # noqa: ARG001
    source: str | None = Query(None, description="Response source (for reference)"),  # noqa: ARG001
    group: str | None = Query(None, description="User group identifier (for reference)"),  # noqa: ARG001
) -> FormResponse:
    try:
        use_case = get_get_form_use_case()
        return await use_case.execute(form_id)
    except FormNotFoundException as e:
        logger.warning("Form not found", extra={"form_id": form_id})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.exception(
            "Unexpected error getting form",
            extra={"form_id": form_id, "error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e
