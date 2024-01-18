import secret_transfer.core as core
import secret_transfer.utils.cli as cli_utils
import secret_transfer.utils.pydantic as pydantic_utils
import secret_transfer.utils.types as utils_types


class Arguments(pydantic_utils.BaseModel):
    address: str
    mount: str
    secret_name: str


class VaultCLIKVSource(core.AbstractSource):
    _arguments_model = Arguments

    def __init__(self, *, address: str, mount: str, secret_name: str):
        self._address = address
        self._mount = mount
        self._secret_name = secret_name

    def __getitem__(self, key: str) -> utils_types.LiteralArgumentType:
        """
        :raises KeyNotFoundError: if the key or secret is not found
        """
        try:
            return cli_utils.Vault.kv.get(
                address=self._address,
                mount=self._mount,
                value=self._secret_name,
                field=key,
            )
        except cli_utils.Vault.kv.MountForbiddenError as exc:
            raise self.KeyNotFoundError(f"Mount {self._mount} is forbidden in {self.__class__.__name__}") from exc
        except cli_utils.Vault.kv.KeyNotFoundError as exc:
            raise self.KeyNotFoundError(f"Key {key} is not found in {self.__class__.__name__}") from exc
        except cli_utils.Vault.kv.SecretNotFoundError as exc:
            raise self.KeyNotFoundError(f"Secret {key} is not found in {self.__class__.__name__}") from exc
