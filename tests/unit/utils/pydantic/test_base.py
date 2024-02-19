import typing

import pydantic
import pytest

import secret_transfer.utils.pydantic as pydantic_utils


def test_pydantic_from_yaml():
    class Model(pydantic_utils.BaseModel):
        test_key: str

    model = Model.from_yaml(raw="test_key: test_value")

    assert model.test_key == "test_value"


def test_pydantic_from_yaml_invalid_format():
    class Model(pydantic_utils.BaseModel):
        test_key: str

    with pytest.raises(pydantic_utils.PydanticYamlLoadError):
        Model.from_yaml(raw="test_key: - test_value")


def test_pydantic_from_yaml_empty():
    class Model(pydantic_utils.BaseModel):
        test_key: typing.Optional[str] = None

    model = Model.from_yaml(raw="")

    assert model.test_key is None


def test_pydantic_validation_error():
    class Model(pydantic_utils.BaseModel):
        test_key: str

    with pytest.raises(pydantic.ValidationError):
        Model.from_yaml(raw="")


def test_format_model_validation_error():
    class Model(pydantic_utils.BaseModel):
        test_key: str

    with pytest.raises(pydantic.ValidationError) as exc:
        Model.model_validate(obj={})

    assert pydantic_utils.format_validation_error(exc.value) == "test_key: Field required"


def test_format_model_validation_error_nested():
    class InnerModel(pydantic_utils.BaseModel):
        test_key: str

    class Model(pydantic_utils.BaseModel):
        inner_model: InnerModel

    with pytest.raises(pydantic.ValidationError) as exc:
        Model.model_validate(obj={"inner_model": {}})

    assert pydantic_utils.format_validation_error(exc.value) == "inner_model.test_key: Field required"


def test_format_model_validation_error_nested_list():
    class InnerModel(pydantic_utils.BaseModel):
        test_key: str

    class Model(pydantic_utils.BaseModel):
        inner_model: list[InnerModel]

    with pytest.raises(pydantic.ValidationError) as exc:
        Model.model_validate(obj={"inner_model": [{}]})

    assert pydantic_utils.format_validation_error(exc.value) == "inner_model[0].test_key: Field required"


def test_format_model_validation_error_multiple():
    class Model(pydantic_utils.BaseModel):
        test_key: str
        test_key2: str

    with pytest.raises(pydantic.ValidationError) as exc:
        Model.model_validate(obj={})

    assert pydantic_utils.format_validation_error(exc.value) == (
        "test_key: Field required\n" "test_key2: Field required"
    )
