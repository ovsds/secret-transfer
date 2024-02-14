import typing

import lazy_object_proxy  # pyright: ignore[reportMissingTypeStubs]

import secret_transfer.protocol as protocol
import secret_transfer.utils.types as utils_types

BaseRawArgumentType = utils_types.Literal


RawArgumentType = typing.Union[
    utils_types.Literal,
    typing.Mapping[str, "BaseRawArgumentType"],
    typing.Sequence["BaseRawArgumentType"],
]


class Proxy(lazy_object_proxy.Proxy):  # pyright: ignore[reportUntypedBaseClass]
    ...


BaseInitArgumentType = typing.Union[
    utils_types.Literal,
    protocol.BaseResourceProtocol,
]

InitArgumentType = typing.Union[
    BaseInitArgumentType,
    typing.Mapping[str, "InitArgumentType"],
    typing.Sequence["InitArgumentType"],
]
