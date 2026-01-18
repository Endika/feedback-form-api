from pydantic import BaseModel, Field, field_validator

from application.dto.requests.create_question_request import CreateQuestionRequest


class CreateFormRequest(BaseModel):
    type: str = Field(..., min_length=1)
    name: dict[str, str] = Field(..., min_length=1)
    description: dict[str, str] | None = None
    questions: list[CreateQuestionRequest] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: dict[str, str]) -> dict[str, str]:
        if not v:
            msg = "Name must have at least one translation"
            raise ValueError(msg)
        for lang_code, text in v.items():
            if not lang_code or not isinstance(lang_code, str):
                msg = "Language code must be a non-empty string"
                raise ValueError(msg)
            if not text or not isinstance(text, str) or not text.strip():
                msg = "Translation text must be a non-empty string"
                raise ValueError(msg)
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: dict[str, str] | None) -> dict[str, str] | None:
        if v is None:
            return v
        for lang_code, text in v.items():
            if not lang_code or not isinstance(lang_code, str):
                msg = "Language code must be a non-empty string"
                raise ValueError(msg)
            if not text or not isinstance(text, str) or not text.strip():
                msg = "Translation text must be a non-empty string"
                raise ValueError(msg)
        return v
