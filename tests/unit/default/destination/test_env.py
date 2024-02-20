import os

import secret_transfer
import secret_transfer.core as core

TEST_KEY = "test_key"
TEST_VALUE = "test_value"


def test_registered():
    key = secret_transfer.EnvDestination.__name__
    assert key in core.DestinationRegistry.classes
    assert core.DestinationRegistry.classes[key] is secret_transfer.EnvDestination
    assert "env" in core.DestinationRegistry.instances
    assert isinstance(core.DestinationRegistry.instances["env"], secret_transfer.EnvDestination)


def test_set():
    destination = secret_transfer.EnvDestination()
    destination[TEST_KEY] = TEST_VALUE

    assert os.environ.get(TEST_KEY) == TEST_VALUE


def test_set_overwrite():
    os.environ[TEST_KEY] = "old_value"

    destination = secret_transfer.EnvDestination()
    destination[TEST_KEY] = TEST_VALUE

    assert os.environ.get(TEST_KEY) == TEST_VALUE


def test_clean():
    os.environ[TEST_KEY] = TEST_VALUE

    destination = secret_transfer.EnvDestination()
    del destination[TEST_KEY]

    assert os.environ.get(TEST_KEY) is None


def test_clean_not_existing():
    destination = secret_transfer.EnvDestination()
    del destination[TEST_KEY]

    assert os.environ.get(TEST_KEY) is None
