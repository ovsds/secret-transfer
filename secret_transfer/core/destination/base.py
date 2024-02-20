import abc
import typing

import secret_transfer.core.base as core_base
import secret_transfer.protocol as protocol
import secret_transfer.utils.types as utils_types


class DestinationRegistry(core_base.BaseRegistry[protocol.DestinationProtocol]):
    classes: dict[str, type[protocol.DestinationProtocol]]
    instances: dict[str, protocol.DestinationProtocol]
    default_class: typing.Optional[type[protocol.DestinationProtocol]]


class AbstractDestination(core_base.BaseResource, metaclass=DestinationRegistry):
    __register__ = False

    @abc.abstractmethod
    def __setitem__(self, key: str, value: utils_types.Literal) -> None: ...

    @abc.abstractmethod
    def __delitem__(self, key: str) -> None: ...
