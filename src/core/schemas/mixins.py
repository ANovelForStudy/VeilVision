from datetime import datetime

from pydantic import BaseModel


class TimestampMixinSchema(BaseModel):
    created_at: datetime
    updated_at: datetime
