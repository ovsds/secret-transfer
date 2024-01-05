import pytest
import pytest_mock

import secret_transfer
import secret_transfer.core as core
import tests.utils as test_utils

TEST_ADDRESS = "test_address"
TEST_MOUNT = "test_mount"
TEST_SECRET_NAME = "test_secret_name"
TEST_KEY = "test_key"

TEST_VALUE = "test_value"


@pytest.fixture(name="vault_mock")
def fixture_vault_mock(mocker: pytest_mock.MockFixture) -> test_utils.Mock:
    mock = mocker.patch("secret_transfer.utils.cli.Vault")

    class SecretNotFoundError(Exception):
        ...

    mock.kv.SecretNotFoundError = SecretNotFoundError

    class KeyNotFoundError(Exception):
        ...

    mock.kv.KeyNotFoundError = KeyNotFoundError

    class MountForbiddenError(Exception):
        ...

    mock.kv.MountForbiddenError = MountForbiddenError

    return mock


def test_registered():
    key = secret_transfer.VaultCLIKVSource.__name__
    assert key in core.SourceRegistry.classes
    assert core.SourceRegistry.classes[key] is secret_transfer.VaultCLIKVSource


def test_parse_init_arguments():
    arguments = secret_transfer.VaultCLIKVSource.parse_init_arguments(
        address=TEST_ADDRESS,
        mount=TEST_MOUNT,
        secret_name=TEST_SECRET_NAME,
    )

    assert arguments == {
        "address": TEST_ADDRESS,
        "mount": TEST_MOUNT,
        "secret_name": TEST_SECRET_NAME,
    }


def test_default(vault_mock: test_utils.Mock):
    vault_mock.kv.get.return_value = TEST_VALUE

    source = secret_transfer.VaultCLIKVSource(
        address=TEST_ADDRESS,
        mount=TEST_MOUNT,
        secret_name=TEST_SECRET_NAME,
    )

    assert source[TEST_KEY] == TEST_VALUE
    vault_mock.kv.get.assert_called_once_with(
        address=TEST_ADDRESS,
        mount=TEST_MOUNT,
        value=TEST_SECRET_NAME,
        field=TEST_KEY,
    )


def test_mount_forbidden(vault_mock: test_utils.Mock):
    vault_mock.kv.get.side_effect = vault_mock.kv.MountForbiddenError

    source = secret_transfer.VaultCLIKVSource(
        address=TEST_ADDRESS,
        mount=TEST_MOUNT,
        secret_name=TEST_SECRET_NAME,
    )

    with pytest.raises(source.KeyNotFoundError):
        source[TEST_KEY]

    vault_mock.kv.get.assert_called_once_with(
        address=TEST_ADDRESS,
        mount=TEST_MOUNT,
        value=TEST_SECRET_NAME,
        field=TEST_KEY,
    )


def test_key_not_found(vault_mock: test_utils.Mock):
    vault_mock.kv.get.side_effect = vault_mock.kv.KeyNotFoundError

    source = secret_transfer.VaultCLIKVSource(
        address=TEST_ADDRESS,
        mount=TEST_MOUNT,
        secret_name=TEST_SECRET_NAME,
    )

    with pytest.raises(source.KeyNotFoundError):
        source[TEST_KEY]

    vault_mock.kv.get.assert_called_once_with(
        address=TEST_ADDRESS,
        mount=TEST_MOUNT,
        value=TEST_SECRET_NAME,
        field=TEST_KEY,
    )


def test_secret_not_found(vault_mock: test_utils.Mock):
    vault_mock.kv.get.side_effect = vault_mock.kv.SecretNotFoundError

    source = secret_transfer.VaultCLIKVSource(
        address=TEST_ADDRESS,
        mount=TEST_MOUNT,
        secret_name=TEST_SECRET_NAME,
    )

    with pytest.raises(source.KeyNotFoundError):
        source[TEST_KEY]

    vault_mock.kv.get.assert_called_once_with(
        address=TEST_ADDRESS,
        mount=TEST_MOUNT,
        value=TEST_SECRET_NAME,
        field=TEST_KEY,
    )
