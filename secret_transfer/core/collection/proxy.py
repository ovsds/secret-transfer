import secret_transfer.core.base as core_base
import secret_transfer.protocol as protocol

CollectionClassSettings = core_base.ResourceClassSettings[protocol.CollectionProtocol]
CollectionSettings = core_base.ResourceSettings[protocol.CollectionProtocol]


class CollectionClassProxy(core_base.BaseClassProxy[protocol.CollectionProtocol]):
    _proxy_protocol = protocol.CollectionProtocol


class CollectionProxy(core_base.BaseResourceProxy[protocol.CollectionProtocol]):
    ...
