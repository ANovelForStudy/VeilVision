from datetime import datetime
from uuid import UUID

import pytest
from pydantic import SecretStr, ValidationError

from src.entities.users.schemas import (
    UserCreateRequestSchema,
    UserDatabaseRecordSchema,
    UserResponseSchema,
)


class TestUserResponse:
    def test_user_response_serialization(self):
        data = {
            "id": "1c4f9fbe-e392-42c5-bed6-9f562a029c1e",
            "username": "test_username",
            "is_active": True,
            "created_at": "2000-01-01T00:00:00",
            "updated_at": "2000-01-01T00:00:00",
        }

        schema = UserResponseSchema(**data)

        assert isinstance(schema.id, UUID)
        assert schema.username == "test_username"
        assert schema.is_active is True
        assert isinstance(schema.created_at, datetime)
        assert isinstance(schema.updated_at, datetime)


class TestUserCreate:
    def test_user_create_request_serialization(self):
        data = {
            "username": "test_username",
            "password": "123456",
        }

        schema = UserCreateRequestSchema(**data)

        assert schema.username == "test_username"
        assert isinstance(schema.password, SecretStr)
        assert schema.password.get_secret_value() == "123456"

    def test_user_create_request_with_invalid_username(self):
        data = {
            "username": "invalid_test_username$",
            "password": "123456",
        }

        with pytest.raises(ValidationError) as exc:
            UserCreateRequestSchema(**data)

        errors = exc.value.errors()
        assert any(error["type"] == "value_error" for error in errors)
        assert any("username" in error["loc"] for error in errors)


class TestUserDatabaseRecord:
    def test_user_database_record_serialization(self):
        data = {
            "id": "1c4f9fbe-e392-42c5-bed6-9f562a029c1e",
            "hashed_password": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",  # sha256 "123456"
            "username": "test_username",
            "is_active": True,
            "created_at": "2000-01-01T00:00:00",
            "updated_at": "2000-01-01T00:00:00",
        }

        schema = UserDatabaseRecordSchema(**data)

        assert isinstance(schema.id, UUID)
        assert isinstance(schema.hashed_password, str)
        assert schema.username == "test_username"
        assert schema.is_active is True
        assert isinstance(schema.created_at, datetime)
        assert isinstance(schema.updated_at, datetime)

    def test_user_database_record_cannot_have_a_password(self):
        data = {
            "id": "1c4f9fbe-e392-42c5-bed6-9f562a029c1e",
            "password": 123456,
            "hashed_password": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",  # sha256 "123456"
            "username": "test_username",
            "is_active": True,
            "created_at": "2000-01-01T00:00:00",
            "updated_at": "2000-01-01T00:00:00",
        }

        with pytest.raises(ValidationError) as exc:
            UserDatabaseRecordSchema(**data)

        errors = exc.value.errors()
        assert any(error["type"] == "extra_forbidden" for error in errors)
        assert any("password" in error["loc"] for error in errors)
