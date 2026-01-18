import pytest

from application.dto.requests.create_form_request import CreateFormRequest
from application.use_cases.create_form_use_case import CreateFormUseCase
from domain.value_objects.form_id import FormId
from infrastructure.persistence.mock_form_repository import MockFormRepository


@pytest.mark.asyncio()
async def test_given_valid_request_when_create_form_then_returns_form_response():
    repository = MockFormRepository()
    use_case = CreateFormUseCase(repository)
    request = CreateFormRequest(
        type="product_feedback",
        name={"en": "Product Feedback"},
    )
    response = await use_case.execute(request)
    assert response.id is not None
    assert response.type == "product_feedback"
    assert response.name == {"en": "Product Feedback"}


@pytest.mark.asyncio()
async def test_given_valid_request_when_create_form_then_persists_to_repository():
    repository = MockFormRepository()
    use_case = CreateFormUseCase(repository)
    request = CreateFormRequest(
        type="product_feedback",
        name={"en": "Product Feedback"},
    )
    response = await use_case.execute(request)
    retrieved_form = await repository.get_by_id(FormId(response.id))
    assert retrieved_form is not None
    assert str(retrieved_form.id) == response.id
