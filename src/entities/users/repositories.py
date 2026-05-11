from typing import Protocol
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.users.models import UserModel
from src.entities.users.schemas import (
    UserCreateRequestSchema,
    UserCreateWithHashedPasswordRequestSchema,
    UserResponseSchema,
)


class IUserRepository(Protocol):
    async def create_user(
        self,
        user_data: UserCreateWithHashedPasswordRequestSchema,
    ) -> UserResponseSchema: ...

    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> UserResponseSchema | None: ...

    async def get_user_by_username(
        self,
        username: str,
    ) -> UserResponseSchema | None: ...

    # async def update_user(
    #     self,
    #     user_data: UserUpdateRequestSchema,
    # ) -> UserResponseSchema: ...

    # async def update_user_password(
    #     self,
    #     user_id: UUID,
    #     new_password: str,
    # ) -> UserResponseSchema: ...

    async def delete_user_by_id(
        self,
        user_id: UUID,
    ) -> None: ...


class SqlAlchemyUserRepository:
    model = UserModel

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    # =====
    # CREATE
    # =====

    async def create_user(
        self,
        user_data: UserCreateWithHashedPasswordRequestSchema,
    ) -> UserModel:
        user_model = self.model(
            username=user_data.username,
            hashed_password=user_data.hashed_password,
        )

        self._session.add(user_model)
        await self._session.flush()
        await self._session.refresh(user_model)

        return UserResponseSchema.model_validate(user_model)

    # =====
    # READ
    # =====

    async def get_user_by_username(
        self,
        username: str,
    ) -> UserResponseSchema | None:
        query = select(self.model).where(
            UserModel.username == username,
        )

        query_result = await self._session.execute(query)

        user_model = query_result.scalar_one_or_none()

        return UserResponseSchema.model_validate(user_model) if user_model else None

    async def get_all_users(self) -> list[UserResponseSchema]:
        query = select(self.model)

        query_result = await self._session.execute(query)

        user_models = query_result.scalars()

        return [UserResponseSchema.model_validate(model) for model in user_models]
