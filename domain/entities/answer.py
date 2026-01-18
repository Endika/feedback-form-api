from dataclasses import dataclass

from domain.value_objects.question_id import QuestionId


@dataclass(frozen=True)
class Answer:
    question_id: QuestionId
    value: str | int | list[str]

    def __post_init__(self) -> None:
        if isinstance(self.value, str) and not self.value.strip():
            msg = "Answer value cannot be empty"
            raise ValueError(msg)
        if isinstance(self.value, list) and len(self.value) == 0:
            msg = "Answer value list cannot be empty"
            raise ValueError(msg)
