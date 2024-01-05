import secret_transfer.core.base as core_base
import secret_transfer.protocol as protocol

DestinationClassSettings = core_base.ResourceClassSettings[protocol.DestinationProtocol]
DestinationSettings = core_base.ResourceSettings[protocol.DestinationProtocol]


class DestinationClassProxy(core_base.BaseClassProxy[protocol.DestinationProtocol]):
    _proxy_protocol = protocol.DestinationProtocol


class DestinationProxy(core_base.BaseResourceProxy[protocol.DestinationProtocol]):
    ...
