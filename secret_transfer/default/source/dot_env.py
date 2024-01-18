import dotenv

import secret_transfer.core as core
import secret_transfer.utils.file as file_utils
import secret_transfer.utils.pydantic as pydantic_utils
import secret_transfer.utils.types as utils_types


class Arguments(pydantic_utils.BaseModel):
    file_path: str


class DotEnvSource(core.AbstractSource):
    _arguments_model = Arguments

    def __init__(self, file_path: str):
        self._file_path = file_utils.get_absolute_file_path(file_path)

    def __getitem__(self, key: str) -> utils_types.LiteralArgumentType:
        """
        :raises KeyNotFoundError: if the key is not found
        """
        values = dotenv.dotenv_values(self._file_path)

        if key not in values or (value := values[key]) is None:
            raise self.KeyNotFoundError(f"Key {key} is not found in {self.__class__.__name__}")

        return value
