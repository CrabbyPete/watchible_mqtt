import logging
import paho.mqtt.client as mqtt

log_format = '[%(asctime)s] [%(levelname)s] - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)
log = logging.getLogger('watchible_mqtt')

from models.telemetry import Telemetry
from models.mongo_telemetry import MongoTelemetry

message = '{"modem": "Quectel_BC660K-GL", "ccid": "89882280666027595358", "imei": "866207053437178", "alarm": false, "temperature": "23.29925", "timestamp": "23/08/01,13:24:17-16", "volts": "3406"}'

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    log.info("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.publish("device/state",message)

def on_publish(client,userdata,result):
    print("data published \n")


client = mqtt.Client()  # Create instance of client with client ID “digi_mqtt_test”
#client.tls_set(ca_certs='mosquitto.org.crt', tls_version=mqtt.ssl.PROTOCOL_TLS)
client.on_connect = on_connect  # Define callback function for successful connection
client.on_publish = on_publish  # Define callback function for receipt of a message
client.username_pw_set("watchible", "w@tch_0ne")
client.connect('54.196.22.131', 1883, 30)  # Connect to (broker, port, keepalive-time)

client.loop_forever()  # Start networking daemon