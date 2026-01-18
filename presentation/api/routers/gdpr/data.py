import logging

from fastapi import APIRouter, HTTPException, Response, status

from application.dto.responses.response_response import ResponseResponse
from infrastructure.config import (
    get_delete_user_data_use_case,
    get_export_user_data_use_case,
    get_get_user_data_use_case,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{user_id}", response_model=list[ResponseResponse])
async def get_user_data(user_id: str) -> list[ResponseResponse]:
    try:
        use_case = get_get_user_data_use_case()
        return await use_case.execute(user_id)
    except Exception as e:
        logger.exception(
            "Unexpected error getting user data", extra={"user_id": user_id, "error": str(e)}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e


@router.get("/{user_id}/export")
async def export_user_data(user_id: str) -> Response:
    try:
        use_case = get_export_user_data_use_case()
        export_json = await use_case.execute(user_id)
    except Exception as e:
        logger.exception(
            "Unexpected error exporting user data", extra={"user_id": user_id, "error": str(e)}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e
    else:
        return Response(
            content=export_json,
            media_type="application/json",
            headers={"Content-Disposition": f'attachment; filename="user_data_{user_id}.json"'},
        )


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_data(user_id: str) -> dict[str, int]:
    try:
        use_case = get_delete_user_data_use_case()
        deleted_count = await use_case.execute(user_id)
    except Exception as e:
        logger.exception(
            "Unexpected error deleting user data", extra={"user_id": user_id, "error": str(e)}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e
    else:
        return {"deleted_responses": deleted_count}
