import logging

from application.dto.responses.form_response import FormResponse
from application.mappers.form_mapper import FormMapper
from domain.repositories.form_repository import FormRepository
from domain.value_objects.form_type import FormType

logger = logging.getLogger(__name__)


class ListFormsUseCase:
    def __init__(self, form_repository: FormRepository) -> None:
        self._form_repository = form_repository

    async def execute(self, form_type: str | None = None) -> list[FormResponse]:
        logger.info("Listing forms", extra={"form_type": form_type})
        form_type_enum = FormType(form_type) if form_type else None
        forms = await self._form_repository.get_all(form_type_enum)
        logger.info("Forms retrieved", extra={"count": len(forms)})
        return [FormMapper.to_response(form) for form in forms]
