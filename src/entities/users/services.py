from src.core.uow import IUnitOfWork
from src.entities.users.password_hasher import IPasswordHasher
from src.entities.users.schemas import (
    UserCreateRequestSchema,
    UserCreateWithHashedPasswordRequestSchema,
    UserResponseSchema,
)


class UserService:
    def __init__(
        self,
        uow: IUnitOfWork,
        password_hasher: IPasswordHasher,
    ):
        self._uow = uow
        self._password_hasher = password_hasher

    # =====
    # CREATE
    # =====

    async def create_user(
        self,
        user_data: UserCreateRequestSchema,
    ) -> UserResponseSchema:
        async with self._uow:
            existing_user: (
                UserResponseSchema | None
            ) = await self._uow.user_repository.get_user_by_username(
                username=user_data.username,
            )

            if existing_user:
                # ! TODO: Add custom exception
                raise Exception

            hashed_password = self._password_hasher.hash(
                user_data.password.get_secret_value(),
            )

            user_data_with_hashed_password = UserCreateWithHashedPasswordRequestSchema(
                username=user_data.username,
                hashed_password=hashed_password,
            )

            created_user: UserResponseSchema = (
                await self._uow.user_repository.create_user(
                    user_data=user_data_with_hashed_password,
                )
            )

            await self._uow.commit()
            return created_user

    # =====
    # READ
    # =====

    async def get_all_users(self) -> list[UserResponseSchema]:
        async with self._uow:
            users = await self._uow.user_repository.get_all_users()

        return users
