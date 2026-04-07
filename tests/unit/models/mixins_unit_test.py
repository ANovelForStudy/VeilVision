from src.core.models.mixins import TimestampMixinModel, UuidMixinModel


def test_timestamp_mixin_model_is_abstract():
    assert TimestampMixinModel.__abstract__ is True


def test_uuid_mixin_model_is_abstract():
    assert UuidMixinModel.__abstract__ is True
