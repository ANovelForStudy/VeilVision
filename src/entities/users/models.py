from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import BaseModel
from src.core.models.mixins import TimestampMixinModel, UuidMixinModel


class UserModel(BaseModel, TimestampMixinModel, UuidMixinModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    def __repr__(self):
        return f"<UserModel(id={self.id}, username={self.username}, is_active={self.is_active})>"
