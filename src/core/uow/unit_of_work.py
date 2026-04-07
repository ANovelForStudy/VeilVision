from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.uow.interfaces import IUnitOfWork
from src.entities.users.repositories import IUserRepository, SqlAlchemyUserRepository


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ):
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

        # Repositories
        # ! TODO: Replace it with property for lazy initialization
        self.user_repository: IUserRepository | None = None

    async def __aenter__(self):
        self._session: AsyncSession = self._session_factory()

        self.user_repository = SqlAlchemyUserRepository(session=self._session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

        if self._session:
            await self._session.close()
            self._session = None

    async def commit(self):
        if self._session:
            await self._session.commit()

    async def rollback(self):
        if self._session:
            await self._session.rollback()
