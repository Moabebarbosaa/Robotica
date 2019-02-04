#!/usr/bin/env python3
from ev3dev.ev3 import *
import statistics

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

    for i in range(300):
        motorA.run_forever(speed_sp=300)
        motorB.run_forever(speed_sp=300)

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

semCor = 0
preto = 1
azul = 2
verde = 3
vermelho = 5
branco = 6



corVermelha = "Esquerda"
corVerde = "Direita"
corAzul = "Seguir"

offset = 28
constProp = 30


qtdQueViraEsquerda = 0
achouACor = False

listaCor = [-1]


try:
    while True:
        erro = offset - sensorInfra.value()
        giro = erro * constProp

        corLida = sensorCor.color
        motorA.run_forever(speed_sp=funcao_saturacao(170 - giro))
        motorB.run_forever(speed_sp=funcao_saturacao(170 + giro))

        print("MODA: ", statistics.mode(listaCor))
#        print(sensorCor.color)

        if listaCor != 6:
            listaCor.append(corLida)
            print (listaCor)

        if statistics.mode(listaCor) != verde and statistics.mode(listaCor) != preto and statistics.mode(listaCor) != branco and statistics.mode(listaCor) != semCor:
            achouACor = True

            if qtdQueViraEsquerda == 1:
                corVerde = "Esquerda"
            elif qtdQueViraEsquerda == 2:
                corVerde = "Frente"
            elif qtdQueViraEsquerda == 3:
                corVerde = "Direita"
            listaCor = [-1]

        elif statistics.mode(listaCor) == verde and achouACor == False:
            print("cor: ", sensorCor.color)
            virarEsquerda(motorA, motorB)
            qtdQueViraEsquerda += 1
            listaCor = [-1]


        if statistics.mode(listaCor) == verde and corVerde == "Esquerda" and achouACor == True:
            virarEsquerda(motorA, motorB)
            listaCor = [-1]
        if statistics.mode(listaCor) == verde and corVerde == "Direita" and achouACor == True:
            virarDireita(motorA, motorB)
            listaCor = [-1]
        if statistics.mode(listaCor) == verde and corVerde == "Frente" and achouACor == True:
            seguirFrente(motorA, motorB)
            listaCor = [-1]
      #  print("Achou cor: " + str(achouACor)+ " Cor lida: "+ str(corLida) + "Sensor infra: "+ str(sensorInfra.value()))

except KeyboardInterrupt:
    motorA.stop()
    motorB.stop()
