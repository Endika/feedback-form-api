import json
import logging

from application.use_cases.get_user_data_use_case import GetUserDataUseCase

logger = logging.getLogger(__name__)


class ExportUserDataUseCase:
    def __init__(self, get_user_data_use_case: GetUserDataUseCase) -> None:
        self._get_user_data_use_case = get_user_data_use_case

    async def execute(self, user_id: str) -> str:
        logger.info("Exporting user data", extra={"user_id": user_id})
        responses = await self._get_user_data_use_case.execute(user_id)
        export_data = {
            "user_id": user_id,
            "exported_at": responses[0].submitted_at if responses else None,
            "total_responses": len(responses),
            "responses": [response.model_dump() for response in responses],
        }
        export_json = json.dumps(export_data, indent=2, ensure_ascii=False)
        logger.info(
            "User data exported successfully",
            extra={"user_id": user_id, "response_count": len(responses)},
        )
        return export_json
