import pytest

from application.use_cases.get_form_use_case import GetFormUseCase
from domain.entities.form import Form
from domain.exceptions import FormNotFoundException
from domain.value_objects.form_id import FormId
from domain.value_objects.form_type import FormType
from domain.value_objects.multilingual_text import MultilingualText
from infrastructure.persistence.mock_form_repository import MockFormRepository


@pytest.mark.asyncio()
async def test_given_existing_form_id_when_get_form_then_returns_form_response():
    repository = MockFormRepository()
    form = Form(
        id=FormId("form-1"),
        type=FormType.PRODUCT_FEEDBACK,
        name=MultilingualText({"en": "Product Feedback"}),
    )
    await repository.create(form)
    use_case = GetFormUseCase(repository)
    response = await use_case.execute("form-1")
    assert response.id == "form-1"
    assert response.type == "product_feedback"


@pytest.mark.asyncio()
async def test_given_nonexistent_form_id_when_get_form_then_raises_exception():
    repository = MockFormRepository()
    use_case = GetFormUseCase(repository)
    with pytest.raises(FormNotFoundException):
        await use_case.execute("nonexistent")
