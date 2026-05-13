from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TimestampMixinSchema(BaseModel):
    created_at: datetime
    updated_at: datetime


class CreatedAtMixinSchema(BaseModel):
    created_at: datetime


class UuidMixinSchema(BaseModel):
    id: UUID


class IdMixinSchema(BaseModel):
    id: int
