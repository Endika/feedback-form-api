from domain.entities.response import Response
from domain.repositories.response_repository import ResponseRepository
from domain.value_objects.form_id import FormId
from domain.value_objects.response_id import ResponseId


class MockResponseRepository(ResponseRepository):
    def __init__(self) -> None:
        self._responses: dict[str, Response] = {}

    async def create(self, response: Response) -> Response:
        self._responses[str(response.id)] = response
        return response

    async def get_by_id(self, response_id: ResponseId) -> Response | None:
        return self._responses.get(str(response_id))

    async def get_by_form_id(self, form_id: FormId) -> list[Response]:
        return [r for r in self._responses.values() if str(r.form_id) == str(form_id)]

    async def get_all(self) -> list[Response]:
        return list(self._responses.values())

    async def get_by_user_id(self, user_id: str) -> list[Response]:
        return [r for r in self._responses.values() if r.user_id == user_id]

    async def delete_by_user_id(self, user_id: str) -> int:
        deleted_count = 0
        response_ids_to_delete = [
            str(response.id) for response in self._responses.values() if response.user_id == user_id
        ]
        for response_id in response_ids_to_delete:
            if response_id in self._responses:
                del self._responses[response_id]
                deleted_count += 1
        return deleted_count
