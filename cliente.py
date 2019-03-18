#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from ev3dev.ev3 import *
from sys import excepthook

ultra = False
MOTOR = LargeMotor("outA")

client = mqtt.Client()

client.connect("169.254.248.207", 1883, 60)

def exception_handle(exctype, value, tb):
    print("Type:", exctype)
    print("Value:", value)
    print("Traceback:", tb)

excepthook = exception_handle

def on_connect(client, userdata, flags, rc):
    client.subscribe([("topic/teste", 0)])

def on_disconnect(client, userdata, rc=0):
    client.loop_stop()

def on_message(client, userdata, msg):
    global ultra

    if msg.topic == "topic/teste":
        ultra = float(msg.payload)

def capturaSensor(valor):
    if int(valor) < 60:
        MOTOR.run_forever(speed_sp=200)
    elif int(valor) >= 60:
        MOTOR.stop()

def andar():
    global ultra

    print (ultra)

def main():

        client.on_connect = on_connect
        client.on_message = on_message
        client.loop_start()

        while True:
            andar()

if __name__ == '__main__':
    main()
