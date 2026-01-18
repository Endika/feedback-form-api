from pydantic import BaseModel, field_validator

MIN_MULTIPLE_CHOICE_OPTIONS = 2


class UpdateQuestionRequest(BaseModel):
    type: str | None = None
    text: dict[str, str] | None = None
    required: bool | None = None
    options: list[dict[str, str]] | None = None
    min_rating: int | None = None
    max_rating: int | None = None

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: dict[str, str] | None) -> dict[str, str] | None:
        if v is None:
            return v
        if not v:
            msg = "Text must have at least one translation"
            raise ValueError(msg)
        for lang_code, text_value in v.items():
            if not lang_code or not isinstance(lang_code, str):
                msg = "Language code must be a non-empty string"
                raise ValueError(msg)
            if not text_value or not isinstance(text_value, str) or not text_value.strip():
                msg = "Translation text must be a non-empty string"
                raise ValueError(msg)
        return v

    @field_validator("options")
    @classmethod
    def validate_options(cls, v: list[dict[str, str]] | None) -> list[dict[str, str]] | None:
        if v is None:
            return v
        if len(v) < MIN_MULTIPLE_CHOICE_OPTIONS:
            msg = f"Multiple choice questions must have at least {MIN_MULTIPLE_CHOICE_OPTIONS} options"
            raise ValueError(msg)
        for option in v:
            if not option:
                msg = "Option must have at least one translation"
                raise ValueError(msg)
            for lang_code, text in option.items():
                if not lang_code or not isinstance(lang_code, str):
                    msg = "Language code must be a non-empty string"
                    raise ValueError(msg)
                if not text or not isinstance(text, str) or not text.strip():
                    msg = "Option translation text must be a non-empty string"
                    raise ValueError(msg)
        return v
