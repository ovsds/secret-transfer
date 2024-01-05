import secret_transfer.core as core
import secret_transfer.utils.cli as cli_utils
import secret_transfer.utils.pydantic as pydantic_utils
import secret_transfer.utils.types as utils_types

DEFAULT_BASE_URL = "https://github.com"


class Arguments(pydantic_utils.BaseModel):
    repo_name: str
    owner_name: str
    base_url: str = DEFAULT_BASE_URL


class GithubCliSecretsDestination(core.AbstractDestination):
    _arguments_model = Arguments

    def __init__(self, *, repo_name: str, owner_name: str, base_url: str = DEFAULT_BASE_URL):
        self._repo_name = repo_name
        self._owner_name = owner_name
        self._base_url = base_url

    @property
    def _repo_url(self) -> str:
        return f"{self._base_url}/{self._owner_name}/{self._repo_name}"

    def set(self, key: str, value: utils_types.BaseArgumentType) -> None:
        cli_utils.GH.secret.set(key=key, value=str(value), repo_url=self._repo_url)

    def clean(self, key: str) -> None:
        try:
            cli_utils.GH.secret.delete(key=key, repo_url=self._repo_url)
        except cli_utils.GH.secret.KeyNotFoundError:
            pass
