#!/usr/bin/env python3

from ev3dev.ev3 import ColorSensor
import paho.mqtt.client as mqtt


sensorCorEsquerdo = ColorSensor("in1")
sensorCorDireito = ColorSensor("in2")
sensorCorEsquerdo.mode = 'COL-COLOR'
sensorCorDireito.mode = 'COL-COLOR'


client = mqtt.Client()
client.connect("localhost", 1883, 60)

cor_anterior1 = ""
cor_anterior2 = ""

def on_disconnect(client, userdata, rc=0):
    client.loop_stop()

client.on_disconnect = on_disconnect



while True:
    cor_atual1 = sensorCorEsquerdo.value()
    cor_atual2 = sensorCorDireito.value()

    if cor_atual1 != cor_anterior1:
        client.publish(topic="topic/sensor/color1", payload=cor_atual1, qos=0, retain=False)
        cor_anterior1 = cor_atual1
    if cor_atual2 != cor_anterior2:
        client.publish(topic="topic/sensor/color2", payload=cor_atual2, qos=0, retain=False)
        cor_anterior2 = cor_atual2
