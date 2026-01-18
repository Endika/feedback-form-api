class DomainException(Exception):  # noqa: N818
    pass


class FormNotFoundException(DomainException):
    pass


class QuestionNotFoundException(DomainException):
    pass


class ResponseNotFoundException(DomainException):
    pass


class InvalidAnswerException(DomainException):
    pass


class DuplicateQuestionException(DomainException):
    pass
