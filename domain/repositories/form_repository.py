from abc import ABC, abstractmethod

from domain.entities.form import Form
from domain.value_objects.form_id import FormId
from domain.value_objects.form_type import FormType


class FormRepository(ABC):
    @abstractmethod
    async def create(self, form: Form) -> Form:
        pass

    @abstractmethod
    async def get_by_id(self, form_id: FormId) -> Form | None:
        pass

    @abstractmethod
    async def get_all(self, form_type: FormType | None = None) -> list[Form]:
        pass

    @abstractmethod
    async def update(self, form: Form) -> Form:
        pass

    @abstractmethod
    async def delete(self, form_id: FormId) -> None:
        pass
