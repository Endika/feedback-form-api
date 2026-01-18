import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from application.dto.requests.create_form_request import CreateFormRequest
from application.dto.requests.update_form_request import UpdateFormRequest
from application.dto.responses.form_response import FormResponse
from domain.exceptions import FormNotFoundException
from infrastructure.config import (
    get_create_form_use_case,
    get_delete_form_use_case,
    get_get_form_use_case,
    get_list_forms_use_case,
    get_update_form_use_case,
)
from presentation.api.middleware.auth import get_current_backoffice_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("", response_model=FormResponse, status_code=status.HTTP_201_CREATED)
async def create_form(
    request: CreateFormRequest,
    current_user: Annotated[str, Depends(get_current_backoffice_user)],  # noqa: ARG001
) -> FormResponse:
    try:
        use_case = get_create_form_use_case()
        return await use_case.execute(request)
    except ValueError as e:
        logger.error("Validation error creating form", extra={"error": str(e)})  # noqa: TRY400
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        logger.exception("Unexpected error creating form", extra={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e


@router.get("", response_model=list[FormResponse])
async def list_forms(
    form_type: str | None = None,
    current_user: Annotated[str, Depends(get_current_backoffice_user)] = "",  # noqa: ARG001
) -> list[FormResponse]:
    try:
        use_case = get_list_forms_use_case()
        return await use_case.execute(form_type)
    except ValueError as e:
        logger.error("Invalid form type", extra={"form_type": form_type, "error": str(e)})  # noqa: TRY400
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        logger.exception("Unexpected error listing forms", extra={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e


@router.get("/{form_id}", response_model=FormResponse)
async def get_form(
    form_id: str,
    current_user: Annotated[str, Depends(get_current_backoffice_user)] = "",  # noqa: ARG001
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


@router.put("/{form_id}", response_model=FormResponse)
async def update_form(
    form_id: str,
    request: UpdateFormRequest,
    current_user: Annotated[str, Depends(get_current_backoffice_user)],  # noqa: ARG001
) -> FormResponse:
    try:
        use_case = get_update_form_use_case()
        return await use_case.execute(form_id, request)
    except FormNotFoundException as e:
        logger.warning("Form not found", extra={"form_id": form_id})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ValueError as e:
        logger.error("Validation error updating form", extra={"form_id": form_id, "error": str(e)})  # noqa: TRY400
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        logger.exception(
            "Unexpected error updating form",
            extra={"form_id": form_id, "error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e


@router.delete("/{form_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_form(
    form_id: str,
    current_user: Annotated[str, Depends(get_current_backoffice_user)],  # noqa: ARG001
) -> None:
    try:
        use_case = get_delete_form_use_case()
        await use_case.execute(form_id)
    except FormNotFoundException as e:
        logger.warning("Form not found", extra={"form_id": form_id})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.exception(
            "Unexpected error deleting form",
            extra={"form_id": form_id, "error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e
