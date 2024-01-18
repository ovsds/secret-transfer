import typing

import pytest

import secret_transfer.core as core
import secret_transfer.protocol as protocol
import tests.unit.core.base.proxy.resource.suite as test_suite


class TestDestinationProxy(test_suite.ResourceProxySuite[protocol.DestinationProtocol]):
    @pytest.fixture(name="collection")
    def fixture_collection(self) -> type[protocol.DestinationProtocol]:
        class TestDestination(core.AbstractDestination):
            __register__ = False

        return TestDestination

    @pytest.fixture(name="target_proxy")
    def fixture_target_proxy(self) -> type[core.DestinationProxy]:
        return core.DestinationProxy

    @pytest.fixture(name="target_settings")
    def fixture_target_settings(self) -> type[core.DestinationSettings]:
        return core.DestinationSettings

    @pytest.fixture(name="classes")
    def fixture_classes(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        class_name: str,
        collection: type[protocol.DestinationProtocol],
    ) -> typing.Mapping[str, type[protocol.DestinationProtocol]]:
        return {class_name: collection}

    @pytest.fixture(name="default_class")
    def fixture_default_class(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, collection: type[protocol.DestinationProtocol]
    ) -> type[protocol.DestinationProtocol]:
        return collection

    @pytest.fixture(name="class_name")
    def fixture_class_name(self) -> str:
        return "TestDestination"
