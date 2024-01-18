import pytest_mock

import secret_transfer
import secret_transfer.core as core

TEST_KEY = "test_key"
TEST_VALUE = "test_value"


def test_registered():
    key = secret_transfer.BashExportDestination.__name__
    assert key in core.DestinationRegistry.classes
    assert core.DestinationRegistry.classes[key] is secret_transfer.BashExportDestination
    assert "bash_export" in core.DestinationRegistry.instances
    assert isinstance(core.DestinationRegistry.instances["bash_export"], secret_transfer.BashExportDestination)


def test_set(mocker: pytest_mock.MockFixture):
    mocked_print = mocker.patch("builtins.print")

    destination = secret_transfer.BashExportDestination()
    destination.set(TEST_KEY, TEST_VALUE)

    mocked_print.assert_called_once_with(f"export {TEST_KEY}={TEST_VALUE}")


def test_clean(mocker: pytest_mock.MockFixture):
    mocked_print = mocker.patch("builtins.print")

    destination = secret_transfer.BashExportDestination()
    destination.clean(TEST_KEY)

    mocked_print.assert_called_once_with(f"unset {TEST_KEY}")
