from typing import AsyncGenerator, Protocol

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import application_config


class IDatabaseHelper(Protocol):
    def get_session_factory(self) -> async_sessionmaker[AsyncSession]: ...

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]: ...


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
    ):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            pool_size=5,
            max_overflow=10,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self.session_factory

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()


# database_helper = DatabaseHelper(
#     url=application_config.database_settings.postgres_dsn.unicode_string(),
# )
