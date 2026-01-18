import pytest

from domain.value_objects.response_id import ResponseId


def test_given_valid_string_when_create_response_id_then_succeeds():
    # Given: A valid string
    response_id_value = "response-123"

    # When: Create ResponseId
    response_id = ResponseId(response_id_value)

    # Then: ResponseId is created successfully
    assert response_id.value == response_id_value
    assert str(response_id) == response_id_value


def test_given_empty_string_when_create_response_id_then_raises_error():
    # Given: An empty string
    empty_value = ""

    # When: Create ResponseId
    # Then: ValueError is raised
    with pytest.raises(ValueError, match="ResponseId must be a non-empty string"):
        ResponseId(empty_value)


def test_given_two_response_ids_with_same_value_when_compare_then_are_equal():
    # Given: Two ResponseIds with same value
    response_id1 = ResponseId("response-123")
    response_id2 = ResponseId("response-123")

    # When: Compare
    # Then: They are equal
    assert response_id1 == response_id2
    assert hash(response_id1) == hash(response_id2)


def test_given_two_response_ids_with_different_values_when_compare_then_are_not_equal():
    # Given: Two ResponseIds with different values
    response_id1 = ResponseId("response-123")
    response_id2 = ResponseId("response-456")

    # When: Compare
    # Then: They are not equal
    assert response_id1 != response_id2
