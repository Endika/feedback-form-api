from pydantic import BaseModel


class QuestionResponse(BaseModel):
    id: str
    type: str
    text: dict[str, str]
    required: bool
    options: list[dict[str, str]] | None = None
    min_rating: int | None = None
    max_rating: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
