from .bash_export import (
    BashExportDestination,
    register_bash_nexport_destinatio_instance,
)
from .env import EnvDestination, register_env_destination_instance
from .gh_cli_secrets import GithubCliSecretsDestination


def register_default_destination_instances() -> None:
    register_env_destination_instance()
    register_bash_nexport_destinatio_instance()


__all__ = [
    "BashExportDestination",
    "EnvDestination",
    "GithubCliSecretsDestination",
    "register_default_destination_instances",
]
