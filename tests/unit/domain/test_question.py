import pytest

from domain.entities.question import MIN_MULTIPLE_CHOICE_OPTIONS, Question
from domain.value_objects.multilingual_text import MultilingualText
from domain.value_objects.question_id import QuestionId
from domain.value_objects.question_type import QuestionType


def test_given_valid_text_question_when_create_then_succeeds():
    question = Question(
        id=QuestionId("q1"),
        type=QuestionType.TEXT,
        text=MultilingualText({"en": "What is your name?"}),
        required=True,
    )
    assert question.type == QuestionType.TEXT
    assert question.required is True


def test_given_valid_rating_question_when_create_then_succeeds():
    question = Question(
        id=QuestionId("q1"),
        type=QuestionType.RATING,
        text=MultilingualText({"en": "Rate your satisfaction"}),
        required=True,
        min_rating=1,
        max_rating=5,
    )
    assert question.type == QuestionType.RATING
    assert question.min_rating == 1
    assert question.max_rating == 5  # noqa: PLR2004


def test_given_rating_question_without_limits_when_create_then_raises_error():
    with pytest.raises(ValueError, match="must have min_rating and max_rating"):
        Question(
            id=QuestionId("q1"),
            type=QuestionType.RATING,
            text=MultilingualText({"en": "Rate"}),
            required=True,
        )


def test_given_rating_question_with_invalid_range_when_create_then_raises_error():
    with pytest.raises(ValueError, match="min_rating must be less than max_rating"):
        Question(
            id=QuestionId("q1"),
            type=QuestionType.RATING,
            text=MultilingualText({"en": "Rate"}),
            required=True,
            min_rating=5,
            max_rating=1,
        )


def test_given_valid_multiple_choice_question_when_create_then_succeeds():
    options = [
        MultilingualText({"en": "Option 1"}),
        MultilingualText({"en": "Option 2"}),
    ]
    question = Question(
        id=QuestionId("q1"),
        type=QuestionType.MULTIPLE_CHOICE,
        text=MultilingualText({"en": "Choose an option"}),
        required=True,
        options=options,
    )
    assert question.type == QuestionType.MULTIPLE_CHOICE
    assert question.options is not None
    assert len(question.options) == MIN_MULTIPLE_CHOICE_OPTIONS


def test_given_multiple_choice_question_without_options_when_create_then_raises_error():
    with pytest.raises(ValueError, match="must have at least 2 options"):
        Question(
            id=QuestionId("q1"),
            type=QuestionType.MULTIPLE_CHOICE,
            text=MultilingualText({"en": "Choose"}),
            required=True,
        )


def test_given_text_question_with_rating_constraints_when_create_then_raises_error():
    with pytest.raises(ValueError, match="should not have options or rating constraints"):
        Question(
            id=QuestionId("q1"),
            type=QuestionType.TEXT,
            text=MultilingualText({"en": "Text"}),
            required=True,
            min_rating=1,
            max_rating=5,
        )


def test_given_valid_text_answer_when_validate_then_returns_true():
    question = Question(
        id=QuestionId("q1"),
        type=QuestionType.TEXT,
        text=MultilingualText({"en": "Name"}),
        required=True,
    )
    assert question.validate_answer("John Doe") is True


def test_given_empty_text_answer_when_validate_then_returns_false():
    question = Question(
        id=QuestionId("q1"),
        type=QuestionType.TEXT,
        text=MultilingualText({"en": "Name"}),
        required=True,
    )
    assert question.validate_answer("") is False


def test_given_valid_rating_answer_when_validate_then_returns_true():
    question = Question(
        id=QuestionId("q1"),
        type=QuestionType.RATING,
        text=MultilingualText({"en": "Rate"}),
        required=True,
        min_rating=1,
        max_rating=5,
    )
    assert question.validate_answer(3) is True
    assert question.validate_answer(1) is True
    assert question.validate_answer(5) is True


def test_given_invalid_rating_answer_when_validate_then_returns_false():
    question = Question(
        id=QuestionId("q1"),
        type=QuestionType.RATING,
        text=MultilingualText({"en": "Rate"}),
        required=True,
        min_rating=1,
        max_rating=5,
    )
    assert question.validate_answer(0) is False
    assert question.validate_answer(6) is False
    assert question.validate_answer("3") is False
