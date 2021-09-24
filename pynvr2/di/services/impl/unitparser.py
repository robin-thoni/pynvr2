import datetime

import pint

from pynvr2.di.services.unitparser import UnitParser
from pint import UnitRegistry


class UnitParserImpl(UnitParser):
    def __init__(self):
        self.ureg = UnitRegistry()

    def parse_timedelta(self, value: str) -> datetime.timedelta:
        v = self.ureg(value)
        if isinstance(v, int):
            return datetime.timedelta(minutes=v)
        elif isinstance(v, pint.Quantity):
            return v.to_timedelta()
        else:
            raise ValueError()

    def parse_bytes(self, value: str) -> int:
        v = self.ureg(value)
        if isinstance(v, int):
            return v
        elif isinstance(v, pint.Quantity):
            b = v.to('bytes')
            return b.magnitude
        else:
            raise ValueError()
