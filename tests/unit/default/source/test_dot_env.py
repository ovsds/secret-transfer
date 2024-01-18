import os
import typing
import uuid

import pytest

import secret_transfer
import secret_transfer.core as core

TEST_KEY = "test_key"
TEST_VALUE = "test_value"


def test_registered():
    key = secret_transfer.DotEnvSource.__name__
    assert key in core.SourceRegistry.classes
    assert core.SourceRegistry.classes[key] is secret_transfer.DotEnvSource


def test_parse_init_arguments():
    arguments = secret_transfer.DotEnvSource.parse_init_arguments(
        file_path="test_file_path",
    )

    assert arguments == {
        "file_path": "test_file_path",
    }


@pytest.fixture(name="dot_env_file")
def fixture_dot_env_file() -> typing.Generator[str, None, None]:
    file_path = f"{uuid.uuid4()}.env"
    file_path = os.path.abspath(file_path)

    with open(file=file_path, mode="x", encoding="utf-8") as file:
        file.write(f'{TEST_KEY}="{TEST_VALUE}"')

    try:
        yield file_path
    finally:
        os.remove(file_path)


def test_default(dot_env_file: str):
    source = secret_transfer.DotEnvSource(dot_env_file)

    assert source[TEST_KEY] == TEST_VALUE


def test_file_not_found():
    source = secret_transfer.DotEnvSource(os.path.abspath("not_found.env"))

    with pytest.raises(source.KeyNotFoundError):
        source[TEST_KEY]


def test_key_not_found(dot_env_file: str):
    source = secret_transfer.DotEnvSource(dot_env_file)

    with pytest.raises(source.KeyNotFoundError):
        source["not_found"]
