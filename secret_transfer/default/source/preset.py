import secret_transfer.core as core
import secret_transfer.utils.types as utils_types


class PresetSource(core.AbstractSource):
    def __init__(self, **kwargs: str):
        self._data = kwargs

    def __getitem__(self, key: str) -> utils_types.LiteralArgumentType:
        """
        :raises KeyNotFoundError: if the key is not found
        """
        try:
            return self._data[key]
        except KeyError as exc:
            raise self.KeyNotFoundError(f"Key {key} is not found in {self.__class__.__name__}") from exc
