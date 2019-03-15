#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from ev3dev.ev3 import *
from sys import excepthook

ultra = 1500

MOTOR = LargeMotor("outA")

client = mqtt.Client()

client.connect("10.42.0.243", 1883, 60)


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
        ultra = int(msg.payload)

def andar():
    print (ultra)

def main():

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()

    while True:
        andar()


if __name__ == '__main__':
    main()
