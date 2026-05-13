from uuid import UUID

from pydantic import (
    Field,
    NonNegativeFloat,
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
    image_path: str | None = Field(
        None,
        max_length=500,
        description="Path to the saved event snapshot/image",
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
    BaseSchema,
    IdMixinSchema,
):
    camera_id: UUID
