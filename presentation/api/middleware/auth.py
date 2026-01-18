import logging
from typing import Annotated

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from infrastructure.config import get_settings

logger = logging.getLogger(__name__)

security = HTTPBasic()


def get_current_backoffice_user(
    credentials: Annotated[HTTPBasicCredentials, Security(security)],
) -> str:
    settings = get_settings()
    correct_username = settings.backoffice_username
    correct_password = settings.backoffice_password

    if not correct_username or not correct_password:
        logger.warning("Backoffice credentials not configured")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Backoffice authentication not configured",
        )

    is_correct_username = credentials.username == correct_username
    is_correct_password = credentials.password == correct_password

    if not (is_correct_username and is_correct_password):
        logger.warning(
            "Invalid backoffice credentials attempt",
            extra={"username": credentials.username},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    logger.info("Backoffice user authenticated", extra={"username": credentials.username})
    return credentials.username
