from enum import Enum


class QuestionType(str, Enum):
    TEXT = "text"
    RATING = "rating"
    MULTIPLE_CHOICE = "multiple_choice"
