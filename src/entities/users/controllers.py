from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.entities.users.repositories import InMemoryUserRepository
from src.entities.users.schemas import UserCreateRequest, UserResponse
from src.entities.users.services import UserService

router = APIRouter(prefix="/users", tags=["Users"])

_users_repo = InMemoryUserRepository()
_users_service = UserService(_users_repo)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreateRequest) -> UserResponse:
    user = await _users_service.create_user(payload)
    return UserResponse.model_validate(user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID) -> UserResponse:
    user = await _users_service.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserResponse.model_validate(user)
