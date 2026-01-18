from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from presentation.api.main import app


@pytest.mark.integration()
def test_given_existing_form_when_submit_response_then_returns_response():
    # Given: A form exists
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
                {
                    "type": "text",
                    "text": {"en": "Comment", "es": "Comentario"},
                    "required": False,
                },
            ],
        },
    )
    form_id = create_form_response.json()["id"]
    question_ids = [q["id"] for q in create_form_response.json()["questions"]]

    # When: Submit response
    response = client.post(
        "/api/v1/mobile/responses",
        json={
            "form_id": form_id,
            "answers": [
                {"question_id": question_ids[0], "value": 5},
                {"question_id": question_ids[1], "value": "Great product!"},
            ],
        },
    )

    # Then: Response is created
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["form_id"] == form_id
    expected_answer_count = 2
    assert len(data["answers"]) == expected_answer_count
    assert "id" in data
    assert "submitted_at" in data
