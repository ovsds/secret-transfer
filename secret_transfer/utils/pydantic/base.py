import dataclasses

import pydantic
import typing_extensions
import yaml
import yaml.scanner as yaml_scanner


@dataclasses.dataclass
class PydanticYamlLoadError(Exception):
    message: str


class BaseModel(pydantic.BaseModel):
    @classmethod
    def from_yaml(cls, raw: str) -> typing_extensions.Self:
        try:
            data = yaml.safe_load(raw)
        except yaml_scanner.ScannerError as exc:
            raise PydanticYamlLoadError(message=f"Incorrect yaml format: \n{exc}") from exc

        if data is None:
            return cls()

        return cls.model_validate(data)

    model_config = pydantic.ConfigDict(extra="forbid")


def format_validation_error(exception: pydantic.ValidationError) -> str:
    result: list[str] = []
    for error in exception.errors():
        locations: list[str] = []
        for loc in error["loc"]:
            if isinstance(loc, int):
                locations[-1] = f"{locations[-1]}[{loc}]"
            else:
                locations.append(loc)
        result.append(f"{'.'.join(locations)}: {error['msg']}")

    return "\n".join(result)
