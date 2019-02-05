#!/usr/bin/env python3
from ev3dev.ev3 import *

def moda(l):
    repeticoes = 0
    valor = 0
    for i in range(len(l)):
        aparicoes = l.count(l[i])
        if aparicoes > repeticoes:
            repeticoes = aparicoes
            valor = l[i]

    return valor

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

def addListaCor(cont):
    listaCor.append(corLida)
    print(listaCor)
    cont += 1

def setaDicionarioCores(dicioCores,qtdQueViraEsquerda,primeiraCor):

    if qtdQueViraEsquerda == 0:
        dicioCores[primeiraCor] = "E"
    elif qtdQueViraEsquerda == 1:
        dicioCores[primeiraCor] = "F"
    elif qtdQueViraEsquerda == 2:
        dicioCores[primeiraCor] = "D"
    return dicioCores

def contaPreto(qtdViraEsquerda):
    qtdViraEsquerda += 1
    print("CONTEI UM PRETO")
    return qtdQueViraEsquerda

def condicoesAPartirDicionario(dicioCores,listaCor):
    if dicioCores[moda(listaCor)] == "E":
        virarEsquerda(motorA, motorB)
    elif dicioCores[moda(listaCor)] == "D":
        virarDireita(motorA, motorB)
    elif dicioCores[moda(listaCor)] == "F":
        seguirFrente(motorA, motorB)
    return dicioCores

motorA = LargeMotor('outA')
motorB = LargeMotor('outB')

sensorInfra = InfraredSensor("in1")
sensorCor = ColorSensor("in2")
MODE_COL_COLOR = 'COL-COLOR'

semCor, preto, azul, verde, vermelho, branco = 0, 1, 2, 3, 5, 6
CoresValidas = []
dicioCores = {0: "", 1: "", 2: "", 3: "", 5: "", 6: ""}

corVermelha = "Esquerda"
corVerde = "Direita"
corAzul = "Seguir"

offset = 35
constProp = 30

qtdQueViraEsquerda = 0
achouACor = False

listaCor = [-1]
cont = 0
try:
    while True:
        erro = offset - sensorInfra.value()
        giro = erro * constProp

        corLida = sensorCor.color
        motorA.run_forever(speed_sp=funcao_saturacao(170 - giro))
        motorB.run_forever(speed_sp=funcao_saturacao(170 + giro))

        print("MODA: ", moda(listaCor))
#       print(sensorCor.color)

        # Tratamento de transição de cores

        # if corLida == semCor:
        #     re(motorA,motorB)
        print(cont)
        if cont < 10 and corLida != 6:
            listaCor.append(corLida)
            cont +=1

        elif corLida == 6:
            listaCor = [-1]
            cont = 0

        elif cont > 9:
            print ("=============ENTREI================= ")
            primeiraCor = moda(listaCor)

            if moda(listaCor) == preto:
                qtdQueViraEsquerda = contaPreto(qtdQueViraEsquerda)

            if moda(listaCor) != primeiraCor and moda(listaCor) != preto and moda(listaCor) != branco and moda(
                    listaCor) != semCor:
                setaDicionarioCores(dicioCores, qtdQueViraEsquerda,primeiraCor)

            print(dicioCores)
            # condicoesAPartirDicionario(dicioCores,listaCor)
            # print(setaDicionarioCores(dicioCores, qtdQueViraEsquerda,primeiraCor))


except KeyboardInterrupt:
    motorA.stop()
    motorB.stop()
