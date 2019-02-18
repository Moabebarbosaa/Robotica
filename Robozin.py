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

    erro = offset - sensorInfraEsquerdo.value()

    if sensorCor.color == 1 or sensorCor.color == 0:
        constProp = 30

    else:
        constProp = 24

    giro = erro * constProp

    motorA.run_forever(speed_sp=funcao_saturacao(300 - giro))
    motorB.run_forever(speed_sp=funcao_saturacao(300 + giro))


def andarSensorDireito():
    offset = 28
    constProp = 24

    erro = offset - sensorInfraDireito.value()
    giro = erro * constProp

    motorA.run_forever(speed_sp=funcao_saturacao(300 + giro))
    motorB.run_forever(speed_sp=funcao_saturacao(300 - giro))


def virarDireita():
    for i in range(1000):
        andarSensorDireito()


def virarEsquerda():
    for i in range(500):
        andarSensorEsquerdo()



def seguirFrente():
    corLida = sensorCor.color

    rotacao = (57-sensorInfraEsquerdo.value())*6


    while corLida != semCor:
        motorA.run_forever(speed_sp=-100)
        corLida = sensorCor.color

    for i in range(rotacao-3):
        motorB.run_forever(speed_sp=-200)
        motorA.run_forever(speed_sp=200)

    for i in range(850):
        motorB.run_forever(speed_sp=200)
        motorA.run_forever(speed_sp=200)


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
        motorA.run_forever(speed_sp=100)
        motorB.run_forever(speed_sp=100)
        listaDeCor.append(sensorCor.color)

    return moda(listaDeCor)


def SaberLado(cor):
    contCor = 0
    contCorTotal = 0

    coresIndesejadas = [7, 6, 1, 0, 4]

    while True:
        corLida = sensorCor.color
        andarSensorEsquerdo()

        while (corLida == cor):
            andarSensorEsquerdo()
            corLida = sensorCor.color
            contCor += 1

        if contCor > 1:
            contCorTotal += 1
            contCor = 0
            print("ContCorTotal: ", contCorTotal)

        if (corLida != cor and corLida not in coresIndesejadas) or contCorTotal == 3:
            if verificarCor() == corLida:
                print("ENTROU AQUI: ", contCorTotal)
                print("COR LIDAAAA: ", corLida)
                break

    return saberGiro(contCorTotal)


def Acao(acao):
    if acao == "Seguir":
        seguirFrente()
    elif acao == "Direita":
        virarDireita()
    elif acao == "Esquerda":
        virarEsquerda()


motorA = LargeMotor('outA')  # Esquerdo
motorB = LargeMotor('outB')  # Direito

sensorInfraEsquerdo = InfraredSensor("in1")
sensorInfraDireito = InfraredSensor("in3")

sensorCor = ColorSensor("in2")
MODE_COL_COLOR = 'COL-COLOR'

semCor, preto, azul, verde, vermelho, branco = 0, 1, 2, 3, 5, 6

corVermelha = ""
corVerde = ""
corAzul = ""

try:
    while True:

        corLida = sensorCor.color

        if corLida == branco or corLida == preto:
            andarSensorEsquerdo()

        if corLida == azul:
            print("AZUL")
            if corAzul == "":
                corAzul = SaberLado(azul)
            else:
                Acao(corAzul)

        if corLida == verde:
            print("VERDE")
            if corVerde == "":
                print("AQUI")
                corVerde = SaberLado(verde)
            else:
                Acao(corVerde)

        if corLida == vermelho:
            print("VERMELHO")
            if corVermelha == "":
                corVermelha = SaberLado(vermelho)
            else:
                Acao(corVermelha)



except KeyboardInterrupt:
    motorA.stop()
    motorB.stop()
