from fastapi import APIRouter, FastAPI

from src.entities.cameras.controllers import cameras_router
from src.entities.users.controllers import users_router


def include_routers(app: FastAPI) -> None:
    main_api_router = APIRouter(prefix="/api")

    routers: list[APIRouter] = [
        users_router,
        cameras_router,
    ]

    for router in routers:
        main_api_router.include_router(router)

    app.include_router(main_api_router)
