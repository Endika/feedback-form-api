from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from presentation.api.main import app


@pytest.mark.integration()
def test_given_existing_form_when_get_form_then_returns_form():
    # Given: A form exists
    client = TestClient(app)
    create_response = client.post(
        "/api/v1/backoffice/forms",
        auth=("admin", "admin"),
        json={
            "type": "product_feedback",
            "name": {"en": "Mobile Form", "es": "Formulario Móvil"},
            "description": {"en": "Description", "es": "Descripción"},
            "questions": [
                {
                    "type": "text",
                    "text": {"en": "Comment", "es": "Comentario"},
                    "required": False,
                },
            ],
        },
    )
    form_id = create_response.json()["id"]

    # When: Get form (mobile endpoint)
    response = client.get(f"/api/v1/mobile/forms/{form_id}")

    # Then: Form is returned
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == form_id
    assert data["type"] == "product_feedback"
    assert len(data["questions"]) == 1
