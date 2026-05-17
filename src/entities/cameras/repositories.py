from typing import Protocol
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.cameras.models import CameraModel
from src.entities.cameras.schemas import (
    CameraCreateRequestSchema,
    CameraResponseSchema,
)

# =====
# INTERFACES
# =====


class ICameraRepository(Protocol):
    async def create_camera(
        self,
        camera_data: CameraCreateRequestSchema,
    ) -> CameraResponseSchema: ...

    async def get_all_cameras(
        self,
    ) -> list[CameraResponseSchema]: ...

    async def get_camera_by_rtsp_url(
        self,
        camera_rtsp_url: str,
    ) -> CameraResponseSchema | None: ...

    async def get_camera_by_id(
        self,
        camera_id: UUID,
    ) -> CameraResponseSchema | None: ...

    async def detele_camera_by_id(
        self,
        camera_id: UUID,
    ) -> None: ...


# =====
# IMPLEMENTATIONS
# =====


class SqlAlchemyCameraRepository(ICameraRepository):
    model = CameraModel

    # ! TODO: Rewrite the repository to only work with models without pydantic validation

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    # =====
    # CREATE
    # =====

    async def create_camera(
        self,
        camera_data: CameraCreateRequestSchema,
    ) -> CameraResponseSchema:
        camera_model = self.model(**camera_data.model_dump())

        self._session.add(camera_model)

        await self._session.flush()
        await self._session.refresh(camera_model)

        created_camera = await self.get_camera_by_id(
            camera_id=camera_model.id,
        )

        return CameraResponseSchema.model_validate(created_camera)

    # =====
    # READ
    # =====

    async def get_all_cameras(self) -> list[CameraResponseSchema]:
        query = select(
            self.model,
        )

        query_result = await self._session.execute(
            query,
        )

        camera_models = query_result.scalars()

        return [CameraResponseSchema.model_validate(model) for model in camera_models]

    async def get_camera_by_id(
        self,
        camera_id: UUID,
    ) -> CameraResponseSchema | None:
        query = select(
            self.model,
        ).where(
            self.model.id == camera_id,
        )

        query_result = await self._session.execute(
            query,
        )

        camera_model = query_result.scalar_one_or_none()

        return (
            CameraResponseSchema.model_validate(camera_model) if camera_model else None
        )

    async def get_camera_by_rtsp_url(
        self,
        camera_rtsp_url: str,
    ) -> CameraResponseSchema | None:
        query = select(
            self.model,
        ).where(
            self.model.rtsp_url == camera_rtsp_url,
        )

        query_result = await self._session.execute(
            query,
        )

        camera_model = query_result.scalar_one_or_none()

        return (
            CameraResponseSchema.model_validate(camera_model) if camera_model else None
        )

    # =====
    # DELETE
    # =====

    async def detele_camera_by_id(
        self,
        camera_id: UUID,
    ) -> None:
        query = select(
            self.model,
        ).where(
            self.model.id == camera_id,
        )

        query_result = await self._session.execute(
            query,
        )

        existing_camera = query_result.scalar_one_or_none()

        if existing_camera:
            await self._session.delete(existing_camera)
