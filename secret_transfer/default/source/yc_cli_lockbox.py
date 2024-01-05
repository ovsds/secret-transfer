import secret_transfer.core as core
import secret_transfer.utils.cli as cli_utils
import secret_transfer.utils.pydantic as pydantic_utils
import secret_transfer.utils.types as utils_types


class Arguments(pydantic_utils.BaseModel):
    profile: str
    folder: str
    lockbox: str


class YCCLILockboxSource(core.AbstractSource):
    _arguments_model = Arguments

    def __init__(self, *, profile: str, folder: str, lockbox: str):
        self._profile = profile
        self._folder = folder
        self._lockbox = lockbox

    def __getitem__(self, key: str) -> utils_types.LiteralArgumentType:
        """
        :raises KeyNotFoundError: if the key is not found
        """
        try:
            return cli_utils.YC.lockbox.payload.get(
                profile_name=self._profile,
                folder_name=self._folder,
                lockbox_name=self._lockbox,
                key=key,
            )
        except cli_utils.YC.lockbox.payload.KeyNotFoundError as exc:
            raise self.KeyNotFoundError(f"Key {key} is not found in {self.__class__.__name__}") from exc
