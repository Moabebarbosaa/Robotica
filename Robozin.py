#!/usr/bin/env python3
from ev3dev.ev3 import *


def funcao_saturacao(v):
    if v > 1000:
        return 1000
    elif v < -1000:
        return -1000
    else:
        return v

def andar():
    offset = 28
    constProp = 30

    erro = offset - sensorInfra.value()
    giro = erro * constProp

    motorA.run_forever(speed_sp=funcao_saturacao(250 - giro))
    motorB.run_forever(speed_sp=funcao_saturacao(250 + giro))

def moda(l):
    repeticoes = 0
    valor = 0
    for i in range(len(l)):
        aparicoes = l.count(l[i])
        if aparicoes > repeticoes:
            repeticoes = aparicoes
            valor = l[i]

    return valor

def transicaoCor():
    listaCor = []
    for i in range(50):
        corLida = sensorCor.color
        listaCor.append(corLida)
        motorA.run_forever(speed_sp=200)
        motorB.run_forever(speed_sp=200)

    MODA = moda(listaCor)
    return MODA

def virarDireita(motorA, motorB):
    for i in range(700):
        motorA.run_forever(speed_sp=200)
        motorB.run_forever(speed_sp=200)

    for i in range(500):
        motorA.run_forever(speed_sp=200)
        motorB.run_forever(speed_sp=-200)

    for i in range(500):
        motorA.run_forever(speed_sp=300)
        motorB.run_forever(speed_sp=300)

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



def saberGiro(contEsquerda):
    if contEsquerda == 1:
        return "Esquerda"
    elif contEsquerda == 2:
        return "Seguir"
    elif contEsquerda == 3:
        return "Direita"



def SaberLado(cor):

    contCor = 0
    contCorTotal = 0

    coresIndesejadas = [7, 6, 1, 0, 4]

    while True:
        corLida = sensorCor.color
        andar()

        while (corLida == cor):
            andar()
            corLida = sensorCor.color
            contCor += 1

        if contCor > 1:
            contCorTotal += 1
            contCor = 0
            print("ContCorTotal: ", contCorTotal)

        if (corLida != cor and corLida not in coresIndesejadas) or contCorTotal == 3:
            print("ENTROU AQUI: ", contCorTotal)
            print(corLida)
            break

    return saberGiro(contCorTotal)

def Acao(acao, motorA, motorB):
    if acao == "Seguir":
        seguirFrente(motorA, motorB)
    elif acao == "Direita":
        virarDireita(motorA, motorB)
    elif acao == "Esquerda":
        virarEsquerda(motorA, motorB)




motorA = LargeMotor('outA')
motorB = LargeMotor('outB')

sensorInfra = InfraredSensor("in1")

sensorCor = ColorSensor("in2")
MODE_COL_COLOR = 'COL-COLOR'

semCor, preto, azul, verde, vermelho, branco = 0, 1, 2, 3, 5, 6

corVermelha = ""
corVerde = ""
corAzul = ""

try:
    while True:

        corLida = sensorCor.color

        #print("Cor Lida: ", corLida)

        if (corLida == branco or corLida == preto):
            andar()

        elif (corLida != branco and corLida != preto):
            corTratada = transicaoCor()
            # print(corTratada)
            if (corTratada == azul):
                print("AZUL")
                if corAzul == "":
                    corAzul = SaberLado(azul)
                else:
                    Acao(corAzul, motorA, motorB)


            if (corTratada == verde):
                print("VERDE")
                if corVerde == "":
                    print("AQUI")
                    corVerde = SaberLado(verde)
                else:
                    Acao(corVerde, motorA, motorB)

            if (corTratada == vermelho):
                print("VERMELHO")
                if corVermelha == "":
                    corVermelha = SaberLado(vermelho)
                else:
                    Acao(corVermelha, motorA, motorB)

except KeyboardInterrupt:
    motorA.stop()
    motorB.stop()
