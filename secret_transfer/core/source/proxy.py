import secret_transfer.core.base as core_base
import secret_transfer.protocol as protocol

SourceClassSettings = core_base.ResourceClassSettings[protocol.SourceProtocol]
SourceSettings = core_base.ResourceSettings[protocol.SourceProtocol]


class SourceClassProxy(core_base.BaseClassProxy[protocol.SourceProtocol]):
    _proxy_protocol = protocol.SourceProtocol


class SourceProxy(core_base.BaseResourceProxy[protocol.SourceProtocol]):
    ...
