import pytest

import secret_transfer.utils.cli as cli_utils
import tests.utils as test_utils


def test_vault_kv_get(run_command_mock: test_utils.Mock):
    expected_result = "test_result"
    run_command_mock.return_value = expected_result

    assert (
        cli_utils.Vault.kv.get(
            address="test_address",
            mount="test_mount",
            field="test_field",
            value="test_value",
        )
        == expected_result
    )
    run_command_mock.assert_called_once_with(
        "vault kv get -address=test_address -mount=test_mount -field=test_field test_value"
    )


def test_vault_kv_get_key_not_found(run_command_mock: test_utils.Mock):
    run_command_mock.side_effect = cli_utils.RunError(
        exit_code=1,
        stdout="",
        stderr='Field "test_field" not present in secret',
        command="test command",
    )

    with pytest.raises(cli_utils.Vault.kv.KeyNotFoundError):
        cli_utils.Vault.kv.get(
            address="test_address",
            mount="test_mount",
            field="test_field",
            value="test_value",
        )

    run_command_mock.assert_called_once_with(
        "vault kv get -address=test_address -mount=test_mount -field=test_field test_value"
    )


def test_vault_kv_get_secret_not_found(run_command_mock: test_utils.Mock):
    run_command_mock.side_effect = cli_utils.RunError(
        exit_code=1,
        stdout="",
        stderr="No value found at test_mount/data/test_value",
        command="test command",
    )

    with pytest.raises(cli_utils.Vault.kv.SecretNotFoundError):
        cli_utils.Vault.kv.get(
            address="test_address",
            mount="test_mount",
            field="test_field",
            value="test_value",
        )

    run_command_mock.assert_called_once_with(
        "vault kv get -address=test_address -mount=test_mount -field=test_field test_value"
    )


def test_vault_kv_get_mount_not_found(run_command_mock: test_utils.Mock):
    run_command_mock.side_effect = cli_utils.RunError(
        exit_code=1,
        stdout="",
        stderr="Error reading test_mount/data/test_value: Error making API request.\nCode: 403\n",
        command="test command",
    )

    with pytest.raises(cli_utils.Vault.kv.MountForbiddenError):
        cli_utils.Vault.kv.get(
            address="test_address",
            mount="test_mount",
            field="test_field",
            value="test_value",
        )

    run_command_mock.assert_called_once_with(
        "vault kv get -address=test_address -mount=test_mount -field=test_field test_value"
    )


def test_vault_kv_get_unknown_error(run_command_mock: test_utils.Mock):
    error = cli_utils.RunError(
        exit_code=1,
        stdout="",
        stderr="Unknown error",
        command="test command",
    )
    run_command_mock.side_effect = error

    with pytest.raises(cli_utils.RunError) as exc_info:
        cli_utils.Vault.kv.get(
            address="test_address",
            mount="test_mount",
            field="test_field",
            value="test_value",
        )
    assert exc_info.value == error

    run_command_mock.assert_called_once_with(
        "vault kv get -address=test_address -mount=test_mount -field=test_field test_value"
    )
