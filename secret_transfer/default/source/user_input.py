import getpass

import typing_extensions

import secret_transfer.core as core
import secret_transfer.utils.types as utils_types


class UserInputSource(core.AbstractSource):
    def __getitem__(self, key: str) -> utils_types.Literal:
        return getpass.getpass(prompt=f"Please provide a value for {key}: ")

    @classmethod
    def get_default_instances(cls) -> dict[str, typing_extensions.Self]:
        return {"user_input": cls()}
