from src.core.uow.interfaces import IUnitOfWork
from src.entities.cameras.schemas import CameraCreateRequestSchema, CameraResponseSchema


class CameraService:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    # =====
    # CREATE
    # =====

    async def create_camera(
        self,
        camera_data: CameraCreateRequestSchema,
    ) -> CameraResponseSchema:
        async with self._uow:
            existing_camera: (
                CameraResponseSchema | None
            ) = await self._uow.camera_repository.get_camera_by_rtsp_url(
                camera_rtsp_url=camera_data.rtsp_url,
            )

            if existing_camera:
                # ! TODO: Add custom exception
                raise Exception("Camera with specified RTSP URL already exists")

            created_camera: CameraResponseSchema = (
                await self._uow.camera_repository.create_camera(
                    camera_data=camera_data,
                )
            )

            await self._uow.commit()

            return created_camera

    # =====
    # READ
    # =====

    async def get_all_cameras(
        self,
    ) -> list[CameraResponseSchema]:
        async with self._uow:
            found_cameras: list[
                CameraResponseSchema
            ] = await self._uow.camera_repository.get_all_cameras()

            return found_cameras

    async def get_camera_by_id(
        self,
        camera_id: int,
    ) -> CameraResponseSchema | None:
        async with self._uow:
            existing_camera: (
                CameraResponseSchema | None
            ) = await self._uow.camera_repository.get_camera_by_id(
                camera_id=camera_id,
            )

            if not existing_camera:
                # ! TODO: Add custom exception
                raise Exception("Camera with specified ID not found")

            return CameraResponseSchema.model_validate(existing_camera)

    async def get_camera_by_rtsp_url(
        self,
        camera_rtsp_url: int,
    ) -> CameraResponseSchema | None:
        async with self._uow:
            existing_camera: (
                CameraResponseSchema | None
            ) = await self._uow.camera_repository.get_camera_by_rtsp_url(
                camera_rtsp_url=camera_rtsp_url,
            )

            if not existing_camera:
                # ! TODO: Add custom exception
                raise Exception("Camera with specified RTSP URL not found")

            return CameraResponseSchema.model_validate(existing_camera)
