#!/usr/bin/env python3
from ev3dev.ev3 import *

def funcao_saturacao(v):
    if v > 1000:
        return 1000
    elif v < -1000:
        return -1000
    else:
        return v

def sair_Quadrado():
    cont = 0

    while sensorCorEsquerdo.value() != preto:
        motorEsquerdo.run_forever(speed_sp=200)
        motorDireito.run_forever(speed_sp=200)

    for i in range(500):
        motorEsquerdo.run_forever(speed_sp=200)
        motorDireito.run_forever(speed_sp=200)

    while cont <= 4:
        posicao_motor_D = motorDireito.position
        posicao_motor_E = motorEsquerdo.position
        if cont == 0 or cont == 2 or cont == 4:
            qtd = 500
        else:
            qtd = 1750

        for i in range(qtd):
            if cont == 0 or cont == 2 or cont == 4:
                motorDireito.run_to_abs_pos(position_sp=posicao_motor_D - 600, speed_sp=100)
                motorEsquerdo.run_to_abs_pos(position_sp=posicao_motor_E + 600, speed_sp=100)
            else:
                motorEsquerdo.run_forever(speed_sp=300)
                motorDireito.run_forever(speed_sp=300)
        if cont == 1 or cont == 3:
            for i in range(50):
                motorEsquerdo.run_forever(speed_sp=-200)
                motorDireito.run_forever(speed_sp=-200)
        cont += 1

    while True:
        if sensorCorEsquerdo.value() == verde:
            while sensorCorDireito.value()!= verde:
                motorDireito.run_forever(speed_sp=100)
                motorEsquerdo.run_forever(speed_sp=-20)
                if sensorCorDireito.value() == verde:
                    break

            alinhar(verde)
            # while sensorCorEsquerdo.value() != branco:
            #     motorEsquerdo.run_forever(speed_sp=-100)
            #     motorDireito.run_forever(speed_sp=20)

            while True:
                motorEsquerdo.stop()
                motorDireito.stop()

        else:
            andarSensoresquerdo()


def andarSensoresquerdo():
    offset =8
    constProp = 30

    erro = offset - sensorInfraEsquerdo.value()
    giro = erro * constProp

    if erro > 8:
        motorEsquerdo.run_forever(speed_sp=funcao_saturacao(100 + giro))
        motorDireito.run_forever(speed_sp=funcao_saturacao(1250 - giro))
    elif erro < 8:
        motorEsquerdo.run_forever(speed_sp=funcao_saturacao(200 + giro))
        motorDireito.run_forever(speed_sp=funcao_saturacao(200 - giro))


def andarSensorEsquerdo():
    offset = 30

    constProp = 30
    erro = offset - sensorInfraEsquerdo.value()

    giro = constProp * erro

    motorEsquerdo.run_forever(speed_sp=funcao_saturacao(200 - giro))
    motorDireito.run_forever(speed_sp=funcao_saturacao(200 + giro))

def andarSensorDireito():
    offset = 30
    constProp = 30

    erro = offset - sensorInfraDireito.value()
    giro = erro * constProp

    motorEsquerdo.run_forever(speed_sp=funcao_saturacao(200 + giro))
    motorDireito.run_forever(speed_sp=funcao_saturacao(200 - giro))


def virarDireita():
    for i in range(1000):
        andarSensorDireito()

def virarEsquerda():
    for i in range(600):
        andarSensorEsquerdo()

def alinhar(cor):
    while sensorCorDireito.value() == cor:
        if sensorCorDireito.color != branco:
            motorDireito.run_forever(speed_sp=-100)
            motorEsquerdo.run_forever(speed_sp=50)

        if sensorCorEsquerdo.color != branco:
            motorEsquerdo.run_forever(speed_sp=-100)
            motorDireito.run_forever(speed_sp=50)

    while sensorCorEsquerdo.value() == cor:
        if sensorCorDireito.color != branco:
            motorDireito.run_forever(speed_sp=-100)
            motorEsquerdo.run_forever(speed_sp=50)

        if sensorCorEsquerdo.color != branco:
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

    while True:
        corLida = sensorCorEsquerdo.color
        andarSensorEsquerdo()

        if ultimaCOR == corLida and corLida != preto:
            if verificarCor() == ultimaCOR:
                return saberGiro(contCorTotal)

        if corLida != cor and corLida not in coresIndesejadas:
            if verificarCor() == corLida:
                return saberGiro(contCorTotal)

        while corLida == cor:
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


def mudarSentidos(cor):
    if cor == "Seguir":
        return "Seguir"
    elif cor == "Esquerda":
        return "Direita"
    else:
        return "Esquerda"




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

contCores = 0


try:
    while True:

        sair_Quadrado()

        while True:
            motorEsquerdo.stop()

            motorDireito.stop()

        corLida = sensorCorEsquerdo.color

        if indo_voltando == True:
            if contCores == 6 and corLida == azul:
                seguirFrente(azul)
                print("AQUI")
                sair_Quadrado()
                indo_voltando = False
                print("AQUI 2")
                corAzul = mudarSentidos(corAzul)
                corVermelha = mudarSentidos(corVermelha)
                corVerde = mudarSentidos(corVerde)
                contCores = 0

        if indo_voltando == False:
            if contCores == 7:
                print("AQUI3")
                for i in range(500):
                    andarSensorEsquerdo()
                for i in range(900):
                    motorEsquerdo.run_forever(speed_sp=-250)
                    motorDireito.run_forever(speed_sp=250)

                indo_voltando = True
                corAzul = mudarSentidos(corAzul)
                corVermelha = mudarSentidos(corVermelha)
                corVerde = mudarSentidos(corVerde)
                contCores = 0

        if corLida == branco or corLida == preto:
            andarSensorEsquerdo()

        if corLida == azul:
            if corAzul == "":
                contCores += 1
                corAzul = SaberLado(azul)

            else:
                contCores += 1
                Acao(corAzul, azul)

        if corLida == verde:
            if corVerde == "":
                contCores += 1
                corVerde = SaberLado(verde)

            else:
                contCores += 1
                Acao(corVerde, verde)

        if corLida == vermelho:
            if corVermelha == "":
                contCores += 1
                corVermelha = SaberLado(vermelho)

            else:
                contCores += 1
                Acao(corVermelha, vermelho)

except KeyboardInterrupt:
    motorEsquerdo.stop()
    motorDireito.stop()
