import os

import secret_transfer.core as core
import secret_transfer.utils.types as utils_types


class EnvSource(core.AbstractSource):
    def __getitem__(self, key: str) -> utils_types.LiteralArgumentType:
        """
        :raises KeyNotFoundError: if the key is not found
        """
        try:
            return os.environ[key]
        except KeyError as exc:
            raise self.KeyNotFoundError(f"Key {key} is not found in {self.__class__.__name__}") from exc

    @classmethod
    def get_default_instances(cls) -> dict[str, "EnvSource"]:
        return {"env": cls()}
