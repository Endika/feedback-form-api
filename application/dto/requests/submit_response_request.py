from pydantic import BaseModel, Field


class AnswerRequest(BaseModel):
    question_id: str = Field(..., min_length=1)
    value: str | int | list[str] = Field(...)


class SubmitResponseRequest(BaseModel):
    form_id: str = Field(..., min_length=1)
    answers: list[AnswerRequest] = Field(..., min_length=1)
    tags: dict[str, str] = Field(default_factory=dict)
    user_id: str | None = Field(None, description="User identifier for GDPR compliance")
