import abc

import secret_transfer.core.base as core_base
import secret_transfer.protocol as protocol
import secret_transfer.utils.types as utils_types


class DestinationRegistry(core_base.BaseRegistry[protocol.DestinationProtocol]):
    ...


class AbstractDestination(core_base.BaseResource, metaclass=DestinationRegistry):
    __register__ = False

    def register(self, name: str) -> None:
        DestinationRegistry.register_instance(name, self)

    @abc.abstractmethod
    def set(self, key: str, value: utils_types.BaseArgumentType) -> None:
        ...

    @abc.abstractmethod
    def clean(self, key: str) -> None:
        ...
