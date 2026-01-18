import pytest

from domain.value_objects.form_id import FormId


def test_given_valid_string_when_create_form_id_then_succeeds():
    # Given: A valid string
    form_id_value = "form-123"

    # When: Create FormId
    form_id = FormId(form_id_value)

    # Then: FormId is created successfully
    assert form_id.value == form_id_value
    assert str(form_id) == form_id_value


def test_given_empty_string_when_create_form_id_then_raises_error():
    # Given: An empty string
    empty_value = ""

    # When: Create FormId
    # Then: ValueError is raised
    with pytest.raises(ValueError, match="FormId must be a non-empty string"):
        FormId(empty_value)


def test_given_none_when_create_form_id_then_raises_error():
    # Given: None value
    # When: Create FormId
    # Then: ValueError is raised
    with pytest.raises(ValueError, match="FormId must be a non-empty string"):
        FormId(None)  # type: ignore[arg-type]


def test_given_two_form_ids_with_same_value_when_compare_then_are_equal():
    # Given: Two FormIds with same value
    form_id1 = FormId("form-123")
    form_id2 = FormId("form-123")

    # When: Compare
    # Then: They are equal
    assert form_id1 == form_id2
    assert hash(form_id1) == hash(form_id2)


def test_given_two_form_ids_with_different_values_when_compare_then_are_not_equal():
    # Given: Two FormIds with different values
    form_id1 = FormId("form-123")
    form_id2 = FormId("form-456")

    # When: Compare
    # Then: They are not equal
    assert form_id1 != form_id2


def test_given_form_id_when_convert_to_string_then_returns_value():
    # Given: A FormId
    form_id = FormId("form-123")

    # When: Convert to string
    result = str(form_id)

    # Then: Value is returned
    assert result == "form-123"
