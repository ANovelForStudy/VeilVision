from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Path, status
from pydantic import PositiveInt

from src.entities.events.schemas import EventCreateRequestSchema, EventResponseSchema
from src.entities.events.services import EventService

events_router = APIRouter(
    prefix="/events",
    # ! TODO: Add auth check
    dependencies=[],
    tags=[
        "Events",
    ],
    route_class=DishkaRoute,
)


# =====
# CREATE
# =====


@events_router.post(
    "/",
    response_model=EventResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    service: FromDishka[EventService],
    event_data: Annotated[
        EventCreateRequestSchema,
        Body(),
    ],
):
    event = await service.create_event(
        event_data=event_data,
    )

    return event


# =====
# READ
# =====


@events_router.get(
    "/",
    response_model=list[EventResponseSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_events(
    service: FromDishka[EventService],
):
    found_events = await service.get_all_events()

    return found_events


@events_router.get(
    "/{event_id}",
    response_model=EventResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_event_by_id(
    service: FromDishka[EventService],
    event_id: Annotated[
        PositiveInt,
        Path(),
    ],
):
    # ! TODO: Add pagination
    found_event = await service.get_event_by_id(
        event_id=event_id,
    )

    return found_event
