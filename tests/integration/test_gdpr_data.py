from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from presentation.api.main import app


@pytest.mark.integration()
def test_given_user_with_responses_when_get_user_data_then_returns_responses():
    # Given: A user with responses exists
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
    user_id = "user123"

    client.post(
        "/api/v1/mobile/responses",
        json={
            "form_id": form_id,
            "answers": [{"question_id": question_id, "value": 5}],
            "user_id": user_id,
        },
    )

    # When: Get user data
    response = client.get(f"/api/v1/gdpr/data/{user_id}")

    # Then: User data is returned
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["user_id"] == user_id
    assert data[0]["form_id"] == form_id


@pytest.mark.integration()
def test_given_user_with_responses_when_export_user_data_then_returns_json_file():
    # Given: A user with responses exists
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
                    "type": "text",
                    "text": {"en": "Comment", "es": "Comentario"},
                    "required": False,
                },
            ],
        },
    )
    form_id = create_form_response.json()["id"]
    question_id = create_form_response.json()["questions"][0]["id"]
    user_id = "user456"

    client.post(
        "/api/v1/mobile/responses",
        json={
            "form_id": form_id,
            "answers": [{"question_id": question_id, "value": "Great product!"}],
            "user_id": user_id,
        },
    )

    # When: Export user data
    response = client.get(f"/api/v1/gdpr/data/{user_id}/export")

    # Then: JSON file is returned
    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"] == "application/json"
    assert f'filename="user_data_{user_id}.json"' in response.headers["content-disposition"]
    import json

    export_data = json.loads(response.text)
    assert export_data["user_id"] == user_id
    assert export_data["total_responses"] == 1
    assert len(export_data["responses"]) == 1


@pytest.mark.integration()
def test_given_user_with_responses_when_delete_user_data_then_responses_are_deleted():
    # Given: A user with responses exists
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
    user_id = "user789"

    client.post(
        "/api/v1/mobile/responses",
        json={
            "form_id": form_id,
            "answers": [{"question_id": question_id, "value": 4}],
            "user_id": user_id,
        },
    )

    # When: Delete user data
    response = client.delete(f"/api/v1/gdpr/data/{user_id}")

    # Then: Responses are deleted
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["deleted_responses"] == 1

    # And: User data is no longer available
    get_response = client.get(f"/api/v1/gdpr/data/{user_id}")
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json() == []
