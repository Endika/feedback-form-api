import pytest
from fastapi.testclient import TestClient

import infrastructure.config.dependencies as deps
from infrastructure.persistence import MockFormRepository, MockResponseRepository
from presentation.api.main import app


@pytest.fixture(autouse=True)
def _reset_repositories():
    shared_form_repository = MockFormRepository()
    shared_response_repository = MockResponseRepository()

    deps._form_repository = shared_form_repository
    deps._response_repository = shared_response_repository

    yield

    shared_form_repository._forms.clear()
    shared_response_repository._responses.clear()
    deps.reset_dependencies()


@pytest.fixture()
def client():
    return TestClient(app)
