import abc

import secret_transfer.core.base as core_base
import secret_transfer.protocol as protocol
import secret_transfer.utils.types as utils_types


class SourceRegistry(core_base.BaseRegistry[protocol.SourceProtocol]):
    ...


class AbstractSource(core_base.BaseResource, metaclass=SourceRegistry):
    __register__ = False

    BaseError = protocol.SourceProtocol.BaseError
    KeyNotFoundError = protocol.SourceProtocol.KeyNotFoundError

    def register(self, name: str) -> None:
        SourceRegistry.register_instance(name, self)

    @abc.abstractmethod
    def __getitem__(self, key: str) -> utils_types.LiteralArgumentType:
        ...
