from typing import Protocol
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.entities.events.models import EventModel
from src.entities.events.schemas import EventCreateRequestSchema, EventResponseSchema

# =====
# INTERFACES
# =====


class IEventRepository(Protocol):
    async def create_event(
        self,
        event_data: EventCreateRequestSchema,
    ) -> EventResponseSchema: ...

    async def get_all_events(
        self,
    ) -> list[EventResponseSchema]: ...

    async def get_camera_events(
        self,
        camera_id: UUID,
    ) -> list[EventResponseSchema]: ...

    async def get_event_by_id(
        self,
        event_id: int,
    ) -> EventResponseSchema | None: ...


# =====
# IMPLEMENTATIONS
# =====


class SqlAlchemyEventRepository(IEventRepository):
    model = EventModel

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    # =====
    # CREATE
    # =====

    async def create_event(
        self,
        event_data: EventCreateRequestSchema,
    ) -> EventResponseSchema:
        event_model: EventModel = self.model(**event_data.model_dump())

        self._session.add(event_model)

        await self._session.flush()
        await self._session.refresh(event_model)

        created_event = await self.get_event_by_id(
            event_id=event_model.id,
        )

        return EventResponseSchema.model_validate(created_event)

    # =====
    # READ
    # =====

    async def get_all_events(
        self,
    ) -> list[EventResponseSchema]:
        query = select(
            self.model,
        )

        query_result = await self._session.execute(
            query,
        )

        event_models = query_result.scalars()

        return [EventResponseSchema.model_validate(model) for model in event_models]

    async def get_event_by_id(
        self,
        event_id: int,
    ) -> EventResponseSchema | None:
        query = select(
            self.model,
        ).where(
            self.model.id == event_id,
        )

        query_result = await self._session.execute(
            query,
        )

        event_model = query_result.scalar_one_or_none()

        return EventResponseSchema.model_validate(event_model) if event_model else None

    async def get_camera_events(
        self,
        camera_id: UUID,
    ) -> list[EventResponseSchema]:
        query = select(
            self.model,
        ).where(
            self.model.camera_id == camera_id,
        )

        query_result = await self._session.execute(
            query,
        )

        event_models = query_result.scalars()

        return [EventResponseSchema.model_validate(model) for model in event_models]
