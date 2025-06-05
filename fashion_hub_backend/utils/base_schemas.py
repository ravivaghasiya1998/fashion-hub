from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_pascal, to_snake
from pydantic_settings import BaseSettings, SettingsConfigDict

# Mapping alias generator names to their corresponding functions
ALIAS_GENERATORS = {
    "to_camel": to_camel,
    "to_snake": to_snake,
    "to_pascal": to_pascal,
}


class PydanticBaseSettings(BaseSettings):
    ALIAS_GENERATOR_NAME: Literal["to_camel", "to_snake", "to_pascal"] = "to_camel"
    POPULATE_BY_NAME: bool = True

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )  # type: ignore [misc]


# Load the settings
config_pydantic = PydanticBaseSettings()


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=ALIAS_GENERATORS.get(config_pydantic.ALIAS_GENERATOR_NAME),
        populate_by_name=config_pydantic.POPULATE_BY_NAME,
    )
