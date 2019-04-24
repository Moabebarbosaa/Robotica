#!/usr/bin/env python3

from time import sleep
from ev3dev.ev3 import *
import paho.mqtt.client as mqtt
from os import system


ultrassonico = UltrasonicSensor('in1')

client = mqtt.Client()
client.connect("localhost", 1883, 60)


def on_disconnect(client, userdata, rc=0):
    client.loop_stop()

client.on_disconnect = on_disconnect

distanciaPermitida = 20
botao = Button()

# print("\n\n\n\n\n\n\n\n\n\n   ----- Botao do meio para iniciar -----")
# while True:
#     if botao.enter:
#         system("clear")
#         break

chave = False

while True:
    ultrassonicoAtual = ultrassonico.value() / 10
    chave = False
    # if botao.enter:
    #     print("\n\n\n\n\n\n\n\n\n\n   ----- Iniciou novamente -----")
    #     system("clear")


    if ultrassonicoAtual <= distanciaPermitida and chave == False:
        client.publish(topic="topic/sensor/ultra", payload=True, qos=0, retain=False)
        print("TEM BONECO")
        chave = True
        sleep(1)

        # system("clear")
