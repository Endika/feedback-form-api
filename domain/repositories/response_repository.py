from abc import ABC, abstractmethod

from domain.entities.response import Response
from domain.value_objects.form_id import FormId
from domain.value_objects.response_id import ResponseId


class ResponseRepository(ABC):
    @abstractmethod
    async def create(self, response: Response) -> Response:
        pass

    @abstractmethod
    async def get_by_id(self, response_id: ResponseId) -> Response | None:
        pass

    @abstractmethod
    async def get_by_form_id(self, form_id: FormId) -> list[Response]:
        pass

    @abstractmethod
    async def get_all(self) -> list[Response]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> list[Response]:
        pass

    @abstractmethod
    async def delete_by_user_id(self, user_id: str) -> int:
        pass
