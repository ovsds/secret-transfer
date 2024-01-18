import pytest

import secret_transfer.core as core
import secret_transfer.protocol as protocol
import tests.unit.core.base.proxy.resource_class.suite as test_suite


class Destination(core.AbstractDestination):
    __register__ = False


class InvalidDestination:
    ...


class TestDestinationClassProxy(test_suite.ClassProxySuite[protocol.DestinationProtocol]):
    @pytest.fixture(name="target_class_proxy")
    def fixture_target_class_proxy(self) -> type[core.DestinationClassProxy]:
        return core.DestinationClassProxy

    @pytest.fixture(name="target_class")
    def fixture_target_class(self) -> type[protocol.DestinationProtocol]:
        return Destination

    @pytest.fixture(name="invalid_protocol_class_name")
    def fixture_invalid_protocol_class_name(self) -> str:
        return "InvalidDestination"
