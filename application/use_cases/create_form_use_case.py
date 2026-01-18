import logging

from application.dto.requests.create_form_request import CreateFormRequest
from application.dto.responses.form_response import FormResponse
from application.mappers.form_mapper import FormMapper
from domain.repositories.form_repository import FormRepository

logger = logging.getLogger(__name__)


class CreateFormUseCase:
    def __init__(self, form_repository: FormRepository) -> None:
        self._form_repository = form_repository

    async def execute(self, request: CreateFormRequest) -> FormResponse:
        logger.info("Creating new form", extra={"form_type": request.type})
        form = FormMapper.to_domain(request)
        created_form = await self._form_repository.create(form)
        logger.info("Form created successfully", extra={"form_id": str(created_form.id)})
        return FormMapper.to_response(created_form)
