import pytest

from domain.entities.answer import Answer
from domain.entities.response import Response
from domain.value_objects.form_id import FormId
from domain.value_objects.question_id import QuestionId
from domain.value_objects.response_id import ResponseId


def test_given_response_when_add_answer_then_answer_is_added():
    # Given: A response
    response = Response(
        id=ResponseId("response-1"),
        form_id=FormId("form-1"),
    )
    answer = Answer(question_id=QuestionId("q-1"), value=5)

    # When: Add answer
    response.add_answer(answer)

    # Then: Answer is added
    assert len(response.answers) == 1
    assert response.answers[0] == answer


def test_given_response_with_existing_answer_when_add_duplicate_answer_then_raises_error():
    # Given: A response with an answer
    response = Response(
        id=ResponseId("response-1"),
        form_id=FormId("form-1"),
    )
    answer = Answer(question_id=QuestionId("q-1"), value=5)
    response.add_answer(answer)

    # When: Add duplicate answer
    # Then: ValueError is raised
    duplicate_answer = Answer(question_id=QuestionId("q-1"), value=4)
    with pytest.raises(ValueError, match="already exists"):
        response.add_answer(duplicate_answer)


def test_given_response_with_answers_when_get_answer_for_question_then_returns_answer():
    # Given: A response with answers
    response = Response(
        id=ResponseId("response-1"),
        form_id=FormId("form-1"),
    )
    answer1 = Answer(question_id=QuestionId("q-1"), value=5)
    answer2 = Answer(question_id=QuestionId("q-2"), value="Good")
    response.add_answer(answer1)
    response.add_answer(answer2)

    # When: Get answer for question
    result = response.get_answer_for_question("q-1")

    # Then: Answer is returned
    expected_rating_value = 5
    assert result == answer1
    assert result.value == expected_rating_value


def test_given_response_without_answer_for_question_when_get_answer_for_question_then_returns_none():
    # Given: A response without answer for question
    response = Response(
        id=ResponseId("response-1"),
        form_id=FormId("form-1"),
    )
    answer = Answer(question_id=QuestionId("q-1"), value=5)
    response.add_answer(answer)

    # When: Get answer for non-existent question
    result = response.get_answer_for_question("q-999")

    # Then: None is returned
    assert result is None


def test_given_response_when_add_multiple_answers_then_all_answers_are_stored():
    # Given: A response
    response = Response(
        id=ResponseId("response-1"),
        form_id=FormId("form-1"),
    )

    # When: Add multiple answers
    answer1 = Answer(question_id=QuestionId("q-1"), value=5)
    answer2 = Answer(question_id=QuestionId("q-2"), value="Good")
    answer3 = Answer(question_id=QuestionId("q-3"), value=["option1", "option2"])

    response.add_answer(answer1)
    response.add_answer(answer2)
    response.add_answer(answer3)

    # Then: All answers are stored
    expected_answer_count = 3
    assert len(response.answers) == expected_answer_count
    assert response.get_answer_for_question("q-1") == answer1
    assert response.get_answer_for_question("q-2") == answer2
    assert response.get_answer_for_question("q-3") == answer3
