from src.core.models.mixins import TimestampMixinModel, UUIDMixinModel


def test_timestamp_mixin_model_is_abstract():
    assert TimestampMixinModel.__abstract__ is True


def test_uuid_mixin_model_is_abstract():
    assert UUIDMixinModel.__abstract__ is True
