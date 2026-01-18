import uuid
from datetime import UTC, datetime

from application.dto.requests.create_question_request import CreateQuestionRequest
from application.dto.responses.question_response import QuestionResponse
from domain.entities.question import Question
from domain.value_objects.multilingual_text import MultilingualText
from domain.value_objects.question_id import QuestionId
from domain.value_objects.question_type import QuestionType


class QuestionMapper:
    @staticmethod
    def to_domain(request: CreateQuestionRequest, question_id: str | None = None) -> Question:
        options = None
        if request.options:
            options = [MultilingualText(opt) for opt in request.options]

        return Question(
            id=QuestionId(question_id or str(uuid.uuid4())),
            type=QuestionType(request.type),
            text=MultilingualText(request.text),
            required=request.required,
            options=options,
            min_rating=request.min_rating,
            max_rating=request.max_rating,
            created_at=datetime.now(tz=UTC),
            updated_at=datetime.now(tz=UTC),
        )

    @staticmethod
    def to_response(question: Question) -> QuestionResponse:
        options = None
        if question.options:
            options = [opt.translations for opt in question.options]

        return QuestionResponse(
            id=str(question.id),
            type=question.type.value,
            text=question.text.translations,
            required=question.required,
            options=options,
            min_rating=question.min_rating,
            max_rating=question.max_rating,
            created_at=question.created_at.isoformat() if question.created_at else None,
            updated_at=question.updated_at.isoformat() if question.updated_at else None,
        )
