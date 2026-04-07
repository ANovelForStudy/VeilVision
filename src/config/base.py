from pydantic_settings import BaseSettings


class BaseConfig(
    BaseSettings,
    env_file=".env",
    extra="ignore",
): ...
