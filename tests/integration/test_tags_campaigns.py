from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from presentation.api.main import app


@pytest.mark.integration()
def test_given_form_when_submit_response_with_tags_then_tags_are_stored():
    # Given: A form exists in the system
    client = TestClient(app)

    create_form_response = client.post(
        "/api/v1/backoffice/forms",
        auth=("admin", "admin"),
        json={
            "type": "product_feedback",
            "name": {"en": "Test Form", "es": "Formulario de Prueba"},
            "description": {"en": "Test description", "es": "Descripción de prueba"},
            "questions": [
                {
                    "type": "rating",
                    "text": {"en": "How satisfied are you?", "es": "¿Qué tan satisfecho estás?"},
                    "required": True,
                    "min_rating": 1,
                    "max_rating": 5,
                },
                {
                    "type": "text",
                    "text": {"en": "Comments", "es": "Comentarios"},
                    "required": False,
                },
            ],
        },
    )
    assert create_form_response.status_code == HTTPStatus.CREATED
    form_data = create_form_response.json()
    form_id = form_data["id"]

    # When: Submit a response with tags from query parameters
    submit_response = client.post(
        "/api/v1/mobile/responses?campaign=summer2024&source=email&group=premium_users",
        json={
            "form_id": form_id,
            "answers": [
                {"question_id": form_data["questions"][0]["id"], "value": 5},
                {"question_id": form_data["questions"][1]["id"], "value": "Great!"},
            ],
            "tags": {
                "utm_source": "newsletter",
                "utm_medium": "email",
            },
        },
    )

    # Then: Response is created with all tags (query params + body tags)
    assert submit_response.status_code == HTTPStatus.CREATED
    response_data = submit_response.json()
    assert response_data["form_id"] == form_id
    expected_answer_count = 2
    assert len(response_data["answers"]) == expected_answer_count
    assert "tags" in response_data
    assert response_data["tags"]["campaign"] == "summer2024"
    assert response_data["tags"]["source"] == "email"
    assert response_data["tags"]["group"] == "premium_users"
    assert response_data["tags"]["utm_source"] == "newsletter"
    assert response_data["tags"]["utm_medium"] == "email"

    # And: Response can be retrieved with tags from backoffice
    get_responses = client.get(
        "/api/v1/backoffice/responses",
        auth=("admin", "admin"),
        params={"form_id": form_id},
    )
    assert get_responses.status_code == HTTPStatus.OK
    responses = get_responses.json()
    assert len(responses) == 1
    assert responses[0]["tags"]["campaign"] == "summer2024"
    assert responses[0]["tags"]["source"] == "email"
    assert responses[0]["tags"]["group"] == "premium_users"
