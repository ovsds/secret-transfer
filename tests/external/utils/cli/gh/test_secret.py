import pytest

import secret_transfer.utils.cli as cli_utils

REPO_NAME = "secret-transfer"
REPO_OWNER_NAME = "ovsds"
REPO_URL = f"{REPO_OWNER_NAME}/{REPO_NAME}"

TEST_KEY = "test_key"
TEST_VALUE = "test_value"


@pytest.fixture(name="clean_up_test_key", autouse=True)
def fixture_clean_up_test_key():
    try:
        yield
    finally:
        try:
            cli_utils.GH.secret.delete(key=TEST_KEY, repo_url=REPO_URL)
        except cli_utils.GH.secret.KeyNotFoundError:
            pass


def test_gh_secret_set_and_delete():
    repo_url = f"{REPO_OWNER_NAME}/{REPO_NAME}"

    cli_utils.GH.secret.set(key=TEST_KEY, value=TEST_VALUE, repo_url=repo_url)
    cli_utils.GH.secret.delete(key=TEST_KEY, repo_url=repo_url)


def test_gh_secret_set_existing_overwrites():
    repo_url = f"{REPO_OWNER_NAME}/{REPO_NAME}"

    cli_utils.GH.secret.set(key=TEST_KEY, value=TEST_VALUE, repo_url=repo_url)
    cli_utils.GH.secret.set(key=TEST_KEY, value=TEST_VALUE, repo_url=repo_url)


def test_gh_secret_delete_non_existing_raises():
    repo_url = f"{REPO_OWNER_NAME}/{REPO_NAME}"

    with pytest.raises(cli_utils.GH.secret.KeyNotFoundError):
        cli_utils.GH.secret.delete(key=TEST_KEY, repo_url=repo_url)
