import typing

LiteralArgumentType = typing.Union[
    str,
    int,
    float,
    bool,
]

BaseArgumentType = typing.Union[
    LiteralArgumentType,
    dict[str, "BaseArgumentType"],
    list["BaseArgumentType"],
]
