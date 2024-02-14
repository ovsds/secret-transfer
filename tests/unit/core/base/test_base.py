import secret_transfer.core.base.base as base


def test_default_parse_init_arguments():
    init_arguments = {"test_key": "test_value"}
    assert base.BaseResource.parse_init_arguments(**init_arguments) == init_arguments


def test_default_get_default_instances():
    assert base.BaseResource.get_default_instances() == {}
