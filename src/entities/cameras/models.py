from sqlalchemy import Boolean, String, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import BaseModel
from src.core.models.mixins import TimestampMixinModel, UuidMixinModel
from src.entities.cameras.enums import CameraStatusEnum


class CameraModel(BaseModel, UuidMixinModel, TimestampMixinModel):
    __tablename__ = "cameras"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="Camera name",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Camera description",
    )

    location: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        comment="Camera location",
    )

    rtsp_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        # TODO!: Add index
        unique=True,
        comment="Camera RTSP URL",
    )

    webrtc_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="WebRTC URL to connect to the stream in a browser",
    )

    # status: Mapped[CameraStatusEnum] = mapped_column(
    #     SqlEnum(
    #         CameraStatusEnum,
    #         create_constraint=True,
    #     ),
    #     nullable=False,
    #     default=CameraStatusEnum.UNKNOWN,
    #     index=True,
    #     comment="Current camera status",
    # )

    # is_enabled: Mapped[bool] = mapped_column(
    #     Boolean,
    #     nullable=False,
    #     default=True,
    #     index=True,
    #     comment="Is camera enabled",
    # )

    # last_online_at: Mapped[datetime | None] = mapped_column(
    #     DateTime(timezone=True),
    #     nullable=True,
    #     comment="Last successful connection time",
    # )

    # created_by: ...

    def __repr__(self):
        return super().__repr__()
