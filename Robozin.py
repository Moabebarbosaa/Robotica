#!/usr/bin/env python3
from ev3dev.ev3 import *

motorA = LargeMotor('outA')
motorB = LargeMotor('outB')

# motorA.run_forever(speed_sp=200)
# motorB.run_forever(speed_sp=200)

# sensor = UltrasonicSensor('in4')

# giroscopio = GyroSensor('in1')
# giroscopio.mode = 'GYRO-ANG'
# unidades = giroscopio.units

# units = sensor.units

sensorInfra = InfraredSensor("in1")


def funcao_saturacao(v):
    if v > 1000:
        return 1000
    elif v < -1000:
        return -1000
    else:
        return v


offset = 28
constProp = 50

try:
    while True:
        erro = offset - sensorInfra.value()
        giro = erro * constProp

        motorA.run_forever(speed_sp=funcao_saturacao(170 - giro))
        motorB.run_forever(speed_sp=funcao_saturacao(170 + giro))
except KeyboardInterrupt:
    motorA.stop()
    motorB.stop()

# verificar quando faz a curva perto da borda (esta caindo). precisa controlar isso!!


# while(True):
#
#     distancia = sensor.value() / 10
#     angle = giroscopio.value()
#
#     if distancia < 20:
#         giro = 0
#         ang_anterior = giroscopio.value()
#         while giro < 90:
#             giro = ang_anterior - giroscopio.value()
#             print(giro, ang_anterior, giroscopio.value())
#             motorA.run_forever(speed_sp=-200)
#             motorB.run_forever(speed_sp=200)
#
#
#     else:
#         motorA.run_forever(speed_sp=200)
#         motorB.run_forever(speed_sp=200)
#
#
#     print(str(angle))
#     print(str(distancia) + " " + units)
