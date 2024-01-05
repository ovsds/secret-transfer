from .collection import DefaultCollection, DefaultCollectionItem
from .destination import (
    BashExportDestination,
    EnvDestination,
    GithubCliSecretsDestination,
    register_default_destination_instances,
)
from .source import (
    DotEnvSource,
    EnvSource,
    PresetSource,
    UserInputSource,
    VaultCLIKVSource,
    YCCLILockboxSource,
    register_default_source_instances,
)
from .transfer import DefaultTransfer


def register_default_instances() -> None:
    register_default_source_instances()
    register_default_destination_instances()


register_default_instances()


__all__ = [
    "BashExportDestination",
    "DefaultCollection",
    "DefaultCollectionItem",
    "DefaultTransfer",
    "DotEnvSource",
    "EnvDestination",
    "EnvSource",
    "GithubCliSecretsDestination",
    "PresetSource",
    "UserInputSource",
    "VaultCLIKVSource",
    "YCCLILockboxSource",
]
