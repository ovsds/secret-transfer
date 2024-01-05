import typing

import secret_transfer.utils.pydantic as pydantic_utils
import secret_transfer.utils.types as utils_types


class BaseResource:
    _arguments_model: typing.Optional[type[pydantic_utils.BaseModel]] = None

    @classmethod
    def parse_init_arguments(cls, **arguments: utils_types.BaseArgumentType) -> typing.Mapping[str, typing.Any]:
        if cls._arguments_model is None:
            return arguments

        model = cls._arguments_model.model_validate(arguments)
        return model.shallow_model_dump()
