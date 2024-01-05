import secret_transfer.utils.cli as cli_utils

REPO_NAME = "secret-transfer"
REPO_OWNER_NAME = "ovsds"
REPO_URL = f"{REPO_OWNER_NAME}/{REPO_NAME}"


def test_gh_repo_view():
    result = cli_utils.GH.repo.view(json="name", template="{{.name}}")
    assert result == REPO_NAME


def test_gh_repo_get_name():
    result = cli_utils.GH.repo.get_name()
    assert result == REPO_NAME


def test_gh_repo_get_owner_name():
    result = cli_utils.GH.repo.get_owner_name()
    assert result == REPO_OWNER_NAME
