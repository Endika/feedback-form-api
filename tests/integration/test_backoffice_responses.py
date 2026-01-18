from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from presentation.api.main import app


@pytest.mark.integration()
def test_given_existing_responses_when_get_responses_then_returns_responses():
    # Given: A form with a response exists
    client = TestClient(app)
    create_form_response = client.post(
        "/api/v1/backoffice/forms",
        auth=("admin", "admin"),
        json={
            "type": "product_feedback",
            "name": {"en": "Test Form", "es": "Formulario de Prueba"},
            "description": {"en": "Test", "es": "Prueba"},
            "questions": [
                {
                    "type": "rating",
                    "text": {"en": "Rating", "es": "Calificación"},
                    "required": True,
                    "min_rating": 1,
                    "max_rating": 5,
                },
            ],
        },
    )
    form_id = create_form_response.json()["id"]
    question_id = create_form_response.json()["questions"][0]["id"]

    client.post(
        "/api/v1/mobile/responses",
        json={
            "form_id": form_id,
            "answers": [{"question_id": question_id, "value": 5}],
        },
    )

    # When: Get responses
    response = client.get(
        "/api/v1/backoffice/responses",
        auth=("admin", "admin"),
        params={"form_id": form_id},
    )

    # Then: Responses are returned
    assert response.status_code == HTTPStatus.OK
    responses = response.json()
    assert isinstance(responses, list)
    assert len(responses) >= 1
    assert responses[0]["form_id"] == form_id
