from sqlalchemy.orm import DeclarativeBase

from src.core.models.base import BaseModel


def test_base_model_inherits_declarative_base():
    assert issubclass(
        BaseModel,
        DeclarativeBase,
    )
