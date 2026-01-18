import logging

from domain.exceptions import FormNotFoundException
from domain.repositories.form_repository import FormRepository
from domain.value_objects.form_id import FormId

logger = logging.getLogger(__name__)


class DeleteFormUseCase:
    def __init__(self, form_repository: FormRepository) -> None:
        self._form_repository = form_repository

    async def execute(self, form_id: str) -> None:
        logger.info("Deleting form", extra={"form_id": form_id})
        form = await self._form_repository.get_by_id(FormId(form_id))
        if not form:
            logger.warning("Form not found", extra={"form_id": form_id})
            msg = f"Form with id {form_id} not found"
            raise FormNotFoundException(msg)
        await self._form_repository.delete(FormId(form_id))
        logger.info("Form deleted successfully", extra={"form_id": form_id})
