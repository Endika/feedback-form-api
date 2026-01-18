from pydantic import BaseModel, field_validator

from application.dto.requests.create_question_request import CreateQuestionRequest


class UpdateFormRequest(BaseModel):
    type: str | None = None
    name: dict[str, str] | None = None
    description: dict[str, str] | None = None
    questions: list[CreateQuestionRequest] | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: dict[str, str] | None) -> dict[str, str] | None:
        if v is None:
            return v
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
