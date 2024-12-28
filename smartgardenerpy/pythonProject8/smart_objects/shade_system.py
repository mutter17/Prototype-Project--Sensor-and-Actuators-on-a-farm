import json
import time
import threading
import paho.mqtt.client as mqtt
from conf.mqtt_params import MqttConfigurationParameters

print_lock = threading.Lock()

class ShadeSystem:
    def __init__(self, client):
        self.client = client
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.username_pw_set(MqttConfigurationParameters.MQTT_USERNAME, MqttConfigurationParameters.MQTT_PASSWORD)
        self.client.connect(MqttConfigurationParameters.BROKER_ADDRESS, MqttConfigurationParameters.BROKER_PORT)
        self.state = "OFF"
        self.shade_history = []  # Storico dei programmi di ombreggiamento

    def on_connect(self, client, userdata, flags, rc):
        with print_lock:
            print("Connected with result code " + str(rc))

    def on_publish(self, client, mid, userdata):
        with print_lock:
            print(f"Message published: {self.last_published_message}")

    def turn_on(self):
        self.state = "ON"
        timestamp = int(time.time())
        with print_lock:
            print(f"Shade system state: {self.state}, timestamp: {timestamp}")
        try:
            # Creo un messaggio JSON
            json_message = json.dumps({"state": self.state})
            self.last_published_message = json_message
            self.client.publish(MqttConfigurationParameters.SHADE_SYSTEM_TOPIC, json_message)
            with print_lock:
                print(f"Shade system message: {json_message}")
            self.shade_history.append({"timestamp": timestamp, "state": self.state})
        except Exception as e:
            with print_lock:
                print("Failed to publish message: " + str(e))
            self.state = "OFF"

    def turn_off(self):
        self.state = "OFF"
        timestamp = int(time.time())
        with print_lock:
            print(f"Shade system state: {self.state}, timestamp: {timestamp}")
        try:
            # Creo un messaggio JSON
            json_message = json.dumps({"state": self.state})
            self.last_published_message = json_message
            self.client.publish(MqttConfigurationParameters.SHADE_SYSTEM_TOPIC, json_message)
            with print_lock:
                print(f"Shade system message: {json_message}")
            self.shade_history.append({"timestamp": timestamp, "state": self.state})
        except Exception as e:
            with print_lock:
                print("Failed to publish message: " + str(e))
            self.state = "ON"

    def to_json(self):
        return {
            "state": self.state,
            "shade_history": self.shade_history
        }
