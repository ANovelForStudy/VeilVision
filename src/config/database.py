from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class DatabaseSettings(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: SecretStr
    DATABASE_NAME: str

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
        env_file=".env",
    )

    @property
    def postgres_dsn(self) -> PostgresDsn:
        url = URL.create(
            host=self.HOST,
            port=self.PORT,
            username=self.USER,
            password=self.PASSWORD.get_secret_value(),
            database=self.DATABASE_NAME,
            drivername="postgresql+asyncpg",
        )

        return PostgresDsn(url=url.render_as_string())


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    database_settings = DatabaseSettings()

    print(database_settings.postgres_dsn.unicode_string())
