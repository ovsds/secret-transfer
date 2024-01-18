import os
import typing
import warnings

import pytest
import pytest_mock

import secret_transfer.utils.file as file_utils

RootPathContext = typing.Callable[[str], typing.ContextManager[str]]


@pytest.fixture(name="clean_up_root_path_context")
def fixture_clean_up_root_path_context() -> typing.Generator[None, None, None]:
    token = file_utils.path._root_path_context.set(None)  # type: ignore[reportPrivateUsage, reportGeneralTypeIssues]
    try:
        yield
    finally:
        file_utils.path._root_path_context.reset(token)  # type: ignore[reportPrivateUsage]


def test_absolute_path(clean_up_root_path_context: None):
    assert file_utils.get_absolute_file_path("/test") == "/test"


def test_set_root_path(clean_up_root_path_context: None):
    file_utils.set_root_path("/test_root_path")
    assert file_utils.get_root_path() == "/test_root_path"


def test_relative_path_with_context(clean_up_root_path_context: None):
    with file_utils.context_root_path("/test_root_path"):
        assert file_utils.get_absolute_file_path("test") == os.path.join("/test_root_path", "test")


def test_relative_path_without_context(clean_up_root_path_context: None, mocker: pytest_mock.MockFixture):
    mocker.patch.object(os, "getcwd", return_value="/test_root_path")

    with warnings.catch_warnings(record=True) as warning_records:  # ignore warning about missing context
        assert file_utils.get_absolute_file_path("test") == os.path.join("/test_root_path", "test")

    assert len(warning_records) == 1
    assert issubclass(warning_records[0].category, RuntimeWarning)
