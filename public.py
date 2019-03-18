#!/usr/bin/env python3

from ev3dev.ev3 import UltrasonicSensor, ColorSensor, Button
from os import system
import paho.mqtt.client as mqtt

# Sensores ultrasonicos
ULTRA1 = UltrasonicSensor("in1")

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.loop_start()

DISTANCIA_BONECOS = 20


def on_disconnect(client, userdata, rc=0):
    client.loop_stop()


client.on_disconnect = on_disconnect

while True:
    distancia1 = ULTRA1.value() / 10

    if distancia1 <= DISTANCIA_BONECOS:
        client.publish(topic="topic/teste", payload=distancia1, qos=0, retain=False)
