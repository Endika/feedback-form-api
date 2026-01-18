from pydantic import BaseModel

from application.dto.responses.question_response import QuestionResponse


class FormResponse(BaseModel):
    id: str
    type: str
    name: dict[str, str]
    description: dict[str, str] | None = None
    questions: list[QuestionResponse] = []
    created_at: str | None = None
    updated_at: str | None = None
