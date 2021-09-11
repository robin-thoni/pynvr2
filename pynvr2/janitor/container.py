from dependency_injector import containers, providers

from pynvr2.di.services.impl.datetime import DateTimeImpl
from pynvr2.di.services.impl.recordsegmentdetails import RecordSegmentDetailsImpl
from pynvr2.di.services.impl.ioro import IORo
from pynvr2.di.services.impl.iorw import IORw
from pynvr2.di.services.impl.unitparser import UnitParserImpl
from pynvr2.models.args.janitorargsmodel import JanitorArgsModel
from pynvr2.models.config.configmodel import ConfigModel
from pynvr2.janitor.mop import Mop
from pynvr2.janitor.policies.policiesstore import policies


class Container(containers.DeclarativeContainer):

    __self__ = providers.Self()

    config = providers.Singleton(ConfigModel)
    options = providers.Singleton(JanitorArgsModel)

    datetime = providers.Singleton(DateTimeImpl)
    record_segment_details = providers.Singleton(RecordSegmentDetailsImpl)
    unit_parser = providers.Singleton(UnitParserImpl)

    _io_selector = providers.Configuration()
    io_ro = providers.Singleton(IORo)
    io_rw = providers.Singleton(IORw)
    io = providers.Selector(
        _io_selector.io_selector,
        io_ro=io_ro,
        io_rw=io_rw,
    )

    mop = providers.Singleton(Mop,
                              options=options,
                              config=config,
                              io=io,
                              container=__self__,
                              record_segment_details=record_segment_details,
                              )

    policies = providers.Factory(policies.instanciate, __self__)
