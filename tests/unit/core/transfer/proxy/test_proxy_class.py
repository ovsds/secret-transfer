import pytest

import secret_transfer.core as core
import secret_transfer.protocol as protocol
import tests.unit.core.base.proxy.resource_class.suite as test_suite


class Transfer(core.AbstractTransfer):
    __register__ = False


class InvalidTransfer:
    ...


class TestTransferClassProxy(test_suite.ClassProxySuite[protocol.TransferProtocol]):
    @pytest.fixture(name="target_class_proxy")
    def fixture_target_class_proxy(self) -> type[core.TransferClassProxy]:
        return core.TransferClassProxy

    @pytest.fixture(name="target_class")
    def fixture_target_class(self) -> type[protocol.TransferProtocol]:
        return Transfer

    @pytest.fixture(name="invalid_protocol_class_name")
    def fixture_invalid_protocol_class_name(self) -> str:
        return "InvalidTransfer"
