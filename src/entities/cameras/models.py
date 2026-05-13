from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import BaseModel
from src.core.models.mixins import TimestampMixinModel, UuidMixinModel


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
        # ! TODO: Add index for filters
        comment="Camera location",
    )

    rtsp_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True,
        comment="Camera RTSP URL",
    )

    webrtc_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="WebRTC URL to connect to the stream in a browser",
    )

    # Relationships
    events: Mapped[list["EventModel"]] = relationship(
        "EventModel",
        back_populates="camera",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"<CameraModel(name={self.name}, id={self.id})>"
