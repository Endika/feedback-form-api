from dataclasses import dataclass, field
from datetime import datetime

from domain.entities.question import Question
from domain.value_objects.form_id import FormId
from domain.value_objects.form_type import FormType
from domain.value_objects.multilingual_text import MultilingualText


@dataclass
class Form:
    id: FormId
    type: FormType
    name: MultilingualText
    description: MultilingualText | None = None
    questions: list[Question] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def add_question(self, question: Question) -> None:
        if question.id in [q.id for q in self.questions]:
            msg = f"Question with id {question.id} already exists in form"
            raise ValueError(msg)
        self.questions.append(question)

    def remove_question(self, question_id: str) -> None:
        self.questions = [q for q in self.questions if str(q.id) != question_id]

    def get_question(self, question_id: str) -> Question | None:
        for question in self.questions:
            if str(question.id) == question_id:
                return question
        return None
