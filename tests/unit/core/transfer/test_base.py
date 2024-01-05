import pytest_mock

import secret_transfer.core as core


def test_abstract_class_not_registered():
    assert core.AbstractTransfer.__name__ not in core.TransferRegistry.classes


def test_register(mocker: pytest_mock.MockFixture):
    class TestTransfer(core.AbstractTransfer):
        __register__ = False

    name = "test_name"

    test_source = TestTransfer()
    test_source.register(name)

    assert name in core.TransferRegistry.instances
    assert test_source is core.TransferRegistry.instances[name]
