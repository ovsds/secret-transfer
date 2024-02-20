import tests.e2e.cli.common as common

ERROR_MESSAGE_PREFIX = """Usage: secret-transfer clean [OPTIONS]
Try 'secret-transfer clean --help' for help.

"""

HELP_MESSAGE = """Usage: secret-transfer clean [OPTIONS]

  Clean up the transfer's destinations.

Options:
  -f, --file_path TEXT  Path to the application settings file.  [required]
  -n, --name TEXT       Name of the transfer, if not specified, all transfers
                        will be cleaned.
  --help                Show this message and exit.
"""


def test_empty():
    result = common.run("secret-transfer clean")

    assert result.exit_code == 2
    assert result.stdout == ""
    assert result.stderr == f"{ERROR_MESSAGE_PREFIX}Error: Missing option '-f' / '--file_path'.\n"


def test_help():
    result = common.run("secret-transfer clean --help")

    assert result.exit_code == 0
    assert result.stdout == HELP_MESSAGE
    assert result.stderr == ""


def test_without_filename():
    result = common.run("secret-transfer clean -f")

    assert result.exit_code == 2
    assert result.stdout == ""
    assert result.stderr == "Error: Option '-f' requires an argument.\n"


def test_file_not_found():
    result = common.run("secret-transfer clean -f invalid_filename")

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == "Error: Could not open file 'invalid_filename': File not found\n"


def test_invalid_file_format(settings_file_context: common.SettingsFileContext):
    content = "test_key: - test_value"
    with settings_file_context(content=content) as filename:
        result = common.run(f"secret-transfer clean -f {filename}")

    assert result.exit_code == 2
    assert result.stdout == ""
    assert result.stderr == (
        f"{ERROR_MESSAGE_PREFIX}Error: Failed to load settings file from {filename}: \n"
        "Incorrect yaml format: \n"
        "sequence entries are not allowed here\n"
        '  in "<unicode string>", line 1, column 11:\n'
        "    test_key: - test_value\n"
        "              ^\n"
    )


def test_incorrect_schema(settings_file_context: common.SettingsFileContext):
    content = "sources: test_value"
    with settings_file_context(content=content) as filename:
        result = common.run(f"secret-transfer clean -f {filename}")

    assert result.exit_code == 2
    assert result.stdout == ""
    assert result.stderr == (
        f"{ERROR_MESSAGE_PREFIX}Error: Failed to validate settings schema for {filename}: \n"
        "sources: Input should be a valid dictionary\n"
    )


def test_extra_fields(settings_file_context: common.SettingsFileContext):
    content = "test_key: test_value"
    with settings_file_context(content=content) as filename:
        result = common.run(f"secret-transfer clean -f {filename}")

    assert result.exit_code == 2
    assert result.stdout == ""
    assert result.stderr == (
        f"{ERROR_MESSAGE_PREFIX}Error: Failed to validate settings schema for {filename}: \n"
        "test_key: Extra inputs are not permitted\n"
    )


def test_default(settings_file_context: common.SettingsFileContext):
    content = (
        "sources:\n"
        "  preset:\n"
        "    class_name: PresetSource\n"
        "    init_args:\n"
        "      test_key: test_value\n"
        "collections:\n"
        "  test_collection:\n"
        "    init_args:\n"
        "      test_key:\n"
        "        source: $sources[preset]\n"
        "transfers:\n"
        "  test_transfer:\n"
        "    init_args:\n"
        "      collection: $collections[test_collection]\n"
        "      destination: $destinations[bash_export]\n"
    )
    with settings_file_context(content=content) as filename:
        result = common.run(f"secret-transfer clean -f {filename}")

    assert result.exit_code == 0
    assert result.stdout == "unset test_key\n"
    assert result.stderr == ""


def test_with_name(settings_file_context: common.SettingsFileContext):
    content = (
        "sources:\n"
        "  preset:\n"
        "    class_name: PresetSource\n"
        "    init_args:\n"
        "      test_key: test_value\n"
        "      test_key2: test_value2\n"
        "  preset2:\n"
        "    class_name: PresetSource\n"
        "    init_args:\n"
        "      test_key: $sources[preset][test_key]\n"
        "collections:\n"
        "  test_collection:\n"
        "    init_args:\n"
        "      test_key:\n"
        "        source: $sources[preset2]\n"
        "transfers:\n"
        "  test_transfer:\n"
        "    init_args:\n"
        "      collection: $collections[test_collection]\n"
        "      destination: $destinations[bash_export]\n"
        "  test_transfer2:\n"
        "    init_args:\n"
        "      collection: $collections[test_collection2]\n"
        "      destination: $destinations[bash_export]\n"
    )
    with settings_file_context(content=content) as filename:
        result = common.run(f"secret-transfer clean -f {filename} -n test_transfer2")

    assert result.exit_code == 0
    assert result.stdout == "unset test_key2\n"
    assert result.stderr == ""
