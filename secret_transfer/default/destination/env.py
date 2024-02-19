import os

import typing_extensions

import secret_transfer.core as core
import secret_transfer.utils.types as utils_types


class EnvDestination(core.AbstractDestination):
    def set(self, key: str, value: utils_types.Literal) -> None:
        os.environ[key] = str(value)

    def clean(self, key: str) -> None:
        try:
            del os.environ[key]
        except KeyError:
            pass

    @classmethod
    def get_default_instances(cls) -> dict[str, typing_extensions.Self]:
        return {"env": cls()}
