import os

import secret_transfer.core as core
import secret_transfer.utils.types as utils_types


class EnvDestination(core.AbstractDestination):
    def set(self, key: str, value: utils_types.BaseArgumentType) -> None:
        os.environ[key] = str(value)

    def clean(self, key: str) -> None:
        try:
            del os.environ[key]
        except KeyError:
            pass


def register_env_destination_instance():
    EnvDestination().register("env")
