from enum import Enum

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: Environment = Field(default=Environment.DEVELOPMENT)
    debug: bool = Field(default=False)
    app_name: str = Field(default="feedback-form-system")
    app_version: str = Field(default="0.1.0")

    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000, ge=1, le=65535)
    api_secret_key: str = Field(..., min_length=32)

    backoffice_username: str = Field(default="admin")
    backoffice_password: str = Field(default="admin")

    log_level: str = Field(default="INFO")

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str | Environment) -> Environment:
        if isinstance(v, str):
            return Environment(v.lower())
        return v

    @property
    def is_development(self) -> bool:
        return self.environment == Environment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        return self.environment == Environment.PRODUCTION


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings  # noqa: PLW0603
    if _settings is None:
        import os

        default_key = "development-secret-key-minimum-32-characters-long-for-testing"
        _settings = Settings(api_secret_key=os.getenv("API_SECRET_KEY", default_key))
    return _settings
