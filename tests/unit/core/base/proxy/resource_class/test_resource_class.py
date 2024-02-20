import typing

import pytest

import secret_transfer.core.base as core_base
import secret_transfer.protocol as protocol
import tests.unit.core.base.proxy.resource_class.suite as test_suite


@typing.runtime_checkable
class ResourceProtocol(protocol.BaseResourceProtocol, typing.Protocol): ...


class Resource(core_base.BaseResource): ...


class InvalidProtocolResource: ...


class ResourceClassProxy(core_base.BaseClassProxy[ResourceProtocol]):
    _proxy_protocol = ResourceProtocol


class TestResourceClassProxy(test_suite.ClassProxySuite[ResourceProtocol]):
    @pytest.fixture(name="target_class_proxy")
    def fixture_target_class_proxy(self) -> type[core_base.BaseClassProxy[ResourceProtocol]]:
        return ResourceClassProxy

    @pytest.fixture(name="target_class")
    def fixture_target_class(self) -> type[ResourceProtocol]:
        return Resource

    @pytest.fixture(name="invalid_protocol_class_name")
    def fixture_invalid_protocol_class_name(self) -> str:
        return "InvalidProtocolResource"
