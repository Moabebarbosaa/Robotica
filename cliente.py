#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from ev3dev.ev3 import *

motor = LargeMotor("outA")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/test")

def on_disconnect(client, userdata, rc=0):
    client.loop_stop()

def printalegal():
    print ("legal")

def capturaSensor(valor):
    if int(valor) < 60:
        motor.run_forever(speed_sp=200)
    elif int (valor) >= 60:
        motor.stop()


def on_message(client, userdata, msg):
    # global test
    # teste = str(msg.payload.decode())
    print (msg.payload.decode())
    capturaSensor(msg.payload)

    printalegal()



client = mqtt.Client()
client.connect("169.254.154.65",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
