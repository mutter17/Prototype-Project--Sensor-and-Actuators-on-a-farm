class MqttConfigurationParameters(object):
    BROKER_ADDRESS = "155.185.4.4"
    BROKER_PORT = 7883
    MQTT_USERNAME = "292832@studenti.unimore.it"
    MQTT_PASSWORD = "wslkiugfccbdsrju"
    MQTT_BASIC_TOPIC = "/iot/user/292832@studenti.unimore.it/"
    HUMIDITY_SENSOR_TOPIC = MQTT_BASIC_TOPIC + "greenhouse/humidity_sensor"
    LIGHT_SENSOR_TOPIC = MQTT_BASIC_TOPIC + "greenhouse/light_sensor"
    IRRIGATION_SYSTEM_TOPIC = MQTT_BASIC_TOPIC + "greenhouse/irrigation_system"
    SHADE_SYSTEM_TOPIC = MQTT_BASIC_TOPIC + "greenhouse/shade_system"
