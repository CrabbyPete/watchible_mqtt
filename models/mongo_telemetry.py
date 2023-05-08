import json
import arrow

from mongoengine import Document, StringField, BooleanField, DecimalField, DateTimeField

from .parse_time import parse_time


class MongoTelemetry(Document):
    ccid = StringField(required=True)
    imei = StringField()
    timestamp = DateTimeField()
    timezone = StringField()
    alarm = BooleanField()
    temperature = DecimalField(precision=2)
    volts = DecimalField(precision=3)
    modem=StringField()
    raw = StringField()


    def convert(self, data):
        """
        Convert a message from the device
        :param data:
            b'{"timestamp": "23/04/24,16:29:00-16",
               "imei": "866207053437178",
               "ccid": "89882280666027595358",
               "volts": "3417",
               "alarm": false,
               "temperature": "22.8311"}'
        :return:
        """
        self.raw = data
        msg = json.loads(data)

        self.imei = msg.get('imei')
        self.ccid = msg.get('ccid')
        self.temperature = float(msg.get('temperature').strip())
        self.volts = float(msg.get('volts').strip())/100
        self.alarm = msg.get('alarm',False)
        modem = msg.get('modem')
        dt,tz = parse_time(msg.get('timestamp'))
        self.timestamp = dt.datetime
        self.timezone = tz


