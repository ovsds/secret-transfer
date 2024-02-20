import typing

import pytest
import pytest_mock

import secret_transfer.core.base as core_base
import secret_transfer.core.types as core_types
import secret_transfer.protocol as protocol
import tests.unit.core.base.proxy.resource.suite as test_suite


@typing.runtime_checkable
class ResourceProtocol(protocol.BaseResourceProtocol, typing.Protocol):
    def test_method(self) -> None: ...


class Resource(core_base.BaseResource):
    def test_method(self) -> None:
        pass  # pragma: no cover


ResourceSettings = core_base.ResourceSettings[ResourceProtocol]


class ResourceProxy(core_base.BaseResourceProxy[ResourceProtocol]): ...


class TestResourceProxy(test_suite.ResourceProxySuite[ResourceProtocol]):
    @pytest.fixture(name="target_proxy")
    def fixture_target_proxy(self) -> type[core_base.BaseResourceProxy[ResourceProtocol]]:
        return ResourceProxy

    @pytest.fixture(name="target_settings")
    def fixture_target_settings(self) -> type[core_base.ResourceSettings[ResourceProtocol]]:
        return ResourceSettings

    @pytest.fixture(name="classes")
    def fixture_classes(self) -> typing.Mapping[str, type[ResourceProtocol]]:
        return {"Resource": Resource}

    @pytest.fixture(name="default_class")
    def fixture_default_class(self) -> type[ResourceProtocol]:
        return Resource

    @pytest.fixture(name="class_name")
    def fixture_class_name(self) -> str:
        return "Resource"


@pytest.mark.parametrize(
    "argument",
    [
        {"test": "test"},
        ["test", "test", "test"],
        "test",
        1,
        1.0,
        True,
        None,
        {"test": {"test": {"test": "test"}}},
        ["test", ["test", ["test", "test"]]],
        {"dict": {"test": "test"}, "list": ["test", "test"], "str": "test", "int": 1, "float": 1.0, "bool": True},
    ],
    ids=[
        "dict",
        "list",
        "str",
        "int",
        "float",
        "bool",
        "none",
        "nested dict",
        "nested list",
        "nested everything",
    ],
)
def test_proxy_arguments(mocker: pytest_mock.MockFixture, argument: typing.Any):
    test_class = mocker.Mock(spec=protocol.BaseResourceProtocol)

    raw_arguments = {"raw": argument}
    parsed_arguments = {"parsed": "parsed"}
    test_class.parse_init_arguments.return_value = parsed_arguments

    proxy = ResourceProxy.from_settings(
        settings=ResourceSettings(
            resource_classes={"Resource": test_class},
            class_name="Resource",
            raw_arguments=raw_arguments,
        ),
    )

    proxy.test_method()
    test_class.parse_init_arguments.assert_called_once_with(**raw_arguments)
    test_class.assert_called_once_with(**parsed_arguments)


def test_proxy_resource_argument(mocker: pytest_mock.MockFixture):
    test_class = mocker.Mock(spec=protocol.BaseResourceProtocol)

    raw_arguments = {"raw": "$sources[source][key]"}
    source = mocker.MagicMock(spec=protocol.SourceProtocol)
    source.__getitem__.return_value = "source_value"

    parsed_arguments = {"parsed": "parsed"}
    test_class.parse_init_arguments.return_value = parsed_arguments

    proxy = ResourceProxy.from_settings(
        settings=ResourceSettings(
            resource_classes={"Resource": test_class},
            class_name="Resource",
            resources={"sources": {"source": source}},
            raw_arguments=raw_arguments,
        ),
    )

    source.__getitem__.assert_not_called()

    proxy.test_method()
    test_class.parse_init_arguments.assert_called_once_with(**{"raw": "source_value"})
    test_class.assert_called_once_with(**parsed_arguments)


def test_proxy_resource_argument_proxy(mocker: pytest_mock.MockFixture):
    test_class = mocker.Mock(spec=protocol.BaseResourceProtocol)

    raw_arguments = {"raw": "$sources[source][key]"}

    class Source(core_base.BaseResource):
        _could_be_called = False

        def __getitem__(self, item: str) -> str:
            assert self._could_be_called, "Should not be called yet"
            return "source_value"

    source = core_types.Proxy(Source)

    parsed_arguments = {"parsed": "parsed"}
    test_class.parse_init_arguments.return_value = parsed_arguments

    proxy = ResourceProxy.from_settings(
        settings=ResourceSettings(
            resource_classes={"Resource": test_class},
            class_name="Resource",
            resources={"sources": {"source": source}},
            raw_arguments=raw_arguments,
        ),
    )

    source._could_be_called = True
    proxy.test_method()
    test_class.parse_init_arguments.assert_called_once_with(**{"raw": "source_value"})
    test_class.assert_called_once_with(**parsed_arguments)


def test_proxy_resource_argument_nested(mocker: pytest_mock.MockFixture):
    test_class = mocker.Mock(spec=protocol.BaseResourceProtocol)

    raw_arguments = {"raw": "$sources[$sources[source2][source2_key]][$sources[source3][source3_key]]"}
    source = mocker.MagicMock(spec=protocol.SourceProtocol)
    source.__getitem__.return_value = "source_value"
    source2 = mocker.MagicMock(spec=protocol.SourceProtocol)
    source2.__getitem__.return_value = "source2_value"
    source3 = mocker.MagicMock(spec=protocol.SourceProtocol)
    source3.__getitem__.return_value = "source3_value"

    parsed_arguments = {"parsed": "parsed"}
    test_class.parse_init_arguments.return_value = parsed_arguments

    proxy = ResourceProxy.from_settings(
        settings=ResourceSettings(
            resource_classes={"Resource": test_class},
            class_name="Resource",
            resources={"sources": {"source2_value": source, "source2": source2, "source3": source3}},
            raw_arguments=raw_arguments,
        ),
    )

    source.__getitem__.assert_not_called()

    proxy.test_method()
    source2.__getitem__.assert_called_once_with("source2_key")
    source3.__getitem__.assert_called_once_with("source3_key")

    test_class.parse_init_arguments.assert_called_once_with(**{"raw": "source_value"})
    test_class.assert_called_once_with(**parsed_arguments)


def test_proxy_resource_argument_resource(mocker: pytest_mock.MockFixture):
    test_class = mocker.Mock(spec=protocol.BaseResourceProtocol)

    raw_arguments = {"raw": "$sources[source]"}
    source = mocker.MagicMock()

    parsed_arguments = {"parsed": "parsed"}
    test_class.parse_init_arguments.return_value = parsed_arguments

    proxy = ResourceProxy.from_settings(
        settings=ResourceSettings(
            resource_classes={"Resource": test_class},
            class_name="Resource",
            resources={"sources": {"source": source}},
            raw_arguments=raw_arguments,
        ),
    )

    source.__getitem__.assert_not_called()

    proxy.test_method()
    test_class.parse_init_arguments.assert_called_once_with(**{"raw": source})
    test_class.assert_called_once_with(**parsed_arguments)


def test_proxy_resource_argument_invalid_format(mocker: pytest_mock.MockFixture):
    test_class = mocker.Mock(spec=protocol.BaseResourceProtocol)

    raw_arguments = {"raw": "$invalid_format"}

    proxy = ResourceProxy.from_settings(
        settings=ResourceSettings(
            resource_classes={"Resource": test_class},
            class_name="Resource",
            resources={},
            raw_arguments=raw_arguments,
        ),
    )
    with pytest.raises(ResourceProxy.InvalidResourceArgumentFormatError):
        proxy.test_method()


def test_proxy_resource_argument_unknown_resource_type(mocker: pytest_mock.MockFixture):
    test_class = mocker.Mock(spec=protocol.BaseResourceProtocol)

    raw_arguments = {"raw": "$unknown_resource_type[key]"}

    proxy = ResourceProxy.from_settings(
        settings=ResourceSettings(
            resource_classes={"Resource": test_class},
            class_name="Resource",
            resources={},
            raw_arguments=raw_arguments,
        ),
    )
    with pytest.raises(ResourceProxy.ResourceTypeNotFoundError):
        proxy.test_method()


def test_proxy_resource_argument_unknown_resource(mocker: pytest_mock.MockFixture):
    test_class = mocker.Mock(spec=protocol.BaseResourceProtocol)

    raw_arguments = {"raw": "$sources[unknown_resource]"}

    proxy = ResourceProxy.from_settings(
        settings=ResourceSettings(
            resource_classes={"Resource": test_class},
            class_name="Resource",
            resources={"sources": {}},
            raw_arguments=raw_arguments,
        ),
    )
    with pytest.raises(ResourceProxy.ResourceNotFoundError):
        proxy.test_method()


def test_proxy_resource_argument_resource_error(mocker: pytest_mock.MockFixture):
    test_class = mocker.Mock(spec=protocol.BaseResourceProtocol)

    raw_arguments = {"raw": "$sources[source][key]"}
    parsed_arguments = {"parsed": "parsed"}
    source = mocker.MagicMock(spec=protocol.SourceProtocol)
    source.__getitem__.side_effect = protocol.SourceProtocol.BaseError
    test_class.parse_init_arguments.return_value = parsed_arguments

    proxy = ResourceProxy.from_settings(
        settings=ResourceSettings(
            resource_classes={"Resource": test_class},
            class_name="Resource",
            resources={"sources": {"source": source}},
            raw_arguments=raw_arguments,
        ),
    )

    proxy.test_method()

    # raises on assert_called_once_with due to lazy evaluation
    with pytest.raises(ResourceProxy.ResourceError):
        test_class.parse_init_arguments.assert_called_once_with(**{"raw": "source_value"})
    test_class.assert_called_once_with(**parsed_arguments)


def test_proxy_resource_argument_resource_name_invalid_type(mocker: pytest_mock.MockFixture):
    test_class = mocker.Mock(spec=protocol.BaseResourceProtocol)

    raw_arguments = {"raw": "$sources[$sources[source2][source2_key]][key]"}
    source = mocker.MagicMock(spec=protocol.SourceProtocol)
    source.__getitem__.return_value = "source_value"
    source2 = mocker.MagicMock(spec=protocol.SourceProtocol)
    source2.__getitem__.return_value = 42

    parsed_arguments = {"parsed": "parsed"}
    test_class.parse_init_arguments.return_value = parsed_arguments

    proxy = ResourceProxy.from_settings(
        settings=ResourceSettings(
            resource_classes={"Resource": test_class},
            class_name="Resource",
            resources={"sources": {"source": source, "source2": source2}},
            raw_arguments=raw_arguments,
        ),
    )

    source.__getitem__.assert_not_called()

    with pytest.raises(ResourceProxy.InvalidResourceArgumentFormatError):
        proxy.test_method()

    source2.__getitem__.assert_called_once_with("source2_key")
    test_class.parse_init_arguments.assert_not_called()
    test_class.assert_not_called()


def test_proxy_resource_argument_resource_key_invalid_type(mocker: pytest_mock.MockFixture):
    test_class = mocker.Mock(spec=protocol.BaseResourceProtocol)

    raw_arguments = {"raw": "$sources[source][$sources[source2][source2_key]]"}
    source = mocker.MagicMock(spec=protocol.SourceProtocol)
    source.__getitem__.return_value = "source_value"
    source2 = mocker.MagicMock(spec=protocol.SourceProtocol)
    source2.__getitem__.return_value = 42

    parsed_arguments = {"parsed": "parsed"}
    test_class.parse_init_arguments.return_value = parsed_arguments

    proxy = ResourceProxy.from_settings(
        settings=ResourceSettings(
            resource_classes={"Resource": test_class},
            class_name="Resource",
            resources={"sources": {"source": source, "source2": source2}},
            raw_arguments=raw_arguments,
        ),
    )

    source.__getitem__.assert_not_called()

    with pytest.raises(ResourceProxy.InvalidResourceArgumentFormatError):
        proxy.test_method()

    source2.__getitem__.assert_called_once_with("source2_key")
    test_class.parse_init_arguments.assert_not_called()
    test_class.assert_not_called()


def test_proxy_resource_argument_resource_not_gettable(mocker: pytest_mock.MockFixture):
    test_class = mocker.Mock(spec=protocol.BaseResourceProtocol)

    raw_arguments = {"raw": "$destinations[destination][key]"}
    destination = mocker.MagicMock(spec=protocol.DestinationProtocol)

    parsed_arguments = {"parsed": "parsed"}
    test_class.parse_init_arguments.return_value = parsed_arguments

    proxy = ResourceProxy.from_settings(
        settings=ResourceSettings(
            resource_classes={"Resource": test_class},
            class_name="Resource",
            resources={"destinations": {"destination": destination}},
            raw_arguments=raw_arguments,
        ),
    )

    with pytest.raises(ResourceProxy.InvalidResourceTypeError):
        proxy.test_method()

    test_class.parse_init_arguments.assert_not_called()
    test_class.assert_not_called()


def test_proxy_resource_argument_not_full_resource_name_block(mocker: pytest_mock.MockFixture):
    test_class = mocker.Mock(spec=protocol.BaseResourceProtocol)

    raw_arguments = {"raw": "$sources[source"}
    source = mocker.MagicMock(spec=protocol.SourceProtocol)
    source.__getitem__.return_value = "source_value"

    parsed_arguments = {"parsed": "parsed"}
    test_class.parse_init_arguments.return_value = parsed_arguments

    proxy = ResourceProxy.from_settings(
        settings=ResourceSettings(
            resource_classes={"Resource": test_class},
            class_name="Resource",
            resources={"sources": {"source": source}},
            raw_arguments=raw_arguments,
        ),
    )

    source.__getitem__.assert_not_called()

    with pytest.raises(ResourceProxy.InvalidResourceArgumentFormatError):
        proxy.test_method()

    test_class.parse_init_arguments.assert_not_called()
    test_class.assert_not_called()


def test_proxy_resource_argument_not_full_key_block(mocker: pytest_mock.MockFixture):
    test_class = mocker.Mock(spec=protocol.BaseResourceProtocol)

    raw_arguments = {"raw": "$sources[source][key"}
    source = mocker.MagicMock(spec=protocol.SourceProtocol)
    source.__getitem__.return_value = "source_value"

    parsed_arguments = {"parsed": "parsed"}
    test_class.parse_init_arguments.return_value = parsed_arguments

    proxy = ResourceProxy.from_settings(
        settings=ResourceSettings(
            resource_classes={"Resource": test_class},
            class_name="Resource",
            resources={"sources": {"source": source}},
            raw_arguments=raw_arguments,
        ),
    )

    source.__getitem__.assert_not_called()

    with pytest.raises(ResourceProxy.InvalidResourceArgumentFormatError):
        proxy.test_method()

    test_class.parse_init_arguments.assert_not_called()
    test_class.assert_not_called()


def test_proxy_resource_argument_too_many_blocks(mocker: pytest_mock.MockFixture):
    test_class = mocker.Mock(spec=protocol.BaseResourceProtocol)

    raw_arguments = {"raw": "$sources[source][key][key2]"}
    source = mocker.MagicMock(spec=protocol.SourceProtocol)
    source.__getitem__.return_value = "source_value"

    parsed_arguments = {"parsed": "parsed"}
    test_class.parse_init_arguments.return_value = parsed_arguments

    proxy = ResourceProxy.from_settings(
        settings=ResourceSettings(
            resource_classes={"Resource": test_class},
            class_name="Resource",
            resources={"sources": {"source": source}},
            raw_arguments=raw_arguments,
        ),
    )

    source.assert_not_called()

    with pytest.raises(ResourceProxy.InvalidResourceArgumentFormatError):
        proxy.test_method()

    test_class.parse_init_arguments.assert_not_called()
    test_class.assert_not_called()
