import json
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html
from fastapi.openapi.utils import get_openapi
from starlette.responses import HTMLResponse

from infrastructure.config import get_form_repository, get_response_repository, get_settings
from infrastructure.persistence.seed_data import seed_database
from presentation.api.routers import backoffice, gdpr, mobile


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "extra") and record.extra:
            log_data.update(record.extra)
        return json.dumps(log_data)


handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    settings = get_settings()
    logger.info(
        "Starting application",
        extra={"app_name": settings.app_name, "version": settings.app_version},
    )

    form_repository = get_form_repository()
    response_repository = get_response_repository()
    await seed_database(form_repository, response_repository)

    yield
    logger.info("Shutting down application")


app = FastAPI(
    title="Feedback Form System API",
    description="Flexible Multi-Language Feedback Form System",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
)


def custom_openapi() -> dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        openapi_version="3.0.2",
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore[method-assign]


@app.get("/redoc", include_in_schema=False)
async def redoc_html() -> HTMLResponse:
    openapi_url = app.openapi_url or "/openapi.json"
    return get_redoc_html(
        openapi_url=openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.1.3/bundles/redoc.standalone.js",
    )


settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    backoffice.forms.router, prefix="/api/v1/backoffice/forms", tags=["backoffice-forms"]
)
app.include_router(
    backoffice.responses.router,
    prefix="/api/v1/backoffice/responses",
    tags=["backoffice-responses"],
)
app.include_router(mobile.forms.router, prefix="/api/v1/mobile/forms", tags=["mobile-forms"])
app.include_router(
    mobile.responses.router, prefix="/api/v1/mobile/responses", tags=["mobile-responses"]
)
app.include_router(gdpr.data.router, prefix="/api/v1/gdpr/data", tags=["gdpr"])


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy", "version": settings.app_version}
