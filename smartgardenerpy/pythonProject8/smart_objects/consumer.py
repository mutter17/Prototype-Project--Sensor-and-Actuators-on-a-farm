import paho.mqtt.client as mqtt
from conf.mqtt_params import MqttConfigurationParameters

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Si iscrive ai vari topic creati per la serra
    topics = ["humidity_sensor", "light_sensor", "irrigation_system", "shade_system"]
    for topic in topics:
        mqtt_topic = "{0}/greenhouse/{1}".format(MqttConfigurationParameters.MQTT_BASIC_TOPIC, topic)
        client.subscribe(mqtt_topic)
        print("Subscribed to: " + mqtt_topic)

def on_message(client, userdata, message):
    message_payload = str(message.payload.decode("utf-8"))
    print(f"Received IoT Message: Topic: {message.topic} Payload: {message_payload}")

client_id = "python-greenhouse-consumer-{0}".format(MqttConfigurationParameters.MQTT_USERNAME)

mqtt_client = mqtt.Client(client_id)
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect

mqtt_client.username_pw_set(MqttConfigurationParameters.MQTT_USERNAME, MqttConfigurationParameters.MQTT_PASSWORD)

print("Connecting to " + MqttConfigurationParameters.BROKER_ADDRESS + " port: " + str(MqttConfigurationParameters.BROKER_PORT))
mqtt_client.connect(MqttConfigurationParameters.BROKER_ADDRESS, MqttConfigurationParameters.BROKER_PORT)

mqtt_client.loop_forever()
