import pytest
import pytest_mock

import secret_transfer
import secret_transfer.core as core
import tests.utils as test_utils

TEST_KEY = "test_key"
TEST_VALUE = "test_value"

TEST_PROFILE = "test_profile"
TEST_FOLDER = "test_folder"
TEST_LOCKBOX = "test_lockbox"


@pytest.fixture(name="yc_mock")
def fixture_yc_mock(mocker: pytest_mock.MockFixture) -> test_utils.Mock:
    yc_mock = mocker.patch("secret_transfer.utils.cli.YC")

    class KeyNotFoundError(Exception):
        ...

    yc_mock.lockbox.payload.KeyNotFoundError = KeyNotFoundError

    return yc_mock


def test_registered():
    key = secret_transfer.YCCLILockboxSource.__name__
    assert key in core.SourceRegistry.classes
    assert core.SourceRegistry.classes[key] is secret_transfer.YCCLILockboxSource


def test_parse_init_arguments():
    arguments = secret_transfer.YCCLILockboxSource.parse_init_arguments(
        profile=TEST_PROFILE,
        folder=TEST_FOLDER,
        lockbox=TEST_LOCKBOX,
    )

    assert arguments == {
        "profile": TEST_PROFILE,
        "folder": TEST_FOLDER,
        "lockbox": TEST_LOCKBOX,
    }


def test_default(yc_mock: test_utils.Mock):
    yc_mock.lockbox.payload.get.return_value = TEST_VALUE

    source = secret_transfer.YCCLILockboxSource(
        profile=TEST_PROFILE,
        folder=TEST_FOLDER,
        lockbox=TEST_LOCKBOX,
    )

    assert source[TEST_KEY] == TEST_VALUE
    yc_mock.lockbox.payload.get.assert_called_once_with(
        profile_name=TEST_PROFILE,
        folder_name=TEST_FOLDER,
        lockbox_name=TEST_LOCKBOX,
        key=TEST_KEY,
    )


def test_not_found(yc_mock: test_utils.Mock):
    yc_mock.lockbox.payload.get.side_effect = yc_mock.lockbox.payload.KeyNotFoundError

    source = secret_transfer.YCCLILockboxSource(
        profile=TEST_PROFILE,
        folder=TEST_FOLDER,
        lockbox=TEST_LOCKBOX,
    )

    with pytest.raises(source.KeyNotFoundError):
        source[TEST_KEY]

    yc_mock.lockbox.payload.get.assert_called_once_with(
        profile_name=TEST_PROFILE,
        folder_name=TEST_FOLDER,
        lockbox_name=TEST_LOCKBOX,
        key=TEST_KEY,
    )
