from domain.entities.form import Form
from domain.repositories.form_repository import FormRepository
from domain.value_objects.form_id import FormId
from domain.value_objects.form_type import FormType


class MockFormRepository(FormRepository):
    def __init__(self) -> None:
        self._forms: dict[str, Form] = {}

    async def create(self, form: Form) -> Form:
        self._forms[str(form.id)] = form
        return form

    async def get_by_id(self, form_id: FormId) -> Form | None:
        return self._forms.get(str(form_id))

    async def get_all(self, form_type: FormType | None = None) -> list[Form]:
        forms = list(self._forms.values())
        if form_type:
            forms = [f for f in forms if f.type == form_type]
        return forms

    async def update(self, form: Form) -> Form:
        if str(form.id) not in self._forms:
            msg = f"Form with id {form.id} not found"
            raise ValueError(msg)
        self._forms[str(form.id)] = form
        return form

    async def delete(self, form_id: FormId) -> None:
        if str(form_id) not in self._forms:
            msg = f"Form with id {form_id} not found"
            raise ValueError(msg)
        del self._forms[str(form_id)]
