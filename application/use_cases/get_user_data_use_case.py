import logging

from application.dto.responses.response_response import ResponseResponse
from application.mappers.response_mapper import ResponseMapper
from domain.repositories.response_repository import ResponseRepository

logger = logging.getLogger(__name__)


class GetUserDataUseCase:
    def __init__(self, response_repository: ResponseRepository) -> None:
        self._response_repository = response_repository

    async def execute(self, user_id: str) -> list[ResponseResponse]:
        logger.info("Getting user data", extra={"user_id": user_id})
        responses = await self._response_repository.get_by_user_id(user_id)
        logger.info(
            "User data retrieved successfully",
            extra={"user_id": user_id, "response_count": len(responses)},
        )
        return [ResponseMapper.to_response(response) for response in responses]
