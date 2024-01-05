import typing

import pytest

import secret_transfer.core.base as core_base
import secret_transfer.protocol as protocol


class ResourceProxySuite(typing.Generic[protocol.ResourceType]):
    @pytest.fixture(name="target_proxy")
    def fixture_target_proxy(self) -> type[core_base.BaseResourceProxy[protocol.ResourceType]]:
        raise NotImplementedError

    @pytest.fixture(name="target_settings")
    def fixture_target_settings(self) -> type[core_base.ResourceSettings[protocol.ResourceType]]:
        raise NotImplementedError

    @pytest.fixture(name="classes")
    def fixture_classes(self) -> typing.Mapping[str, type[protocol.ResourceType]]:
        raise NotImplementedError

    @pytest.fixture(name="default_class")
    def fixture_default_class(self) -> type[protocol.ResourceType]:
        raise NotImplementedError

    @pytest.fixture(name="resources")
    def fixture_resources(self) -> typing.Mapping[str, typing.Mapping[str, protocol.SourceProtocol]]:
        return {}

    @pytest.fixture(name="class_name")
    def fixture_class_name(self) -> str:
        raise NotImplementedError

    @pytest.fixture(name="raw_arguments")
    def fixture_raw_arguments(self) -> typing.Mapping[str, typing.Any]:
        return {}

    def test_default(
        self,
        target_proxy: type[core_base.BaseResourceProxy[protocol.ResourceType]],
        target_settings: type[core_base.ResourceSettings[protocol.ResourceType]],
        classes: typing.Mapping[str, type[protocol.ResourceType]],
        default_class: type[protocol.ResourceType],
        resources: typing.Mapping[str, typing.Mapping[str, protocol.SourceProtocol]],
        class_name: str,
        raw_arguments: typing.Mapping[str, typing.Any],
    ):
        proxy = target_proxy.from_settings(
            settings=target_settings(
                resource_classes=classes,
                default_resource_class=default_class,
                resources=resources,
                class_name=class_name,
                raw_arguments=raw_arguments,
            ),
        )

        assert isinstance(proxy, default_class)

    def test_default_class_name(
        self,
        target_proxy: type[core_base.BaseResourceProxy[protocol.ResourceType]],
        target_settings: type[core_base.ResourceSettings[protocol.ResourceType]],
        classes: typing.Mapping[str, type[protocol.ResourceType]],
        default_class: type[protocol.ResourceType],
        resources: typing.Mapping[str, typing.Mapping[str, protocol.SourceProtocol]],
        raw_arguments: typing.Mapping[str, typing.Any],
    ):
        proxy = target_proxy.from_settings(
            settings=target_settings(
                resource_classes=classes,
                default_resource_class=default_class,
                resources=resources,
                raw_arguments=raw_arguments,
            ),
        )

        assert isinstance(proxy, default_class)

    def test_no_class_name_or_default_class_name(
        self,
        target_proxy: type[core_base.BaseResourceProxy[protocol.ResourceType]],
        target_settings: type[core_base.ResourceSettings[protocol.ResourceType]],
        classes: typing.Mapping[str, type[protocol.ResourceType]],
        default_class: type[protocol.ResourceType],
        resources: typing.Mapping[str, typing.Mapping[str, protocol.SourceProtocol]],
        raw_arguments: typing.Mapping[str, typing.Any],
    ):
        proxy = target_proxy.from_settings(
            settings=target_settings(
                resource_classes=classes,
                resources=resources,
                raw_arguments=raw_arguments,
            ),
        )

        with pytest.raises(core_base.BaseResourceProxy.ClassNotFoundError):
            assert isinstance(proxy, default_class)

    def test_unknown_class_name(
        self,
        target_proxy: type[core_base.BaseResourceProxy[protocol.ResourceType]],
        target_settings: type[core_base.ResourceSettings[protocol.ResourceType]],
        classes: typing.Mapping[str, type[protocol.ResourceType]],
        default_class: type[protocol.ResourceType],
        resources: typing.Mapping[str, typing.Mapping[str, protocol.SourceProtocol]],
        raw_arguments: typing.Mapping[str, typing.Any],
    ):
        proxy = target_proxy.from_settings(
            settings=target_settings(
                resource_classes=classes,
                default_resource_class=default_class,
                resources=resources,
                class_name="UnknownClass",
                raw_arguments=raw_arguments,
            ),
        )

        with pytest.raises(core_base.BaseResourceProxy.ClassNotFoundError):
            assert isinstance(proxy, default_class)
