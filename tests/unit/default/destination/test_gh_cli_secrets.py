import pytest
import pytest_mock

import secret_transfer
import secret_transfer.core as core
import tests.utils as test_utils

TEST_KEY = "test_key"
TEST_VALUE = "test_value"

TEST_ORGANIZATION_NAME = "test_organization_name"
TEST_REPO_NAME = "test_repo_name"
TEST_REPO_URL = f"https://github.com/{TEST_ORGANIZATION_NAME}/{TEST_REPO_NAME}"


@pytest.fixture(name="gh_mock")
def fixture_gh_mock(mocker: pytest_mock.MockFixture) -> test_utils.Mock:
    gh_mock = mocker.patch("secret_transfer.utils.cli.GH")

    class KeyNotFoundError(Exception):
        ...

    gh_mock.secret.KeyNotFoundError = KeyNotFoundError

    return gh_mock


def test_registered():
    key = secret_transfer.GithubCliSecretsDestination.__name__
    assert key in core.DestinationRegistry.classes
    assert core.DestinationRegistry.classes[key] is secret_transfer.GithubCliSecretsDestination


def test_parse_init_arguments():
    arguments = secret_transfer.GithubCliSecretsDestination.parse_init_arguments(
        owner_name=TEST_ORGANIZATION_NAME,
        repo_name=TEST_REPO_NAME,
    )

    assert arguments == {
        "owner_name": TEST_ORGANIZATION_NAME,
        "repo_name": TEST_REPO_NAME,
    }


def test_set(gh_mock: test_utils.Mock):
    destination = secret_transfer.GithubCliSecretsDestination(
        owner_name=TEST_ORGANIZATION_NAME,
        repo_name=TEST_REPO_NAME,
    )
    destination.set(key=TEST_KEY, value=TEST_VALUE)
    gh_mock.secret.set.assert_called_once_with(
        key=TEST_KEY,
        value=TEST_VALUE,
        repo_url=TEST_REPO_URL,
    )


def test_clean(gh_mock: test_utils.Mock):
    destination = secret_transfer.GithubCliSecretsDestination(
        owner_name=TEST_ORGANIZATION_NAME,
        repo_name=TEST_REPO_NAME,
    )
    destination.clean(key=TEST_KEY)
    gh_mock.secret.delete.assert_called_once_with(
        key=TEST_KEY,
        repo_url=TEST_REPO_URL,
    )


def test_clean_not_existing(gh_mock: test_utils.Mock):
    destination = secret_transfer.GithubCliSecretsDestination(
        owner_name=TEST_ORGANIZATION_NAME,
        repo_name=TEST_REPO_NAME,
    )
    gh_mock.secret.delete.side_effect = gh_mock.secret.KeyNotFoundError

    destination.clean(key=TEST_KEY)

    gh_mock.secret.delete.assert_called_once_with(
        key=TEST_KEY,
        repo_url=TEST_REPO_URL,
    )
