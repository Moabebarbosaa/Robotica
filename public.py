#!/usr/bin/env python3

from ev3dev.ev3 import UltrasonicSensor
import paho.mqtt.client as mqtt

# Sensor ultrasonico
ULTRA1 = UltrasonicSensor("in1")

client = mqtt.Client()
client.connect("localhost", 1883, 60)

def on_disconnect(client, userdata, rc=0):
    client.loop_stop()

client.on_disconnect = on_disconnect

while True:
    distancia1 = ULTRA1.value() / 10

    client.publish(topic="topic/teste", payload=distancia1, qos=0, retain=False)
