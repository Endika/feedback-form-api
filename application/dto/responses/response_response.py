from pydantic import BaseModel

from application.dto.responses.answer_response import AnswerResponse


class ResponseResponse(BaseModel):
    id: str
    form_id: str
    answers: list[AnswerResponse] = []
    tags: dict[str, str] = {}
    user_id: str | None = None
    submitted_at: str | None = None
