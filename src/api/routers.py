from fastapi import APIRouter

from src.entities.users.controllers import router as users_router

api_router = APIRouter(prefix="/api")
api_router.include_router(users_router)
