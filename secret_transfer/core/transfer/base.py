import abc

import secret_transfer.core.base as core_base
import secret_transfer.protocol as protocol


class TransferRegistry(core_base.BaseRegistry[protocol.TransferProtocol]):
    ...


class AbstractTransfer(core_base.BaseResource, metaclass=TransferRegistry):
    __register__ = False

    BaseError = protocol.TransferProtocol.BaseError
    CollectionNotFoundError = protocol.TransferProtocol.CollectionNotFoundError
    DestinationNotFoundError = protocol.TransferProtocol.DestinationNotFoundError
    CollectionError = protocol.TransferProtocol.CollectionError

    def register(self, name: str) -> None:
        TransferRegistry.register_instance(name, self)

    @abc.abstractmethod
    def run(self) -> None:
        ...

    @abc.abstractmethod
    def clean(self) -> None:
        ...
