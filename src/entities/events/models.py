import uuid

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import BaseModel
from src.core.models.mixins import CreatedAtMixinModel


class EventModel(BaseModel, CreatedAtMixinModel):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        sort_order=-10,
    )

    camera_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "cameras.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="Type of the detected event (e.g., 'fire', 'smoke')",
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
        comment="Detection confidence score (0.0 to 1.0)",
    )

    image_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Path to the saved event snapshot/image",
    )

    # Relations
    camera: Mapped["CameraModel"] = relationship(
        "CameraModel",
        back_populates="events",
    )

    def __repr__(self):
        return f"<UserModel(id={self.id}, username={self.username}, is_active={self.is_active})>"
