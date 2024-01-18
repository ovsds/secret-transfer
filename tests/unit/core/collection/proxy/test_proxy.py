import typing

import pytest

import secret_transfer.core as core
import secret_transfer.protocol as protocol
import tests.unit.core.base.proxy.resource.suite as test_suite


class TestCollectionProxy(test_suite.ResourceProxySuite[protocol.CollectionProtocol]):
    @pytest.fixture(name="collection")
    def fixture_collection(self) -> type[protocol.CollectionProtocol]:
        class TestCollection(core.AbstractCollection):
            __register__ = False

        return TestCollection

    @pytest.fixture(name="target_proxy")
    def fixture_target_proxy(self) -> type[core.CollectionProxy]:
        return core.CollectionProxy

    @pytest.fixture(name="target_settings")
    def fixture_target_settings(self) -> type[core.CollectionSettings]:
        return core.CollectionSettings

    @pytest.fixture(name="classes")
    def fixture_classes(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        class_name: str,
        collection: type[protocol.CollectionProtocol],
    ) -> typing.Mapping[str, type[protocol.CollectionProtocol]]:
        return {class_name: collection}

    @pytest.fixture(name="default_class")
    def fixture_default_class(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, collection: type[protocol.CollectionProtocol]
    ) -> type[protocol.CollectionProtocol]:
        return collection

    @pytest.fixture(name="class_name")
    def fixture_class_name(self) -> str:
        return "TestCollection"
