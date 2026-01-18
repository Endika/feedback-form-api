from dataclasses import dataclass, field
from datetime import datetime

from domain.entities.answer import Answer
from domain.value_objects.form_id import FormId
from domain.value_objects.response_id import ResponseId


@dataclass
class Response:
    id: ResponseId
    form_id: FormId
    answers: list[Answer] = field(default_factory=list)
    tags: dict[str, str] = field(default_factory=dict)
    user_id: str | None = None
    submitted_at: datetime | None = None

    def add_answer(self, answer: Answer) -> None:
        existing_answer = self.get_answer_for_question(str(answer.question_id))
        if existing_answer:
            msg = f"Answer for question {answer.question_id} already exists"
            raise ValueError(msg)
        self.answers.append(answer)

    def get_answer_for_question(self, question_id: str) -> Answer | None:
        for answer in self.answers:
            if str(answer.question_id) == question_id:
                return answer
        return None
