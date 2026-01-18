from pydantic import BaseModel


class AnswerResponse(BaseModel):
    question_id: str
    value: str | int | list[str]
