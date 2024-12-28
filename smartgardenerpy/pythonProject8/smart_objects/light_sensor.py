import random
import time
import paho.mqtt.client as mqtt
from conf.mqtt_params import MqttConfigurationParameters
import json
import threading

print_lock = threading.Lock()

class LightSensor:
    def __init__(self, client):
        self.client = client
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.username_pw_set(MqttConfigurationParameters.MQTT_USERNAME, MqttConfigurationParameters.MQTT_PASSWORD)
        self.client.connect(MqttConfigurationParameters.BROKER_ADDRESS, MqttConfigurationParameters.BROKER_PORT)
        self.wait_timer = 0  # Timer di attesa

    def on_connect(self, client, userdata, flags, rc):
        with print_lock:
            print("Connected with result code " + str(rc))

    def on_publish(self, client, mid, userdata):
        with print_lock:
            print(f"Message published: {self.last_published_message}")

    def read_light(self):
        self.light = random.uniform(0, 100)
        try:
            # Creo un messaggio SenML+JSON
            senml_message = json.dumps([{"n": "light", "u": "%", "v": self.light}])
            self.last_published_message = senml_message
            self.client.publish(MqttConfigurationParameters.LIGHT_SENSOR_TOPIC, senml_message)
            with print_lock:
                print(f"Generated light value: {senml_message}")
        except Exception as e:
            with print_lock:
                print("Failed to publish message: " + str(e))

        # Controllo il range della luce
        if not 30 <= self.light <= 70:
            self.wait_timer = 10  # Imposto un timer di attesa di 10 secondi

    def wait(self):
        if self.wait_timer > 0:
            time.sleep(self.wait_timer)
            self.wait_timer = 0

    def to_json(self):
        return {
            "light": self.light,
        }
