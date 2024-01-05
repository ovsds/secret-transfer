import pytest

import secret_transfer.utils.cli as cli_utils
import tests.utils as test_utils


def test_lockbox_payload_get(run_command_mock: test_utils.Mock):
    expected_result = "test_result"
    run_command_mock.return_value = expected_result

    assert (
        cli_utils.YC.lockbox.payload.get(
            profile_name="test_profile_name",
            folder_name="test_folder_name",
            lockbox_name="test_lockbox_name",
            key="test_key",
        )
        == expected_result
    )
    run_command_mock.assert_called_once_with(
        "yc lockbox payload get"
        " --profile test_profile_name"
        " --folder-name test_folder_name"
        " --name test_lockbox_name"
        " --key test_key"
    )


def test_lockbox_payload_get_not_found(run_command_mock: test_utils.Mock):
    run_command_mock.side_effect = cli_utils.RunError(
        exit_code=1,
        stdout="",
        stderr="ERROR: payload entry with key 'test_key' not found",
        command="test command",
    )

    with pytest.raises(cli_utils.YC.lockbox.payload.KeyNotFoundError):
        cli_utils.YC.lockbox.payload.get(
            profile_name="test_profile_name",
            folder_name="test_folder_name",
            lockbox_name="test_lockbox_name",
            key="test_key",
        )

    run_command_mock.assert_called_once_with(
        "yc lockbox payload get"
        " --profile test_profile_name"
        " --folder-name test_folder_name"
        " --name test_lockbox_name"
        " --key test_key"
    )


def test_lockbox_payload_get_unknown_error(run_command_mock: test_utils.Mock):
    error = cli_utils.RunError(
        exit_code=1,
        stdout="",
        stderr="ERROR: unknown error",
        command="test command",
    )
    run_command_mock.side_effect = error

    with pytest.raises(cli_utils.RunError) as exc_info:
        cli_utils.YC.lockbox.payload.get(
            profile_name="test_profile_name",
            folder_name="test_folder_name",
            lockbox_name="test_lockbox_name",
            key="test_key",
        )

    assert exc_info.value == error
    run_command_mock.assert_called_once_with(
        "yc lockbox payload get"
        " --profile test_profile_name"
        " --folder-name test_folder_name"
        " --name test_lockbox_name"
        " --key test_key"
    )
