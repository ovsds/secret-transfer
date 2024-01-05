import typing

import secret_transfer.protocol.base as base
import secret_transfer.utils.types as utils_types


@typing.runtime_checkable
class CollectionProtocol(base.BaseResourceProtocol, typing.Protocol):
    class BaseError(Exception):
        ...

    class KeyNotFoundError(BaseError):
        ...

    def __getitem__(self, key: str) -> utils_types.LiteralArgumentType:
        """
        :raises KeyNotFoundError: if the key is not found
        :raises SourceNotFoundError: if the source is not found
        :raises KeyNotFoundInSourceError: if the key is not found in the source
        """
        ...

    def __iter__(self) -> typing.Iterator[str]:
        ...

    def items(self) -> typing.Iterator[tuple[str, utils_types.LiteralArgumentType]]:
        """
        :raises SourceNotFoundError: if the source is not found
        :raises KeyNotFoundInSourceError: if the key is not found in the source
        """
        ...
