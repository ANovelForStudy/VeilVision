from uuid import UUID

from fastapi import HTTPException, UploadFile, status

from src.core.uow.interfaces import IUnitOfWork
from src.entities.events.managers import IDetectionImageManager
from src.entities.events.schemas import EventCreateRequestSchema, EventResponseSchema


class EventService:
    def __init__(
        self,
        uow: IUnitOfWork,
        # ! TODO: Replace with dishka
        image_manager: IDetectionImageManager,
    ):
        self._uow = uow
        self._image_manager = image_manager

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

    # =====
    # UPDATE
    # =====

    async def upload_event_image(
        self,
        event_id: int,
        image: UploadFile,
    ) -> EventResponseSchema:
        async with self._uow:
            event = await self._uow.event_repository.get_event_by_id(
                event_id=event_id,
            )

            if not event:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Event with id {event_id} not found",
                )

            storage_filename, _ = await self._image_manager.save_upload_file(image)

            print(storage_filename)

            updated_event = await self._uow.event_repository.update_image(
                event_id=event_id,
                storage_filename=storage_filename,
            )

            await self._uow.commit()

            return updated_event
