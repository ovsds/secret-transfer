import typing

import typing_extensions

import secret_transfer.core as core
import secret_transfer.utils.types as utils_types


class BashExportDestination(core.AbstractDestination):
    def __setitem__(self, key: str, value: utils_types.Literal) -> None:
        print(f"export {key}={value}")

    def __delitem__(self, key: str) -> None:
        print(f"unset {key}")

    @classmethod
    def get_default_instances(cls) -> typing.Mapping[str, typing_extensions.Self]:
        return {"bash_export": cls()}
