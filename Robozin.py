#!/usr/bin/env python3
from ev3dev.ev3 import *


def funcao_saturacao(v):
    if v > 1000:
        return 1000
    elif v < -1000:
        return -1000
    else:
        return v

def andarSensorEsquerdo():
    offset = 28

    constProp = 30
    erro = offset - sensorInfraEsquerdo.value()

    giro = erro * constProp

    motorEsquerdo.run_forever(speed_sp=funcao_saturacao(250 - giro))
    motorDireito.run_forever(speed_sp=funcao_saturacao(250 + giro))

def andarSensorDireito():
    offset = 28
    constProp = 30

    erro = offset - sensorInfraDireito.value()
    giro = erro * constProp

    motorEsquerdo.run_forever(speed_sp=funcao_saturacao(200 + giro))
    motorDireito.run_forever(speed_sp=funcao_saturacao(200 - giro))



def virarDireita():
    for i in range(1200):
        andarSensorDireito()

def virarEsquerda():
    for i in range(600):
        andarSensorEsquerdo()

def alinhar(cor):
    while sensorCorDireito.value() == cor:
        if sensorCorDireito.color == cor:
            motorDireito.run_forever(speed_sp=-100)
            motorEsquerdo.run_forever(speed_sp=50)

        if sensorCorEsquerdo.color == cor:
            motorEsquerdo.run_forever(speed_sp=-100)
            motorDireito.run_forever(speed_sp=50)

    while sensorCorEsquerdo.value() == cor:
        if sensorCorDireito.color == cor:
            motorDireito.run_forever(speed_sp=-100)
            motorEsquerdo.run_forever(speed_sp=50)

        if sensorCorEsquerdo.color == cor:
            motorEsquerdo.run_forever(speed_sp=-100)
            motorDireito.run_forever(speed_sp=50)

def seguirFrente(cor):
    print("Seguir em frente!")
    alinhar(cor)
    for i in range(900):
        motorEsquerdo.run_forever(speed_sp=300)
        motorDireito.run_forever(speed_sp=300)


def saberGiro(cont):
    if cont == 1:
        return "Esquerda"
    elif cont == 2:
        return "Seguir"
    elif cont == 3:
        return "Direita"

def moda(l):
    repeticoes = 0
    valor = 0
    for i in range(len(l)):
        aparicoes = l.count(l[i])
        if aparicoes > repeticoes:
            repeticoes = aparicoes
            valor = l[i]

    return valor

def verificarCor():
    listaDeCor = []

    for i in range(20):
        motorEsquerdo.run_forever(speed_sp=100)
        motorDireito.run_forever(speed_sp=100)
        listaDeCor.append(sensorCorEsquerdo.color)

    return moda(listaDeCor)

def SaberLado(cor):
    contCor = 0
    contCorTotal = 0

    coresIndesejadas = [7, 6, 1, 0, 4]

    ultimaCOR = 0

    global constanteGiroscopio

    while True:
        corLida = sensorCorEsquerdo.color
        andarSensorEsquerdo()

        if ultimaCOR == corLida:
            if verificarCor() == ultimaCOR:
                return saberGiro(contCorTotal)

        if corLida != cor and corLida not in coresIndesejadas:
            if verificarCor() == corLida:
                return saberGiro(contCorTotal)

        while (corLida == cor):
            andarSensorEsquerdo()
            corLida = sensorCorEsquerdo.color
            contCor += 1
            ultimaCOR = cor

        if contCor > 1:
            contCorTotal += 1
            contCor = 0

        while corLida == preto or corLida == semCor:
            andarSensorEsquerdo()
            ultimaCOR = preto
            corLida = sensorCorEsquerdo.color

def Acao(acao, cor):
    if acao == "Seguir":
        seguirFrente(cor)
    elif acao == "Direita":
        virarDireita()
    elif acao == "Esquerda":
        virarEsquerda()


motorEsquerdo = LargeMotor('outA')
motorDireito = LargeMotor('outB')

sensorInfraEsquerdo = InfraredSensor("in1")
sensorInfraDireito = InfraredSensor("in3")

sensorCorEsquerdo = ColorSensor("in2")
sensorCorDireito = ColorSensor("in4")
sensorCorEsquerdo.mode = 'COL-COLOR'
sensorCorDireito.mode = 'COL-COLOR'

semCor, preto, azul, verde, vermelho, branco = 0, 1, 2, 3, 5, 6

corVermelha = ""
corVerde = ""
corAzul = ""


indo_voltando = True



contCoresAzul = 0
primeiraCorLida = 0


try:
    while True:

        corLida = sensorCorEsquerdo.color

        if corLida == branco or corLida == preto:
            andarSensorEsquerdo()

        if corLida == azul:
            if corAzul == "":
                contCoresAzul += 1
                corAzul = SaberLado(azul)
                if primeiraCorLida == 0:
                    primeiraCorLida = azul
            else:
                contCoresAzul += 1
                Acao(corAzul, azul)

        if corLida == verde:
            if corVerde == "":
                corVerde = SaberLado(verde)
                if primeiraCorLida == 0:
                    primeiraCorLida = azul
            else:
                contCoresAzul += 1
                Acao(corVerde, verde)

        if corLida == vermelho:
            if corVermelha == "":
                corVermelha = SaberLado(vermelho)
                if primeiraCorLida == 0:
                    primeiraCorLida = azul
            else:
                Acao(corVermelha, vermelho)


        # if indo_voltando == True:
        #     if contCoresAzul == 3:
        #         print("FINAL")
        #         for i in range(600):
        #             motorEsquerdo.run_forever(speed_sp=200)
        #             motorDireito.run_forever(speed_sp=200)


except KeyboardInterrupt:
    motorEsquerdo.stop()
    motorDireito.stop()
