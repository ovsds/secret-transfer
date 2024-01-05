import pytest

import secret_transfer.core as core
import secret_transfer.protocol as protocol
import tests.unit.core.base.proxy.resource_class.suite as test_suite


class Collection(core.AbstractCollection):
    __register__ = False


class InvalidCollection:
    ...


class TestCollectionClassProxy(test_suite.ClassProxySuite[protocol.CollectionProtocol]):
    @pytest.fixture(name="target_class_proxy")
    def fixture_target_class_proxy(self) -> type[core.CollectionClassProxy]:
        return core.CollectionClassProxy

    @pytest.fixture(name="target_class")
    def fixture_target_class(self) -> type[protocol.CollectionProtocol]:
        return Collection

    @pytest.fixture(name="invalid_protocol_class_name")
    def fixture_invalid_protocol_class_name(self) -> str:
        return "InvalidCollection"
