from uuid import UUID

from src.entities.users.models import User
from src.entities.users.repositories import IUserRepository
from src.entities.users.schemas import UserCreateRequest


class UserService:
    def __init__(self, users_repo: IUserRepository) -> None:
        self._users_repo = users_repo

    async def create_user(self, payload: UserCreateRequest) -> User:
        user = User.create(
            email=payload.email,
            full_name=payload.full_name,
        )
        return await self._users_repo.create(user)

    async def get_user(self, user_id: UUID) -> User | None:
        return await self._users_repo.get_by_id(user_id)
