import contextlib
import os
import typing
import uuid

import pytest

import tests.e2e.cli.common as common


@pytest.fixture(name="settings_file_context")
def fixture_settings_file_context() -> common.SettingsFileContext:
    @contextlib.contextmanager
    def inner(content: str) -> typing.Generator[str, None, None]:
        filename = str(uuid.uuid4())

        with open(filename, "w") as file:
            file.write(content)

        try:
            yield filename
        finally:
            os.remove(filename)

    return inner
