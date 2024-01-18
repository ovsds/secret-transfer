import tests.e2e.cli.common as common

HELP_MESSAGE = """Usage: secret-transfer [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  clean  Clean up the transfer's destinations.
  run    Run transfers.
"""


def test_empty():
    result = common.run("secret-transfer")

    assert result.exit_code == 0
    assert result.stdout == HELP_MESSAGE
    assert result.stderr == ""


def test_help():
    result = common.run("secret-transfer --help")

    assert result.exit_code == 0
    assert result.stdout == HELP_MESSAGE
    assert result.stderr == ""
