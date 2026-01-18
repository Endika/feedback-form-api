from pydantic import BaseModel, Field, field_validator, model_validator

MIN_MULTIPLE_CHOICE_OPTIONS = 2


class CreateQuestionRequest(BaseModel):
    type: str = Field(..., min_length=1)
    text: dict[str, str] = Field(..., min_length=1)
    required: bool = Field(default=False)
    options: list[dict[str, str]] | None = None
    min_rating: int | None = None
    max_rating: int | None = None

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: dict[str, str]) -> dict[str, str]:
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

    @model_validator(mode="after")
    def validate_question_type_constraints(self) -> "CreateQuestionRequest":
        if self.type == "multiple_choice":
            if not self.options or len(self.options) < MIN_MULTIPLE_CHOICE_OPTIONS:
                msg = "Multiple choice questions must have at least 2 options"
                raise ValueError(msg)
        elif self.type == "rating":
            if self.min_rating is None or self.max_rating is None:
                msg = "Rating questions must have min_rating and max_rating"
                raise ValueError(msg)
            if self.min_rating >= self.max_rating:
                msg = "min_rating must be less than max_rating"
                raise ValueError(msg)
        elif self.type == "text" and (
            self.options is not None or self.min_rating is not None or self.max_rating is not None
        ):
            msg = "Text questions should not have options or rating constraints"
            raise ValueError(msg)
        return self
