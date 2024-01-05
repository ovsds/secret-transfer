import typing

import secret_transfer.protocol.base as base


@typing.runtime_checkable
class TransferProtocol(base.BaseResourceProtocol, typing.Protocol):
    class BaseError(Exception):
        ...

    class CollectionNotFoundError(BaseError):
        ...

    class DestinationNotFoundError(BaseError):
        ...

    class CollectionError(BaseError):
        ...

    def run(self) -> None:
        """
        :raises CollectionNotFoundError: if the collection is not found
        :raises DestinationNotFoundError: if the destination is not found
        :raises CollectionError: if the collection failed
        """
        ...

    def clean(self) -> None:
        """
        :raises CollectionNotFoundError: if the collection is not found
        :raises DestinationNotFoundError: if the destination is not found
        """
        ...
