from .dot_env import DotEnvSource
from .env import EnvSource, register_env_source_instance
from .preset import PresetSource
from .user_input import UserInputSource, register_user_input_source_instance
from .vault_cli_kv import VaultCLIKVSource
from .yc_cli_lockbox import YCCLILockboxSource


def register_default_source_instances() -> None:
    register_env_source_instance()
    register_user_input_source_instance()


__all__ = [
    "DotEnvSource",
    "EnvSource",
    "PresetSource",
    "UserInputSource",
    "VaultCLIKVSource",
    "YCCLILockboxSource",
]
