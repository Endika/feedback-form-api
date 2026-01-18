import logging

from domain.repositories.response_repository import ResponseRepository

logger = logging.getLogger(__name__)


class DeleteUserDataUseCase:
    def __init__(self, response_repository: ResponseRepository) -> None:
        self._response_repository = response_repository

    async def execute(self, user_id: str) -> int:
        logger.info("Deleting user data", extra={"user_id": user_id})
        deleted_count = await self._response_repository.delete_by_user_id(user_id)
        logger.info(
            "User data deleted successfully",
            extra={"user_id": user_id, "deleted_responses": deleted_count},
        )
        return deleted_count
