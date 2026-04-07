from pydantic import PostgresDsn, SecretStr

from src.config.base import BaseConfig


class PostgresSettings(
    BaseConfig,
    env_prefix="POSTGRES_",
):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: SecretStr
    DATABASE_NAME: str

    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            host=self.HOST,
            port=self.PORT,
            username=self.USER,
            password=self.PASSWORD.get_secret_value(),
            path=self.DATABASE_NAME,
            scheme="postgresql+asyncpg",
        )

    @property
    def dsn_unicode_string(self) -> str:
        return self.dsn.unicode_string()
