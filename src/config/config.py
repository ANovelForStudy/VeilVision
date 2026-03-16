from dotenv import load_dotenv

from src.config.database import DatabaseSettings


class ApplicationConfig:
    def __init__(self):
        load_dotenv()

        self.database_settings = DatabaseSettings()


application_config = ApplicationConfig()

if __name__ == "__main__":
    print(application_config.database_settings.postgres_dsn.unicode_string())
