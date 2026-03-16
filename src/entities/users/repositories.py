from abc import ABC, abstractmethod
from typing import Dict
from uuid import UUID

from src.entities.users.models import User


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None: ...


class InMemoryUserRepository(IUserRepository):
    def __init__(self) -> None:
        self._users: Dict[UUID, User] = {}

    async def create(self, user: User) -> User:
        self._users[user.id] = user
        return user

    async def get_by_id(self, user_id: UUID) -> User | None:
        return self._users.get(user_id)
