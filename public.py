#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from ev3dev.ev3 import *

ultra = UltrasonicSensor("in1")

#  This is the Publisher

while True:
        client = mqtt.Client()
        client.connect("localhost",1883,60)
        client.publish(topic="topic/test", payload=ultra.value(),qos=1,retain=False)
