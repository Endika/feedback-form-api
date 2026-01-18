import logging

from fastapi import APIRouter, HTTPException, Query, status

from application.dto.requests.submit_response_request import SubmitResponseRequest
from application.dto.responses.response_response import ResponseResponse
from domain.exceptions import FormNotFoundException, InvalidAnswerException
from infrastructure.config import get_submit_response_use_case

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("", response_model=ResponseResponse, status_code=status.HTTP_201_CREATED)
async def submit_response(
    request: SubmitResponseRequest,
    campaign: str | None = Query(None, description="Campaign identifier"),
    source: str | None = Query(None, description="Response source (email, sms, etc.)"),
    group: str | None = Query(None, description="User group identifier"),
) -> ResponseResponse:
    try:
        tags = request.tags.copy() if request.tags else {}
        if campaign:
            tags["campaign"] = campaign
        if source:
            tags["source"] = source
        if group:
            tags["group"] = group

        request_with_tags = SubmitResponseRequest(
            form_id=request.form_id,
            answers=request.answers,
            tags=tags,
            user_id=request.user_id,
        )
        use_case = get_submit_response_use_case()
        return await use_case.execute(request_with_tags)
    except FormNotFoundException as e:
        logger.warning("Form not found for response submission", extra={"form_id": request.form_id})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except InvalidAnswerException as e:
        logger.warning(
            "Invalid answer in response", extra={"form_id": request.form_id, "error": str(e)}
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        logger.exception("Unexpected error submitting response", extra={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e
