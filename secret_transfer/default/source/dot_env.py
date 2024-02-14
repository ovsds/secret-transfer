import dotenv

import secret_transfer.core as core
import secret_transfer.utils.file as file_utils
import secret_transfer.utils.types as utils_types


class DotEnvSource(core.AbstractSource):
    def __init__(self, file_path: str):
        self._file_path = file_utils.get_absolute_file_path(file_path)

    def __getitem__(self, key: str) -> utils_types.Literal:
        """
        :raises KeyNotFoundError: if the key is not found
        """
        values = dotenv.dotenv_values(self._file_path)

        if key not in values or (value := values[key]) is None:
            raise self.KeyNotFoundError(f"Key {key} is not found in {self.__class__.__name__}")

        return value
