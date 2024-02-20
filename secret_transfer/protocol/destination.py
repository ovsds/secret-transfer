import typing

import secret_transfer.protocol.base as base
import secret_transfer.utils.types as utils_types


@typing.runtime_checkable
class DestinationProtocol(base.BaseResourceProtocol, typing.Protocol):
    def __setitem__(self, key: str, value: utils_types.Literal) -> None: ...

    def __delitem__(self, key: str) -> None: ...
