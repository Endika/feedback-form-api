import logging

from application.dto.requests.submit_response_request import SubmitResponseRequest
from application.dto.responses.response_response import ResponseResponse
from application.mappers.response_mapper import ResponseMapper
from domain.exceptions import FormNotFoundException, InvalidAnswerException
from domain.repositories.form_repository import FormRepository
from domain.repositories.response_repository import ResponseRepository
from domain.value_objects.form_id import FormId

logger = logging.getLogger(__name__)


class SubmitResponseUseCase:
    def __init__(
        self,
        form_repository: FormRepository,
        response_repository: ResponseRepository,
    ) -> None:
        self._form_repository = form_repository
        self._response_repository = response_repository

    async def execute(self, request: SubmitResponseRequest) -> ResponseResponse:
        logger.info("Submitting response", extra={"form_id": request.form_id})
        form = await self._form_repository.get_by_id(FormId(request.form_id))
        if not form:
            logger.warning("Form not found", extra={"form_id": request.form_id})
            msg = f"Form with id {request.form_id} not found"
            raise FormNotFoundException(msg)

        response = ResponseMapper.to_domain(request)

        for answer in response.answers:
            question = form.get_question(str(answer.question_id))
            if not question:
                logger.warning(
                    "Question not found in form",
                    extra={"form_id": request.form_id, "question_id": str(answer.question_id)},
                )
                msg = f"Question {answer.question_id} not found in form {request.form_id}"
                raise InvalidAnswerException(msg)
            if question.required:
                if isinstance(answer.value, str) and not answer.value.strip():
                    logger.warning(
                        "Required question not answered",
                        extra={"form_id": request.form_id, "question_id": str(answer.question_id)},
                    )
                    msg = f"Question {answer.question_id} is required but not answered"
                    raise InvalidAnswerException(msg)
                if isinstance(answer.value, list) and len(answer.value) == 0:
                    logger.warning(
                        "Required question not answered",
                        extra={"form_id": request.form_id, "question_id": str(answer.question_id)},
                    )
                    msg = f"Question {answer.question_id} is required but not answered"
                    raise InvalidAnswerException(msg)
            if not question.validate_answer(answer.value):
                logger.warning(
                    "Invalid answer value",
                    extra={
                        "form_id": request.form_id,
                        "question_id": str(answer.question_id),
                        "question_type": question.type.value,
                    },
                )
                msg = f"Invalid answer value for question {answer.question_id}"
                raise InvalidAnswerException(msg)

        created_response = await self._response_repository.create(response)
        logger.info(
            "Response submitted successfully", extra={"response_id": str(created_response.id)}
        )
        return ResponseMapper.to_response(created_response)
