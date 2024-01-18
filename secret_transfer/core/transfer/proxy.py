import secret_transfer.core.base as core_base
import secret_transfer.protocol as protocol

TransferClassSettings = core_base.ResourceClassSettings[protocol.TransferProtocol]
TransferSettings = core_base.ResourceSettings[protocol.TransferProtocol]


class TransferClassProxy(core_base.BaseClassProxy[protocol.TransferProtocol]):
    _proxy_protocol = protocol.TransferProtocol


class TransferProxy(core_base.BaseResourceProxy[protocol.TransferProtocol]):
    ...
