import uuid
from datetime import UTC, datetime

from application.dto.requests.create_form_request import CreateFormRequest
from application.dto.requests.update_form_request import UpdateFormRequest
from application.dto.responses.form_response import FormResponse
from application.mappers.question_mapper import QuestionMapper
from domain.entities.form import Form
from domain.value_objects.form_id import FormId
from domain.value_objects.form_type import FormType
from domain.value_objects.multilingual_text import MultilingualText


class FormMapper:
    @staticmethod
    def to_domain(request: CreateFormRequest, form_id: str | None = None) -> Form:
        questions = [QuestionMapper.to_domain(q) for q in request.questions]
        return Form(
            id=FormId(form_id or str(uuid.uuid4())),
            type=FormType(request.type),
            name=MultilingualText(request.name),
            description=MultilingualText(request.description) if request.description else None,
            questions=questions,
            created_at=datetime.now(tz=UTC),
            updated_at=datetime.now(tz=UTC),
        )

    @staticmethod
    def update_domain(form: Form, request: UpdateFormRequest) -> Form:
        if request.type is not None:
            form.type = FormType(request.type)
        if request.name is not None:
            form.name = MultilingualText(request.name)
        if request.description is not None:
            form.description = MultilingualText(request.description)
        if request.questions is not None:
            form.questions = [QuestionMapper.to_domain(q) for q in request.questions]
        form.updated_at = datetime.now(tz=UTC)
        return form

    @staticmethod
    def to_response(form: Form) -> FormResponse:
        return FormResponse(
            id=str(form.id),
            type=form.type.value,
            name=form.name.translations,
            description=form.description.translations if form.description else None,
            questions=[QuestionMapper.to_response(q) for q in form.questions],
            created_at=form.created_at.isoformat() if form.created_at else None,
            updated_at=form.updated_at.isoformat() if form.updated_at else None,
        )
