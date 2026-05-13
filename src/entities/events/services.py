from uuid import UUID

from src.core.uow.interfaces import IUnitOfWork
from src.entities.cameras.schemas import CameraCreateRequestSchema, CameraResponseSchema
from src.entities.events.schemas import EventCreateRequestSchema, EventResponseSchema


class EventService:
    def __init__(
        self,
        uow: IUnitOfWork,
    ):
        self._uow = uow

    # =====
    # CREATE
    # =====

    async def create_event(
        self,
        event_data: EventCreateRequestSchema,
    ) -> EventResponseSchema:
        async with self._uow:
            created_event: EventResponseSchema = (
                await self._uow.event_repository.create_event(
                    event_data=event_data,
                )
            )

            await self._uow.commit()

            return created_event

    # =====
    # READ
    # =====

    async def get_all_events(
        self,
    ) -> list[EventResponseSchema]:
        # ! Add paginating
        async with self._uow:
            found_events: list[
                EventResponseSchema
            ] = await self._uow.event_repository.get_all_events()

            return found_events

    async def get_event_by_id(
        self,
        event_id: int,
    ) -> EventResponseSchema:
        async with self._uow:
            found_event: EventResponseSchema = (
                await self._uow.event_repository.get_event_by_id(
                    event_id=event_id,
                )
            )

            return found_event

    async def get_camera_events(
        self,
        camera_id: UUID,
    ) -> list[EventResponseSchema]:
        # ! TODO: Move this method to camera entity
        async with self._uow:
            found_events: list[
                EventResponseSchema
            ] = await self._uow.event_repository.get_camera_events(
                camera_id=camera_id,
            )

            return found_events
