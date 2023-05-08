import json
import arrow
import hashlib

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, NumberAttribute

from .parse_time import parse_time


class Telemetry(Model):
    class Meta:
        table_name = 'telemetry'
        region = 'us-east-1'

    ccid          = UnicodeAttribute(hash_key=True)
    timestamp     = UnicodeAttribute(range_key=True)
    timezone      = UnicodeAttribute(default='')
    imei          = UnicodeAttribute(default='')
    alarm         = BooleanAttribute(default=False)
    temperature   = UnicodeAttribute(default='')
    volts         = UnicodeAttribute(default='')
    modem         = UnicodeAttribute(default='')

    def convert(self, json_message):
        msg = json.loads(json_message)
        self.ccid        = msg.get('ccid')
        self.imei        = msg.get('imei')
        self.modem       = msg.get('modem')
        self.alarm       = msg.get('alarm',False)
        self.temperature = msg.get('temperature','0')
        self.volts       = msg.get('volts','0')

        dt, tz = parse_time(msg.get('timestamp'))
        self.timestamp = dt.isoformat()
        self.timezone = tz

        return self