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

    motorEsquerdo.run_forever(speed_sp=funcao_saturacao(200 - giro))
    motorDireito.run_forever(speed_sp=funcao_saturacao(200 + giro))

def andarSensorDireito():
    offset = 28
    constProp = 24

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
    while sensorCorDireito.value() != branco:
        if sensorCorDireito.color == cor:
            motorDireito.run_forever(speed_sp=-100)
            motorEsquerdo.run_forever(speed_sp=50)

        if sensorCorEsquerdo.color == cor:
            motorEsquerdo.run_forever(speed_sp=-100)
            motorDireito.run_forever(speed_sp=50)

    while sensorCorEsquerdo.value() != branco:
        if sensorCorDireito.color == cor:
            motorDireito.run_forever(speed_sp=-100)
            motorEsquerdo.run_forever(speed_sp=50)

        if sensorCorEsquerdo.color == cor:
            motorEsquerdo.run_forever(speed_sp=-100)
            motorDireito.run_forever(speed_sp=50)

def seguirFrente(cor):
    print("SSSSSS")
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

        if ultimaCOR == corLida:
            if verificarCor() == ultimaCOR:
                #print("ULTIMA COR == COR LIDA:", contCorTotal)
                return saberGiro(contCorTotal)

        if corLida != cor and corLida not in coresIndesejadas:
            if verificarCor() == corLida:
                #print("ENTROU AQUI: ", contCorTotal)
                return saberGiro(contCorTotal)

        while (corLida == cor):
            andarSensorEsquerdo()
            corLida = sensorCorEsquerdo.color
            contCor += 1
            ultimaCOR = cor

        if contCor > 1:
            contCorTotal += 1
            contCor = 0
            #print("ContCorTotal: ", contCorTotal)

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

giroscopio = GyroSensor("in3")
giroscopio.mode = 'GYRO-ANG'

semCor, preto, azul, verde, vermelho, branco = 0, 1, 2, 3, 5, 6

corVermelha = ""
corVerde = ""
corAzul = ""

anglo = 0

try:
    while True:

        corLida = sensorCorEsquerdo.color

        if corLida == branco or corLida == preto:
            andarSensorEsquerdo()

        if corLida == azul:
            if corAzul == "":
                corAzul = SaberLado(azul)
                anglo = giroscopio.value()
            else:
                Acao(corAzul, azul)
                anglo = giroscopio.value()

        if corLida == verde:
            if corVerde == "":
                corVerde = SaberLado(verde)
                anglo = giroscopio.value()
            else:
                Acao(corVerde, verde)
                anglo = giroscopio.value()

        if corLida == vermelho:
            if corVermelha == "":
                corVermelha = SaberLado(vermelho)
                anglo = giroscopio.value()
            else:
                Acao(corVermelha, vermelho)
                anglo = giroscopio.value()

        

except KeyboardInterrupt:
    motorEsquerdo.stop()
    motorDireito.stop()
