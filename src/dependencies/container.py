from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import application_config
from src.config.database import DatabaseSettings
from src.core.uow import IUnitOfWork, SQLAlchemyUnitOfWork
from src.database.helpers import DatabaseHelper
from src.database.interfaces import IDatabaseHelper


class AppProvider(Provider):
    scope = Scope.APP

    # =====
    # CONFIGURATIONS
    # =====

    @provide
    def get_database_config(
        self,
    ) -> DatabaseSettings:
        return DatabaseSettings()

    # =====
    # HELPERS
    # =====

    @provide
    def get_database_helper(
        self,
    ) -> IDatabaseHelper:
        return DatabaseHelper(
            url=application_config.database_settings.postgres_dsn.unicode_string(),
        )


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_session(
        self, helper: IDatabaseHelper
    ) -> AsyncGenerator[AsyncSession, None]:
        async for session in helper.get_session():
            yield session

    @provide(scope=Scope.SESSION)
    async def get_uow(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[IUnitOfWork, None]:
        uow = SQLAlchemyUnitOfWork(
            session_factory=session_factory,
        )

        try:
            yield uow
        finally:
            await uow.rollback()
