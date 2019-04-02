#!/usr/bin/env python3

from ev3dev.ev3 import *
import paho.mqtt.client as mqtt


ultrassonico = UltrasonicSensor('in1')

client = mqtt.Client()
client.connect("localhost", 1883, 60)


def on_disconnect(client, userdata, rc=0):
    client.loop_stop()

client.on_disconnect = on_disconnect

distanciaPermitida = 25


while True:
    ultrassonicoAtual = ultrassonico.value() / 10

    if ultrassonicoAtual <= distanciaPermitida:
        client.publish(topic="topic/sensor/ultra", payload=True, qos=0, retain=False)
