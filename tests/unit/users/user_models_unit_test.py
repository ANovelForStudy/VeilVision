from sqlalchemy import UUID as SQLAlchemyUUID
from sqlalchemy import Boolean, DateTime, String

from src.core.models.base import (
    BaseModel,
)
from src.entities.users.models import (
    UserModel,
)


def test_user_model_inherits_base():
    assert issubclass(
        UserModel,
        BaseModel,
    )


def test_user_model_table_name():
    assert UserModel.__tablename__ == "users"


def test_user_model_has_required_columns():
    required_attrs = {
        "id",
        "username",
        "hashed_password",
        "is_active",
        "created_at",
        "updated_at",
    }
    for attr in required_attrs:
        assert hasattr(UserModel, attr), f"Missing attribute '{attr}'"

    columns = {column.name for column in UserModel.__table__.columns}
    assert required_attrs.issubset(columns), (
        f"Missing columns: {required_attrs - columns}"
    )


def test_user_model_column_types():
    id_col = UserModel.__table__.columns["id"]
    assert isinstance(id_col.type, SQLAlchemyUUID)

    username_col = UserModel.__table__.columns["username"]
    assert isinstance(username_col.type, String)
    assert username_col.type.length == 30

    hashed_password_col = UserModel.__table__.columns["hashed_password"]
    assert isinstance(hashed_password_col.type, String)

    is_active_col = UserModel.__table__.columns["is_active"]
    assert isinstance(is_active_col.type, Boolean)

    created_at_col = UserModel.__table__.columns["created_at"]
    assert isinstance(created_at_col.type, DateTime)

    updated_at_col = UserModel.__table__.columns["updated_at"]
    assert isinstance(updated_at_col.type, DateTime)


def test_user_model_constraints():
    assert UserModel.id.primary_key

    assert UserModel.username.unique

    assert not UserModel.id.nullable
    assert not UserModel.username.nullable
    assert not UserModel.hashed_password.nullable
    assert not UserModel.created_at.nullable
    assert not UserModel.updated_at.nullable


def test_user_model_default_values():
    assert UserModel.is_active.default.arg is True

    assert UserModel.created_at.server_default is not None
    assert UserModel.updated_at.server_onupdate is not None


def test_user_model_repr():
    user = UserModel(
        username="testuser",
        hashed_password="8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
    )

    repr_str = repr(user)

    assert "UserModel" in repr_str
    assert user.username in repr_str
    assert str(user.id) in repr_str
