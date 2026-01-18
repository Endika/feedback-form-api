from application.use_cases.create_form_use_case import CreateFormUseCase
from application.use_cases.delete_form_use_case import DeleteFormUseCase
from application.use_cases.delete_user_data_use_case import DeleteUserDataUseCase
from application.use_cases.export_user_data_use_case import ExportUserDataUseCase
from application.use_cases.get_form_use_case import GetFormUseCase
from application.use_cases.get_responses_use_case import GetResponsesUseCase
from application.use_cases.get_user_data_use_case import GetUserDataUseCase
from application.use_cases.list_forms_use_case import ListFormsUseCase
from application.use_cases.submit_response_use_case import SubmitResponseUseCase
from application.use_cases.update_form_use_case import UpdateFormUseCase
from domain.repositories.form_repository import FormRepository
from domain.repositories.response_repository import ResponseRepository
from infrastructure.persistence import MockFormRepository, MockResponseRepository

_form_repository: FormRepository | None = None
_response_repository: ResponseRepository | None = None


def get_form_repository() -> FormRepository:
    global _form_repository  # noqa: PLW0603
    if _form_repository is None:
        _form_repository = MockFormRepository()
    return _form_repository


def get_response_repository() -> ResponseRepository:
    global _response_repository  # noqa: PLW0603
    if _response_repository is None:
        _response_repository = MockResponseRepository()
    return _response_repository


def get_create_form_use_case() -> CreateFormUseCase:
    return CreateFormUseCase(get_form_repository())


def get_get_form_use_case() -> GetFormUseCase:
    return GetFormUseCase(get_form_repository())


def get_list_forms_use_case() -> ListFormsUseCase:
    return ListFormsUseCase(get_form_repository())


def get_update_form_use_case() -> UpdateFormUseCase:
    return UpdateFormUseCase(get_form_repository())


def get_delete_form_use_case() -> DeleteFormUseCase:
    return DeleteFormUseCase(get_form_repository())


def get_submit_response_use_case() -> SubmitResponseUseCase:
    return SubmitResponseUseCase(get_form_repository(), get_response_repository())


def get_get_responses_use_case() -> GetResponsesUseCase:
    return GetResponsesUseCase(get_response_repository())


def get_get_user_data_use_case() -> GetUserDataUseCase:
    return GetUserDataUseCase(get_response_repository())


def get_delete_user_data_use_case() -> DeleteUserDataUseCase:
    return DeleteUserDataUseCase(get_response_repository())


def get_export_user_data_use_case() -> ExportUserDataUseCase:
    return ExportUserDataUseCase(get_get_user_data_use_case())


def reset_dependencies() -> None:
    global _form_repository, _response_repository  # noqa: PLW0603
    _form_repository = None
    _response_repository = None
