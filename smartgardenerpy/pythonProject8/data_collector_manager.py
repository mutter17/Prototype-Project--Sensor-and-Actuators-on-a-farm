import time
from smart_objects.humidity_sensor import HumiditySensor
from smart_objects.irrigation_system import IrrigationSystem
from smart_objects.light_sensor import LightSensor
from smart_objects.shade_system import ShadeSystem
from conf.mqtt_params import MqttConfigurationParameters
import paho.mqtt.client as mqtt
import json
import threading

print_lock = threading.Lock()

class DataCollectorManager:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message
        self.client.username_pw_set(MqttConfigurationParameters.MQTT_USERNAME, MqttConfigurationParameters.MQTT_PASSWORD)
        self.client.connect(MqttConfigurationParameters.BROKER_ADDRESS, MqttConfigurationParameters.BROKER_PORT)
        self.irrigation_system = IrrigationSystem(self.client)
        self.humidity_sensor = HumiditySensor(self.client)
        self.light_sensor = LightSensor(self.client)
        self.shade_system = ShadeSystem(self.client)

    def on_connect(self, client, userdata, flags, rc):
        with print_lock:
            print("Connected with result code " + str(rc))
        client.subscribe(MqttConfigurationParameters.MQTT_BASIC_TOPIC + "greenhouse/#")

    def on_publish(self, client, mid, userdata):
        with print_lock:
            print(f"Message published: {userdata}")

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode("utf-8")
        with print_lock:
            print(f"Received message: {payload}")

        if topic == MqttConfigurationParameters.HUMIDITY_SENSOR_TOPIC:
            if not 30 <= float(payload) <= 70:
                self.humidity_sensor.wait_timer = 10

        elif topic == MqttConfigurationParameters.IRRIGATION_SYSTEM_TOPIC:
            self.irrigation_system.irrigation_history.append({"timestamp": int(time.time()), "state": payload})

        elif topic == MqttConfigurationParameters.SHADE_SYSTEM_TOPIC:
            self.shade_system.shade_history.append({"timestamp": int(time.time()), "state": payload})

    def run(self):
        self.client.loop_start()
        while True:
            self.humidity_sensor.read_humidity()
            self.light_sensor.read_light()

            # Verifico la logica per il sistema di irrigazione e ombreggiamento
            humidity = self.humidity_sensor.to_json()["humidity"]
            if humidity < 30:
                self.irrigation_system.turn_on()
            else:
                self.irrigation_system.turn_off()

            light = self.light_sensor.to_json()["light"]
            if light > 70:
                self.shade_system.turn_on()
            else:
                self.shade_system.turn_off()

            time.sleep(10)  # Aspetto 10s per la prossima iterazione
        self.client.loop_stop()
