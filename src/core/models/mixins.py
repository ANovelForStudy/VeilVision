import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixinModel:
    __abstract__ = True

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        default=datetime.now,
        # server_default=func.now(),
        # server_onupdate=func.now(),
        nullable=False,
        sort_order=99,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        default=datetime.now,
        # server_default=func.now(),
        nullable=False,
        sort_order=100,
    )


class CreatedAtMixinModel:
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        default=datetime.now,
        # server_default=func.now(),
        nullable=False,
        sort_order=100,
    )


class UuidMixinModel:
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(
            as_uuid=True,
        ),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        sort_order=-1,
    )
