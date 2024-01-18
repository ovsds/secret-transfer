import pytest

import secret_transfer
import secret_transfer.core as core

TEST_KEY = "test_key"
TEST_VALUE = "test_value"


def test_registered():
    key = secret_transfer.PresetSource.__name__
    assert key in core.SourceRegistry.classes
    assert core.SourceRegistry.classes[key] is secret_transfer.PresetSource


def test_parse_init_arguments():
    arguments = secret_transfer.PresetSource.parse_init_arguments(
        **{
            TEST_KEY: TEST_VALUE,
        }
    )

    assert arguments == {
        TEST_KEY: TEST_VALUE,
    }


def test_default():
    source = secret_transfer.PresetSource(**{TEST_KEY: TEST_VALUE})

    assert source[TEST_KEY] == TEST_VALUE


def test_not_found():
    source = secret_transfer.PresetSource()

    with pytest.raises(source.KeyNotFoundError):
        source[TEST_KEY]
