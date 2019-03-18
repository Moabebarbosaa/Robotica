#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from ev3dev.ev3 import *
# import Queue
from sys import excepthook

ultra = False
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

        # print(ultra)
        ultra = float(msg.payload)
        # print (ultra)

def capturaSensor(valor):
    if int(valor) < 60:
        MOTOR.run_forever(speed_sp=200)
    elif int(valor) >= 60:
        MOTOR.stop()

def andar():
    global ultra
    # capturaSensor(ultra)
    # if ultra == True:
    #     print ("legal")

    print (ultra)

def main():

        # print(ultra)
        client.on_connect = on_connect
        client.on_message = on_message
        client.loop_start()

        while True:
            andar()



if __name__ == '__main__':
    main()
