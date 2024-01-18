import os

import pytest

import secret_transfer
import secret_transfer.core as core

TEST_KEY = "test_key"
TEST_VALUE = "test_value"


def test_registered():
    key = secret_transfer.EnvSource.__name__
    assert key in core.SourceRegistry.classes
    assert core.SourceRegistry.classes[key] is secret_transfer.EnvSource
    assert "env" in core.SourceRegistry.instances
    assert isinstance(core.SourceRegistry.instances["env"], secret_transfer.EnvSource)


def test_default():
    os.environ[TEST_KEY] = TEST_VALUE

    source = secret_transfer.EnvSource()

    assert source[TEST_KEY] == TEST_VALUE


def test_not_found():
    os.environ.pop(TEST_KEY, None)

    source = secret_transfer.EnvSource()

    with pytest.raises(source.KeyNotFoundError):
        source[TEST_KEY]
