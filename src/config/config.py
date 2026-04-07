from dotenv import load_dotenv

from src.config.database import PostgresSettings


class Config:
    def __init__(
        self,
        postgres_settings: PostgresSettings | None = None,
    ):
        load_dotenv()

        self.postgres_settings = postgres_settings or PostgresSettings()
