from uuid import UUID

from pydantic import (
    Field,
    NonNegativeFloat,
    field_validator,
    model_validator,
)

from src.core.schemas.base import BaseSchema
from src.core.schemas.mixins import (
    CreatedAtMixinSchema,
    IdMixinSchema,
)

# =====
# BASE
# =====


class EventBaseSchema(BaseSchema):
    event_type: str = Field(
        ...,
        max_length=100,
        description="Type of the detected event (e.g., 'fire', 'smoke')",
    )
    confidence: NonNegativeFloat = Field(
        default=0.0,
        le=1.0,
        description="Detection confidence score (0.0 to 1.0)",
    )
    storage_filename: str | None = Field(
        None,
        max_length=255,
        description="Event snapshot/image name",
    )


# =====
# REQUESTS
# =====


class EventCreateRequestSchema(EventBaseSchema):
    camera_id: UUID = Field(
        ...,
        description="UUID of the signaled camera",
    )


# =====
# RESPONSES
# =====


class EventResponseSchema(
    CreatedAtMixinSchema,
    EventBaseSchema,
    IdMixinSchema,
):
    camera_id: UUID = Field(
        ...,
        description="UUID of the signaled camera",
    )

    image_url: str | None = Field(
        None,
        description="Dynamically generated absolute URL",
    )

    @model_validator(mode="after")
    def generate_image_url(self) -> "EventResponseSchema":
        if self.storage_filename and self.created_at:
            date_str = self.created_at.strftime("%Y_%m_%d")

            # ! TODO: Get from app settings
            self.image_url = f"http://127.0.0.1:8000/static/images/{date_str}/{self.storage_filename}"
        return self
