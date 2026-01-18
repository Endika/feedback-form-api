import logging

from application.dto.responses.response_response import ResponseResponse
from application.mappers.response_mapper import ResponseMapper
from domain.repositories.response_repository import ResponseRepository
from domain.value_objects.form_id import FormId

logger = logging.getLogger(__name__)


class GetResponsesUseCase:
    def __init__(self, response_repository: ResponseRepository) -> None:
        self._response_repository = response_repository

    async def execute(self, form_id: str | None = None) -> list[ResponseResponse]:
        logger.info("Getting responses", extra={"form_id": form_id})
        if form_id:
            responses = await self._response_repository.get_by_form_id(FormId(form_id))
        else:
            responses = await self._response_repository.get_all()
        logger.info("Responses retrieved", extra={"count": len(responses)})
        return [ResponseMapper.to_response(response) for response in responses]
