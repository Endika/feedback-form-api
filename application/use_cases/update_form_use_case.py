import logging

from application.dto.requests.update_form_request import UpdateFormRequest
from application.dto.responses.form_response import FormResponse
from application.mappers.form_mapper import FormMapper
from domain.exceptions import FormNotFoundException
from domain.repositories.form_repository import FormRepository
from domain.value_objects.form_id import FormId

logger = logging.getLogger(__name__)


class UpdateFormUseCase:
    def __init__(self, form_repository: FormRepository) -> None:
        self._form_repository = form_repository

    async def execute(self, form_id: str, request: UpdateFormRequest) -> FormResponse:
        logger.info("Updating form", extra={"form_id": form_id})
        form = await self._form_repository.get_by_id(FormId(form_id))
        if not form:
            logger.warning("Form not found", extra={"form_id": form_id})
            msg = f"Form with id {form_id} not found"
            raise FormNotFoundException(msg)
        updated_form = FormMapper.update_domain(form, request)
        saved_form = await self._form_repository.update(updated_form)
        logger.info("Form updated successfully", extra={"form_id": str(saved_form.id)})
        return FormMapper.to_response(saved_form)
