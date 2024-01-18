import typing

import secret_transfer.protocol.base as base
import secret_transfer.utils.types as utils_types


@typing.runtime_checkable
class SourceProtocol(base.BaseResourceProtocol, typing.Protocol):
    class BaseError(Exception):
        ...

    class KeyNotFoundError(BaseError):
        ...

    def __getitem__(self, key: str) -> utils_types.LiteralArgumentType:
        """
        :raises KeyNotFoundError: if the key is not found
        """
        ...
