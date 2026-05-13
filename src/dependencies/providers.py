from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.config.database import PostgresSettings
from src.core.uow import IUnitOfWork, SqlAlchemyUnitOfWork
from src.database.helpers import DatabaseHelper
from src.database.interfaces import IDatabaseHelper
from src.entities.cameras.services import CameraService
from src.entities.events.services import EventService
from src.entities.users.password_hasher import BcryptPasswordHasher, IPasswordHasher
from src.entities.users.services import UserService


class AppProvider(Provider):
    scope = Scope.APP

    # =====
    # CONFIGURATIONS
    # =====

    @provide
    def get_database_config(
        self,
    ) -> PostgresSettings:
        return PostgresSettings()

    # =====
    # HELPERS
    # =====

    @provide
    def get_database_helper(
        self,
        config: PostgresSettings,
    ) -> IDatabaseHelper:
        return DatabaseHelper(
            url=config.dsn_unicode_string,
        )


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(
        self,
        helper: IDatabaseHelper,
    ) -> AsyncEngine:
        engine = helper.get_engine()

        return engine

    @provide(scope=Scope.APP)
    async def get_session(
        self,
        helper: IDatabaseHelper,
    ) -> AsyncGenerator[AsyncSession, None]:
        async for session in helper.get_session():
            yield session

    @provide(scope=Scope.SESSION)
    async def get_session_factory(
        self,
        helper: IDatabaseHelper,
    ) -> async_sessionmaker[AsyncSession]:
        session_factory = helper.get_session_factory()

        return session_factory

    @provide(scope=Scope.SESSION)
    async def get_uow(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[IUnitOfWork, None]:
        uow = SqlAlchemyUnitOfWork(
            session_factory=session_factory,
        )

        try:
            yield uow
        finally:
            await uow.rollback()


class UtilsProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_password_hasher(
        self,
    ) -> IPasswordHasher:
        return BcryptPasswordHasher()


class ServicesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_user_service(
        self,
        uow: IUnitOfWork,
        password_hasher: IPasswordHasher,
    ) -> UserService:
        return UserService(
            uow=uow,
            password_hasher=password_hasher,
        )

    @provide
    async def get_camera_service(
        self,
        uow: IUnitOfWork,
    ) -> CameraService:
        return CameraService(
            uow=uow,
        )

    @provide
    async def get_event_service(
        self,
        uow: IUnitOfWork,
    ) -> EventService:
        return EventService(
            uow=uow,
        )


def get_all_providers() -> list[Provider]:
    return [
        AppProvider(),
        DatabaseProvider(),
        UtilsProvider(),
        ServicesProvider(),
    ]
