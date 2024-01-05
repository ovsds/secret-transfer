import typing

import secret_transfer.protocol.base as base
import secret_transfer.utils.types as utils_types


@typing.runtime_checkable
class DestinationProtocol(base.BaseResourceProtocol, typing.Protocol):
    def set(self, key: str, value: utils_types.BaseArgumentType) -> None:
        ...

    def clean(self, key: str) -> None:
        ...
