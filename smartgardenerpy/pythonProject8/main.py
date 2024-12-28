from greenhouse import Greenhouse
from data_collector_manager import DataCollectorManager
import paho.mqtt.client as mqtt
from conf.mqtt_params import MqttConfigurationParameters
import threading

print_lock = threading.Lock()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        with print_lock:
            print("Connected successfully.")
    else:
        with print_lock:
            print("Connection failed with error code "+str(rc))
        exit(1)
    client.subscribe(MqttConfigurationParameters.MQTT_BASIC_TOPIC + "greenhouse/#")

def on_message(client, userdata, msg):
    with print_lock:
        print(f"Received message: {msg.payload.decode('utf-8')}")

client_id = "python-greenhouse-consumer-{0}".format(MqttConfigurationParameters.MQTT_USERNAME)

mqtt_client = mqtt.Client(client_id)
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect

mqtt_client.username_pw_set(MqttConfigurationParameters.MQTT_USERNAME, MqttConfigurationParameters.MQTT_PASSWORD)

with print_lock:
    print("Connecting to " + MqttConfigurationParameters.BROKER_ADDRESS + " port: " + str(MqttConfigurationParameters.BROKER_PORT))
try:
    mqtt_client.connect(MqttConfigurationParameters.BROKER_ADDRESS, MqttConfigurationParameters.BROKER_PORT)
except Exception as e:
    with print_lock:
        print("Failed to connect to MQTT broker: "+str(e))
    exit(1)

mqtt_client.loop_start()

# Creo un'istanza del DataCollector e la eseguo
data_collector_manager = DataCollectorManager()
data_collector_manager.run()

mqtt_client.loop_stop()
