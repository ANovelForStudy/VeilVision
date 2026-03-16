from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class IUnitOfWork(ABC):
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ):
        self.session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

        if self.session:
            await self.session.close()
            self.session = None

    async def commit(self):
        if self.session:
            await self.session.commit()

    async def rollback(self):
        if self.session:
            await self.session.rollback()
