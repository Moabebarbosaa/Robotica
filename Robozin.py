#!/usr/bin/env python3
from ev3dev.ev3 import *

def virarDireita(motorA, motorB):
    for i in range(700):
        motorA.run_forever(speed_sp=200)
        motorB.run_forever(speed_sp=200)

    for i in range(500):
        motorA.run_forever(speed_sp=200)
        motorB.run_forever(speed_sp=-200)

    for i in range(500):
        motorA.run_forever(speed_sp=200)
        motorB.run_forever(speed_sp=200)

def seguirFrente(motorA, motorB):
    for i in range(1500):
        motorA.run_forever(speed_sp=200)
        motorB.run_forever(speed_sp=200)

def virarEsquerda(motorA, motorB):
    for i in range(700):
        motorA.run_forever(speed_sp=200)
        motorB.run_forever(speed_sp=200)

    for i in range(500):
        motorA.run_forever(speed_sp=-200)
        motorB.run_forever(speed_sp=200)

    for i in range(500):
        motorA.run_forever(speed_sp=200)
        motorB.run_forever(speed_sp=200)

def saberCor():

    return 0



def funcao_saturacao(v):
    if v > 1000:
        return 1000
    elif v < -1000:
        return -1000
    else:
        return v



motorA = LargeMotor('outA')
motorB = LargeMotor('outB')

sensorInfra = InfraredSensor("in1")
sensorCor = ColorSensor("in2")
MODE_COL_COLOR = 'COL-COLOR'

branco, preto, azul, verde, vermelho = 6, 1, 2, 3, 5

acoes = {"acaoVermelho": seguirFrente(motorA, motorB), "acaoVerde": virarEsquerda(motorA, motorB), "acaoAzul": virarEsquerda(motorA, motorB)}


offset = 28
constProp = 30

try:
    while True:
        erro = offset - sensorInfra.value()
        giro = erro * constProp

        corLida = sensorCor.color

        motorA.run_forever(speed_sp=funcao_saturacao(170 - giro))
        motorB.run_forever(speed_sp=funcao_saturacao(170 + giro))



        if str(corLida) == str(vermelho):
            seguirFrente(motorA, motorB)
        if str(corLida) == str(verde):
            virarDireita(motorA, motorB)
        if str(corLida) == str(azul):
            virarEsquerda(motorA, motorB)


        print("valor = " + str(corLida))

except KeyboardInterrupt:
    motorA.stop()
    motorB.stop()
