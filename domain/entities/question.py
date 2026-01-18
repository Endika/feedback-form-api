from dataclasses import dataclass
from datetime import datetime

from domain.value_objects.multilingual_text import MultilingualText
from domain.value_objects.question_id import QuestionId
from domain.value_objects.question_type import QuestionType

MIN_MULTIPLE_CHOICE_OPTIONS = 2


@dataclass
class Question:
    id: QuestionId
    type: QuestionType
    text: MultilingualText
    required: bool
    options: list[MultilingualText] | None = None
    min_rating: int | None = None
    max_rating: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.type == QuestionType.MULTIPLE_CHOICE:
            if not self.options or len(self.options) < MIN_MULTIPLE_CHOICE_OPTIONS:
                msg = "Multiple choice questions must have at least 2 options"
                raise ValueError(msg)
        elif self.type == QuestionType.RATING:
            if self.min_rating is None or self.max_rating is None:
                msg = "Rating questions must have min_rating and max_rating"
                raise ValueError(msg)
            if self.min_rating >= self.max_rating:
                msg = "min_rating must be less than max_rating"
                raise ValueError(msg)
        elif self.type == QuestionType.TEXT and (
            self.options is not None or self.min_rating is not None or self.max_rating is not None
        ):
            msg = "Text questions should not have options or rating constraints"
            raise ValueError(msg)

    def validate_answer(self, answer_value: str | int | list[str]) -> bool:  # noqa: PLR0911
        if self.type == QuestionType.TEXT:
            return isinstance(answer_value, str) and len(answer_value.strip()) > 0
        if self.type == QuestionType.RATING:
            if not isinstance(answer_value, int):
                return False
            if self.min_rating is None or self.max_rating is None:
                return False
            return self.min_rating <= answer_value <= self.max_rating
        if self.type == QuestionType.MULTIPLE_CHOICE:
            if not isinstance(answer_value, list):
                return False
            if not self.options:
                return False
            available_options = [opt.get_text("en") for opt in self.options]
            return all(opt in available_options for opt in answer_value)
        return False
