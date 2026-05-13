from abc import ABC, abstractmethod

from src.entities.cameras.repositories import ICameraRepository
from src.entities.events.repositories import IEventRepository
from src.entities.users.repositories import IUserRepository


class IUnitOfWork(ABC):
    user_repository: IUserRepository | None
    camera_repository: ICameraRepository | None
    event_repository: IEventRepository | None

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
