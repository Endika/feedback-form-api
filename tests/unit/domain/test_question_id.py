import pytest

from domain.value_objects.question_id import QuestionId


def test_given_valid_string_when_create_question_id_then_succeeds():
    # Given: A valid string
    question_id_value = "question-123"

    # When: Create QuestionId
    question_id = QuestionId(question_id_value)

    # Then: QuestionId is created successfully
    assert question_id.value == question_id_value
    assert str(question_id) == question_id_value


def test_given_empty_string_when_create_question_id_then_raises_error():
    # Given: An empty string
    empty_value = ""

    # When: Create QuestionId
    # Then: ValueError is raised
    with pytest.raises(ValueError, match="QuestionId must be a non-empty string"):
        QuestionId(empty_value)


def test_given_two_question_ids_with_same_value_when_compare_then_are_equal():
    # Given: Two QuestionIds with same value
    question_id1 = QuestionId("question-123")
    question_id2 = QuestionId("question-123")

    # When: Compare
    # Then: They are equal
    assert question_id1 == question_id2
    assert hash(question_id1) == hash(question_id2)


def test_given_two_question_ids_with_different_values_when_compare_then_are_not_equal():
    # Given: Two QuestionIds with different values
    question_id1 = QuestionId("question-123")
    question_id2 = QuestionId("question-456")

    # When: Compare
    # Then: They are not equal
    assert question_id1 != question_id2
