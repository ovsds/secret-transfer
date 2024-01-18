import typing

import pytest

import secret_transfer.core as core
import secret_transfer.protocol as protocol
import tests.unit.core.base.proxy.resource.suite as test_suite


class TestSourceProxy(test_suite.ResourceProxySuite[protocol.SourceProtocol]):
    @pytest.fixture(name="collection")
    def fixture_collection(self) -> type[protocol.SourceProtocol]:
        class TestSource(core.AbstractSource):
            __register__ = False

        return TestSource

    @pytest.fixture(name="target_proxy")
    def fixture_target_proxy(self) -> type[core.SourceProxy]:
        return core.SourceProxy

    @pytest.fixture(name="target_settings")
    def fixture_target_settings(self) -> type[core.SourceSettings]:
        return core.SourceSettings

    @pytest.fixture(name="classes")
    def fixture_classes(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        class_name: str,
        collection: type[protocol.SourceProtocol],
    ) -> typing.Mapping[str, type[protocol.SourceProtocol]]:
        return {class_name: collection}

    @pytest.fixture(name="default_class")
    def fixture_default_class(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, collection: type[protocol.SourceProtocol]
    ) -> type[protocol.SourceProtocol]:
        return collection

    @pytest.fixture(name="class_name")
    def fixture_class_name(self) -> str:
        return "TestSource"
