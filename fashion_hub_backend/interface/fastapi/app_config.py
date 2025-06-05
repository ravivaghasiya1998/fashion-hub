from enum import StrEnum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunMode(StrEnum):
    PROD = "PROD"
    DEBUG = "DEBUG"


class AppConfig(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    run_mode: RunMode = Field(RunMode.PROD, validation_alias="TESTGPT_RUN_MODE")
    debug_sql_echo: bool = False
    """If set to true, set sqlachemy echo option to print all SQL statements"""

    basic_auth_password: str | None = None


config = AppConfig()
