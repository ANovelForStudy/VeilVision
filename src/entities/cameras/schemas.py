from uuid import UUID

from pydantic import Field

from src.core.schemas.base import BaseSchema
from src.core.schemas.mixins import TimestampMixinSchema, UuidMixinSchema
from src.entities.cameras.enums import CameraStatusEnum

# =====
# BASE
# =====


class CameraBaseSchema(BaseSchema):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Camera name",
    )
    # description: str | None = Field(
    #     None,
    #     max_length=500,
    #     description="Camera description",
    # )
    # location: str | None = Field(
    #     None,
    #     max_length=200,
    #     description="Camera location",
    # )
    # ! TODO: Replace it with custom RtspUrl class
    rtsp_url: str = Field(
        ...,
        description="Camera RTSP URL",
    )
    webrtc_url: str = Field(
        ...,
        description="Camera WebRTC URL",
    )
    # is_enabled: bool = Field(
    #     True,
    #     description="Is camera enabled",
    # )

    # def validate_rtsp_url(cls, value): ...

    # def validate_name(cls, value): ...


# =====
# REQUESTS
# =====


class CameraCreateRequestSchema(CameraBaseSchema):
    pass


class CameraUpdateRequestSchema(BaseSchema):
    name: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Camera name",
    )
    # description: str | None = Field(
    #     None,
    #     max_length=500,
    #     description="Camera description",
    # )
    # location: str | None = Field(
    #     None,
    #     max_length=200,
    #     description="Camera location",
    # )
    # ! TODO: Replace it with custom RtspUrl class
    rtsp_url: str | None = Field(
        None,
        description="Camera RTSP URL",
    )
    webrtc_url: str = Field(
        ...,
        description="Camera WebRTC URL",
    )
    # is_enabled: bool | None = Field(
    #     None,
    #     description="Is camera enabled",
    # )

    # def validate_rtsp_url(cls, value): ...

    # def validate_name(cls, value): ...


# =====
# RESPONSES
# =====


class CameraResponseSchema(TimestampMixinSchema, CameraBaseSchema, UuidMixinSchema):
    # status: CameraStatusEnum
    # last_online_at: datetime | None

    # webrtc_url: str | None = Field(
    #     None,
    #     description="WebRTC URL to connect to the stream in a browser",
    # )
    pass


class CameraShortResponseSchema(BaseSchema):
    id: UUID
    name: str
    location: str | None
    status: CameraStatusEnum
    # thumbnail_url: str | None = None
