import logging

from application.dto.responses.form_response import FormResponse
from application.mappers.form_mapper import FormMapper
from domain.exceptions import FormNotFoundException
from domain.repositories.form_repository import FormRepository
from domain.value_objects.form_id import FormId

logger = logging.getLogger(__name__)


class GetFormUseCase:
    def __init__(self, form_repository: FormRepository) -> None:
        self._form_repository = form_repository

    async def execute(self, form_id: str) -> FormResponse:
        logger.info("Getting form", extra={"form_id": form_id})
        form = await self._form_repository.get_by_id(FormId(form_id))
        if not form:
            logger.warning("Form not found", extra={"form_id": form_id})
            msg = f"Form with id {form_id} not found"
            raise FormNotFoundException(msg)
        return FormMapper.to_response(form)
