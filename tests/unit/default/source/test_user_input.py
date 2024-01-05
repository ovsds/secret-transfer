import pytest_mock

import secret_transfer
import secret_transfer.core as core

TEST_KEY = "test_key"
TEST_VALUE = "test_value"


def test_registered():
    key = secret_transfer.UserInputSource.__name__
    assert key in core.SourceRegistry.classes
    assert core.SourceRegistry.classes[key] is secret_transfer.UserInputSource
    assert "user_input" in core.SourceRegistry.instances
    assert isinstance(core.SourceRegistry.instances["user_input"], secret_transfer.UserInputSource)


def test_default(mocker: pytest_mock.MockFixture):
    mocker.patch("getpass.getpass", return_value=TEST_VALUE)

    source = secret_transfer.UserInputSource()

    assert source[TEST_KEY] == TEST_VALUE
