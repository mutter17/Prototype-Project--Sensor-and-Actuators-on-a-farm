from smart_objects.humidity_sensor import HumiditySensor
from smart_objects.irrigation_system import IrrigationSystem
from smart_objects.light_sensor import LightSensor
from smart_objects.shade_system import ShadeSystem

class Greenhouse:
    def __init__(self, client):
        self.client = client
        self.irrigation_system = IrrigationSystem(client)
        self.humidity_sensor = HumiditySensor(client)
        self.light_sensor = LightSensor(client)
        self.shade_system = ShadeSystem(client)
