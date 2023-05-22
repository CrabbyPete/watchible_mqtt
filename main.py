import logging
import paho.mqtt.client as mqtt


log = logging.getLogger('watchible_mqtt')
log.setLevel(logging.INFO)

from models.telemetry import Telemetry
from models.mongo_telemetry import MongoTelemetry

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    log.info("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("device/state")  # Subscribe to the topic “digitest/test1”, receive any messages published on it


def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    log.info("Message-> " + msg.topic + " " + str(msg.payload))  # Print a received msg

    try:
        msg_str = msg.payload.decode('utf-8')
    except Exception as e:
        log.error(f"Error jsonifing {msg}")
        return

    try:
        telemetry = Telemetry()
        telemetry.convert(msg_str)
        telemetry.save()
    except Exception as e:
        log.error(f"Error {str(e)} converting {msg_str} to Dynamo")

    try:
        mongo_telemetry = MongoTelemetry()
        mongo_telemetry.convert(msg_str)
        mongo_telemetry.save()
    except Exception as e:
        log.error(f"Error {str(e)} converting {msg_str} to MongoDB")


client = mqtt.Client()  # Create instance of client with client ID “digi_mqtt_test”
#client.tls_set(ca_certs='mosquitto.org.crt', tls_version=mqtt.ssl.PROTOCOL_TLS)
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
client.username_pw_set("watchible", "w@tch_0ne")
client.connect('54.196.22.131', 1883, 30)  # Connect to (broker, port, keepalive-time)

client.loop_forever()  # Start networking daemon