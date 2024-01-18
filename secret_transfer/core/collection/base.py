import abc
import typing

import secret_transfer.core.base as core_base
import secret_transfer.protocol as protocol
import secret_transfer.utils.types as utils_types


class CollectionRegistry(core_base.BaseRegistry[protocol.CollectionProtocol]):
    ...


class AbstractCollection(core_base.BaseResource, metaclass=CollectionRegistry):
    __register__ = False

    BaseError = protocol.CollectionProtocol.BaseError
    KeyNotFoundError = protocol.CollectionProtocol.KeyNotFoundError

    def register(self, name: str) -> None:
        CollectionRegistry.register_instance(name, self)

    @abc.abstractmethod
    def __getitem__(self, key: str) -> utils_types.LiteralArgumentType:
        ...

    @abc.abstractmethod
    def __iter__(self) -> typing.Iterator[str]:
        ...

    @abc.abstractmethod
    def items(self) -> typing.Iterator[tuple[str, utils_types.LiteralArgumentType]]:
        ...
