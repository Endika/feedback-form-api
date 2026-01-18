from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from presentation.api.main import app


@pytest.mark.integration()
def test_given_valid_request_when_create_form_then_returns_form():
    # Given: Valid form request
    client = TestClient(app)

    # When: Create form
    response = client.post(
        "/api/v1/backoffice/forms",
        auth=("admin", "admin"),
        json={
            "type": "product_feedback",
            "name": {"en": "Product Feedback", "es": "Feedback del Producto"},
            "description": {"en": "Help us improve", "es": "Ayúdanos a mejorar"},
            "questions": [
                {
                    "type": "rating",
                    "text": {"en": "How satisfied?", "es": "¿Qué tan satisfecho?"},
                    "required": True,
                    "min_rating": 1,
                    "max_rating": 5,
                },
            ],
        },
    )

    # Then: Form is created successfully
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["type"] == "product_feedback"
    assert "id" in data
    assert len(data["questions"]) == 1


@pytest.mark.integration()
def test_given_existing_forms_when_list_forms_then_returns_forms():
    # Given: At least one form exists
    client = TestClient(app)
    client.post(
        "/api/v1/backoffice/forms",
        auth=("admin", "admin"),
        json={
            "type": "product_feedback",
            "name": {"en": "Form 1", "es": "Formulario 1"},
            "description": {"en": "Description", "es": "Descripción"},
            "questions": [],
        },
    )

    # When: List forms
    response = client.get("/api/v1/backoffice/forms", auth=("admin", "admin"))

    # Then: Forms are returned
    assert response.status_code == HTTPStatus.OK
    forms = response.json()
    assert isinstance(forms, list)
    assert len(forms) >= 1


@pytest.mark.integration()
def test_given_existing_form_when_get_form_then_returns_form():
    # Given: A form exists
    client = TestClient(app)
    create_response = client.post(
        "/api/v1/backoffice/forms",
        auth=("admin", "admin"),
        json={
            "type": "product_feedback",
            "name": {"en": "Test Form", "es": "Formulario de Prueba"},
            "description": {"en": "Test", "es": "Prueba"},
            "questions": [],
        },
    )
    form_id = create_response.json()["id"]

    # When: Get form
    response = client.get(f"/api/v1/backoffice/forms/{form_id}", auth=("admin", "admin"))

    # Then: Form is returned
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == form_id
    assert data["type"] == "product_feedback"


@pytest.mark.integration()
def test_given_existing_form_when_update_form_then_returns_updated_form():
    # Given: A form exists
    client = TestClient(app)
    create_response = client.post(
        "/api/v1/backoffice/forms",
        auth=("admin", "admin"),
        json={
            "type": "product_feedback",
            "name": {"en": "Original", "es": "Original"},
            "description": {"en": "Original", "es": "Original"},
            "questions": [],
        },
    )
    form_id = create_response.json()["id"]

    # When: Update form
    response = client.put(
        f"/api/v1/backoffice/forms/{form_id}",
        auth=("admin", "admin"),
        json={
            "name": {"en": "Updated", "es": "Actualizado"},
            "description": {"en": "Updated", "es": "Actualizado"},
        },
    )

    # Then: Form is updated
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == form_id
    assert data["name"]["en"] == "Updated"


@pytest.mark.integration()
def test_given_existing_form_when_delete_form_then_form_is_deleted():
    # Given: A form exists
    client = TestClient(app)
    create_response = client.post(
        "/api/v1/backoffice/forms",
        auth=("admin", "admin"),
        json={
            "type": "product_feedback",
            "name": {"en": "To Delete", "es": "A Eliminar"},
            "description": {"en": "Test", "es": "Prueba"},
            "questions": [],
        },
    )
    form_id = create_response.json()["id"]

    # When: Delete form
    response = client.delete(f"/api/v1/backoffice/forms/{form_id}", auth=("admin", "admin"))

    # Then: Form is deleted
    assert response.status_code == HTTPStatus.NO_CONTENT

    # And: Form cannot be retrieved
    get_response = client.get(f"/api/v1/backoffice/forms/{form_id}", auth=("admin", "admin"))
    assert get_response.status_code == HTTPStatus.NOT_FOUND
