import dataclasses
import os

import pytest

import secret_transfer.utils.cli as cli_utils

DEFAULT_YC_KEY = "TEST_KEY"
DEFAULT_YC_VALUE = "TEST_VALUE"


@dataclasses.dataclass
class Config:
    profile_name: str
    folder_name: str
    lockbox_name: str
    key: str
    value: str


@pytest.fixture(name="config", scope="session")
def fixture_config():
    try:
        return Config(
            profile_name=os.environ["INTEGRATION_TESTS_YC_PROFILE_NAME"],
            folder_name=os.environ["INTEGRATION_TESTS_YC_FOLDER_NAME"],
            lockbox_name=os.environ["INTEGRATION_TESTS_YC_LOCKBOX_NAME"],
            key=os.environ.get("INTEGRATION_TESTS_YC_KEY", DEFAULT_YC_KEY),
            value=os.environ.get("INTEGRATION_TESTS_YC_VALUE", DEFAULT_YC_VALUE),
        )
    except KeyError as exc:
        pytest.xfail(f"missing environment variables {exc}")


def test_lockbox_payload_get(config: Config):
    result = cli_utils.YC.lockbox.payload.get(
        profile_name=config.profile_name,
        folder_name=config.folder_name,
        lockbox_name=config.lockbox_name,
        key=config.key,
    )

    assert result == config.value


def test_lockbox_payload_get_key_not_found(config: Config):
    with pytest.raises(cli_utils.YC.lockbox.payload.KeyNotFoundError):
        cli_utils.YC.lockbox.payload.get(
            profile_name=config.profile_name,
            folder_name=config.folder_name,
            lockbox_name=config.lockbox_name,
            key="not_found",
        )
