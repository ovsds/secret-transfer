import pytest

import secret_transfer.utils.cli as cli_utils
import tests.utils as test_utils


def test_repo_view(run_command_mock: test_utils.Mock):
    expected_result = "test_result"
    run_command_mock.return_value = expected_result

    assert cli_utils.GH.repo.view(json="test_json", template="test_template") == expected_result
    run_command_mock.assert_called_once_with("gh repo view --json test_json --template test_template")


def test_repo_get_name(run_command_mock: test_utils.Mock):
    expected_result = "test_repo_name"
    run_command_mock.return_value = expected_result

    assert cli_utils.GH.repo.get_name() == expected_result
    run_command_mock.assert_called_once_with("gh repo view --json name --template {{.name}}")


def test_repo_get_owner_name(run_command_mock: test_utils.Mock):
    expected_result = "test_owner_name"
    run_command_mock.return_value = expected_result

    assert cli_utils.GH.repo.get_owner_name() == expected_result
    run_command_mock.assert_called_once_with("gh repo view --json owner --template {{.owner.login}}")


def test_secret_set(run_command_mock: test_utils.Mock):
    cli_utils.GH.secret.set(key="test_key", value="test_value", repo_url="test_repo_url")
    run_command_mock.assert_called_once_with('gh secret set test_key --body "test_value" --repo test_repo_url')


def test_secret_delete(run_command_mock: test_utils.Mock):
    cli_utils.GH.secret.delete(key="test_key", repo_url="test_repo_url")
    run_command_mock.assert_called_once_with("gh secret delete test_key --repo test_repo_url")


def test_secret_delete_key_not_found(run_command_mock: test_utils.Mock):
    run_command_mock.side_effect = cli_utils.RunError(
        exit_code=1,
        stdout="",
        stderr="failed to delete secret test_key: HTTP 404",
        command="test command",
    )

    with pytest.raises(cli_utils.GH.secret.KeyNotFoundError):
        cli_utils.GH.secret.delete(key="test_key", repo_url="test_repo_url")

    run_command_mock.assert_called_once_with("gh secret delete test_key --repo test_repo_url")


def test_secret_delete_unknown_error(run_command_mock: test_utils.Mock):
    run_command_mock.side_effect = cli_utils.RunError(
        exit_code=1,
        stdout="",
        stderr="test error",
        command="test command",
    )

    with pytest.raises(cli_utils.RunError):
        cli_utils.GH.secret.delete(key="test_key", repo_url="test_repo_url")

    run_command_mock.assert_called_once_with("gh secret delete test_key --repo test_repo_url")
