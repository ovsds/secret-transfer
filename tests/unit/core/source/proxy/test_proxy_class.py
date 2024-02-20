import pytest

import secret_transfer.core as core
import secret_transfer.protocol as protocol
import tests.unit.core.base.proxy.resource_class.suite as test_suite


class Source(core.AbstractSource):
    __register__ = False


class InvalidSource: ...


class TestSourceClassProxy(test_suite.ClassProxySuite[protocol.SourceProtocol]):
    @pytest.fixture(name="target_class_proxy")
    def fixture_target_class_proxy(self) -> type[core.SourceClassProxy]:
        return core.SourceClassProxy

    @pytest.fixture(name="target_class")
    def fixture_target_class(self) -> type[protocol.SourceProtocol]:
        return Source

    @pytest.fixture(name="invalid_protocol_class_name")
    def fixture_invalid_protocol_class_name(self) -> str:
        return "InvalidSource"
