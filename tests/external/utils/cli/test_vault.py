import dataclasses
import os

import pytest

import secret_transfer.utils.cli as cli_utils

DEFAULT_VAULT_SECRET = "TEST_SECRET"
DEFAULT_VAULT_KEY = "TEST_KEY"
DEFAULT_VAULT_VALUE = "TEST_VALUE"


@dataclasses.dataclass
class Config:
    address: str
    mount: str
    secret: str
    key: str
    value: str


@pytest.fixture(name="config", scope="session")
def fixture_config():
    try:
        return Config(
            address=os.environ["INTEGRATION_TESTS_VAULT_ADDRESS"],
            mount=os.environ["INTEGRATION_TESTS_VAULT_MOUNT"],
            secret=os.environ.get("INTEGRATION_TESTS_VAULT_SECRET", DEFAULT_VAULT_SECRET),
            key=os.environ.get("INTEGRATION_TESTS_VAULT_KEY", DEFAULT_VAULT_KEY),
            value=os.environ.get("INTEGRATION_TESTS_VAULT_VALUE", DEFAULT_VAULT_VALUE),
        )
    except KeyError as exc:
        pytest.xfail(f"missing environment variables {exc}")


def test_vault_kv_get(config: Config):
    result = cli_utils.Vault.kv.get(
        address=config.address,
        mount=config.mount,
        value=config.secret,
        field=config.key,
    )

    assert result == config.value


def test_vault_kv_get_mount_not_found(config: Config):
    with pytest.raises(cli_utils.Vault.kv.MountForbiddenError):
        cli_utils.Vault.kv.get(
            address=config.address,
            mount="not_found",
            value=config.secret,
            field=config.key,
        )


def test_vault_kv_get_secret_not_found(config: Config):
    with pytest.raises(cli_utils.Vault.kv.SecretNotFoundError):
        cli_utils.Vault.kv.get(
            address=config.address,
            mount=config.mount,
            value="not_found",
            field=config.key,
        )


def test_vault_kv_get_key_not_found(config: Config):
    with pytest.raises(cli_utils.Vault.kv.KeyNotFoundError):
        cli_utils.Vault.kv.get(
            address=config.address,
            mount=config.mount,
            value=config.secret,
            field="not_found",
        )
