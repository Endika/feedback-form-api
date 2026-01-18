from datetime import UTC, datetime

from application.dto.requests.create_form_request import CreateFormRequest
from application.dto.requests.create_question_request import CreateQuestionRequest
from application.dto.requests.update_form_request import UpdateFormRequest
from application.mappers.form_mapper import FormMapper
from domain.entities.form import Form
from domain.value_objects.form_id import FormId
from domain.value_objects.form_type import FormType
from domain.value_objects.multilingual_text import MultilingualText


def test_given_create_form_request_when_to_domain_then_creates_form():
    request = CreateFormRequest(
        type="product_feedback",
        name={"en": "Product Feedback", "es": "Feedback del Producto"},
        description={"en": "Description"},
        questions=[
            CreateQuestionRequest(
                type="text",
                text={"en": "Question 1"},
                required=True,
            )
        ],
    )
    form = FormMapper.to_domain(request)
    assert isinstance(form, Form)
    assert form.type == FormType.PRODUCT_FEEDBACK
    assert form.name.translations == {"en": "Product Feedback", "es": "Feedback del Producto"}
    assert len(form.questions) == 1


def test_given_form_when_to_response_then_creates_response_dto():
    form = Form(
        id=FormId("form-1"),
        type=FormType.PRODUCT_FEEDBACK,
        name=MultilingualText({"en": "Product Feedback"}),
        created_at=datetime(2024, 1, 1, tzinfo=UTC),
        updated_at=datetime(2024, 1, 1, tzinfo=UTC),
    )
    response = FormMapper.to_response(form)
    assert response.id == "form-1"
    assert response.type == "product_feedback"
    assert response.name == {"en": "Product Feedback"}
    assert response.created_at == "2024-01-01T00:00:00+00:00"


def test_given_update_form_request_when_update_domain_then_updates_form():
    form = Form(
        id=FormId("form-1"),
        type=FormType.PRODUCT_FEEDBACK,
        name=MultilingualText({"en": "Old Name"}),
        created_at=datetime(2024, 1, 1, tzinfo=UTC),
        updated_at=datetime(2024, 1, 1, tzinfo=UTC),
    )
    request = UpdateFormRequest(
        name={"en": "New Name"},
        type="survey",
    )
    updated_form = FormMapper.update_domain(form, request)
    assert updated_form.name.translations == {"en": "New Name"}
    assert updated_form.type == FormType.SURVEY
    assert updated_form.updated_at is not None
