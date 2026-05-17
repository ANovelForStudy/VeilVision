from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Path, status

from src.entities.cameras.schemas import CameraCreateRequestSchema, CameraResponseSchema
from src.entities.cameras.services import CameraService
from src.entities.events.schemas import EventResponseSchema
from src.entities.events.services import EventService

cameras_router = APIRouter(
    prefix="/cameras",
    # ! TODO: Add auth check
    dependencies=[],
    tags=[
        "Cameras",
    ],
    route_class=DishkaRoute,
)


# =====
# CREATE
# =====


@cameras_router.post(
    "/",
    response_model=CameraResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_camera(
    service: FromDishka[CameraService],
    camera_data: Annotated[
        CameraCreateRequestSchema,
        Body(),
    ],
):
    created_camera = await service.create_camera(
        camera_data=camera_data,
    )

    return created_camera


# =====
# READ
# =====


@cameras_router.get(
    "/",
    response_model=list[CameraResponseSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_cameras(
    service: FromDishka[CameraService],
):
    found_cameras = await service.get_all_cameras()

    return found_cameras


@cameras_router.get(
    "/{camera_id}",
    response_model=CameraResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_camera_by_id(
    service: FromDishka[CameraService],
    camera_id: Annotated[
        UUID,
        Path(),
    ],
):
    found_camera = await service.get_camera_by_id(
        camera_id=camera_id,
    )

    return found_camera


@cameras_router.get(
    "/{camera_id}/events",
    response_model=list[EventResponseSchema],
    status_code=status.HTTP_200_OK,
)
async def get_camera_events(
    service: FromDishka[EventService],
    camera_id: Annotated[
        UUID,
        Path(),
    ],
):
    found_events = await service.get_camera_events(
        camera_id=camera_id,
    )

    return found_events


# =====
# DELETE
# =====


@cameras_router.delete(
    "/{camera_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_camera_by_id(
    service: FromDishka[CameraService],
    camera_id: Annotated[
        UUID,
        Path(),
    ],
):
    await service.detele_camera_by_id(
        camera_id=camera_id,
    )
