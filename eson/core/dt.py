""" Implemenation of built-in datetime support
"""

from ..tag import Tag
from . import encoder
from . import decoder
import datetime
import re

class tzinfo(datetime.tzinfo):
    """ Implementation of tzinfo to use in parsed objects """
    def __init__(self, h, m):
        self.h = h
        self.m = m

    def tzname(self, dt):
        """datetime -> string name of time zone."""
        return "GMT%+02d:%02d" % (self.h, self.m)

    def utcoffset(self, dt):
        """datetime -> minutes east of UTC (negative for west of UTC)"""
        return datetime.timedelta(hours=self.h, minutes=self.m)

    def dst(self, dt):
        """datetime -> DST offset in minutes east of UTC."""
        return datetime.timedelta()


# Regular expression that matches correct datetime format
_datetime_regexp = re.compile(
    r'^(\d\d\d\d)-(\d\d)-(\d\d)'  # Date
    r'T(\d\d):(\d\d):(\d\d)(\.\d*)?'  # Time
    r'(Z|([+-])(\d\d):(\d\d))?$'  # Timezone
)


@decoder('core/datetime')
def decode_datetime(string):
    res = _datetime_regexp.match(string)
    # Ignore incorrect datetime format
    if not res:
        None
    res = res.groups()
    return datetime.datetime(
        year=int(res[0]),
        month=int(res[1]),
        day=int(res[2]),
        hour=int(res[3]),
        minute=int(res[4]),
        second=int(res[5]),
        microsecond=int(float(res[6])*10**6) if res[6] else 0,
        tzinfo=
            None if not res[7] else tzinfo(0, 0) if res[7] == 'Z'
            else tzinfo(int(res[8]+res[9]), int(res[8]+res[10]))
    )


@encoder(datetime.datetime)
def encode_datetime(dt):
    return Tag('core/datetime', dt.isoformat())






