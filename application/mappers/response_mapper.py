import uuid
from datetime import UTC, datetime

from application.dto.requests.submit_response_request import SubmitResponseRequest
from application.dto.responses.answer_response import AnswerResponse
from application.dto.responses.response_response import ResponseResponse
from domain.entities.answer import Answer
from domain.entities.response import Response
from domain.value_objects.form_id import FormId
from domain.value_objects.question_id import QuestionId
from domain.value_objects.response_id import ResponseId


class ResponseMapper:
    @staticmethod
    def to_domain(request: SubmitResponseRequest, response_id: str | None = None) -> Response:
        answers = [
            Answer(
                question_id=QuestionId(answer.question_id),
                value=answer.value,
            )
            for answer in request.answers
        ]

        return Response(
            id=ResponseId(response_id or str(uuid.uuid4())),
            form_id=FormId(request.form_id),
            answers=answers,
            tags=request.tags,
            user_id=request.user_id,
            submitted_at=datetime.now(tz=UTC),
        )

    @staticmethod
    def to_response(response: Response) -> ResponseResponse:
        return ResponseResponse(
            id=str(response.id),
            form_id=str(response.form_id),
            answers=[
                AnswerResponse(
                    question_id=str(answer.question_id),
                    value=answer.value,
                )
                for answer in response.answers
            ],
            tags=response.tags,
            user_id=response.user_id,
            submitted_at=response.submitted_at.isoformat() if response.submitted_at else None,
        )
