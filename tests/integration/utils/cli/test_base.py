import pytest

import secret_transfer.utils.cli as cli_utils


def test_run_utils_default():
    assert cli_utils.run("echo test") == "test\n"


def test_run_utils_exit():
    command = "echo test; >&2 echo test error; exit 42"

    with pytest.raises(cli_utils.RunError) as exc:
        cli_utils.run(command)

    assert exc.value.exit_code == 42
    assert exc.value.stdout == "test\n"
    assert exc.value.stderr == "test error\n"
    assert exc.value.command == command
