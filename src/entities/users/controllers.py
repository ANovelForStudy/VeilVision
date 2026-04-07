from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Path, status

from src.entities.users.schemas import UserCreateRequestSchema, UserResponseSchema
from src.entities.users.services import UserService

users_router = APIRouter(
    prefix="/users",
    # ! TODO: Add auth check
    dependencies=[],
    tags=[
        "Users",
    ],
    route_class=DishkaRoute,
)


# =====
# CREATE
# =====


@users_router.post(
    "/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    service: FromDishka[UserService],
    user_data: Annotated[
        UserCreateRequestSchema,
        Body(),
    ],
):
    user = await service.create_user(
        user_data=user_data,
    )

    return user


# =====
# READ
# =====


@users_router.get(
    "/me",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_current_user(): ...


@users_router.get(
    "/{user_id}",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(
    user_id: Annotated[
        UUID,
        Path(),
    ],
): ...


@users_router.get(
    "/",
    response_model=list[UserResponseSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_users(
    service: FromDishka[UserService],
):
    users = await service.get_all_users()

    return users


# =====
# UPDATE
# =====


@users_router.patch(
    "/{user_id}",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_password_by_id(): ...


@users_router.patch(
    "/{username}",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_username_by_id(): ...


# =====
# DELETE
# =====


@users_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_by_id(): ...


@users_router.delete(
    "/{username}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_by_username(): ...
