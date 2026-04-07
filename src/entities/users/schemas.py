from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator

from src.core.schemas.base import BaseSchema, BaseSchemaWithForbiddenExtra
from src.core.schemas.mixins import TimestampMixinSchema

# =====
# BASE
# =====


class UserBaseSchema(BaseSchema):
    username: str = Field(
        min_length=3,
        max_length=30,
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str | None) -> str | None:
        if value is not None:
            if not value.replace("_", "").isalnum():
                raise ValueError(
                    "Username must contain only letters, numbers and underscores"
                )

        return value


# =====
# REQUESTS
# =====


class UserCreateRequestSchema(UserBaseSchema):
    password: SecretStr = Field(
        min_length=3,
        max_length=32,
    )


class UserCreateWithHashedPasswordRequestSchema(UserBaseSchema):
    hashed_password: str


# =====
# RESPONSES
# =====


class UserResponseSchema(BaseSchemaWithForbiddenExtra, TimestampMixinSchema):
    id: UUID
    username: str = Field(
        min_length=3,
        max_length=30,
    )
    is_active: bool = Field(
        True,
    )


class UserDatabaseRecordSchema(UserResponseSchema):
    hashed_password: str
