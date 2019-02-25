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

    if sensorCorEsquerdo.color == 1 or sensorCorEsquerdo.color == 0:
        constProp = 30

    else:
        constProp = 24

    giro = erro * constProp

    motorEsquerdo.run_forever(speed_sp=funcao_saturacao(300 - giro))
    motorDireito.run_forever(speed_sp=funcao_saturacao(300 + giro))

def andarSensorDireito():
    offset = 28
    constProp = 24

    erro = offset - sensorInfraDireito.value()
    giro = erro * constProp

    motorEsquerdo.run_forever(speed_sp=funcao_saturacao(300 + giro))
    motorDireito.run_forever(speed_sp=funcao_saturacao(300 - giro))

def virarDireita():
    for i in range(1000):
        andarSensorDireito()

def virarEsquerda():
    for i in range(500):
        andarSensorEsquerdo()

def seguirFrente():
    while (sensorCorEsquerdo.color != branco) or (sensorCorDireito.color != branco):

        if sensorCorDireito.color == vermelho:
            motorDireito.run_forever(speed_sp=-150)
            motorEsquerdo.run_forever(speed_sp=100)
            print("Sensor Direito: ", sensorCorDireito.color)

        if sensorCorEsquerdo.color == vermelho:
            motorEsquerdo.run_forever(speed_sp=-150)
            motorDireito.run_forever(speed_sp=100)
            print("Sensor esquerdo: ", sensorCorEsquerdo.color)

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

    while True:
        corLida = sensorCorEsquerdo.color
        andarSensorEsquerdo()

        while (corLida == cor):
            andarSensorEsquerdo()
            corLida = sensorCorEsquerdo.color
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

def mudarDirecao(acao):
    if acao == "Esquerda":
        return "Direita"
    elif acao == "Direita":
        return "Esquerda"
    else:
        return "Seguir"



def Acao(acao):
    if acao == "Seguir":
        seguirFrente()
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
MODE_COL_COLOR = 'COL-COLOR'

semCor, preto, azul, verde, vermelho, branco = 0, 1, 2, 3, 5, 6

corVermelha = ""
corVerde = ""
corAzul = ""

cont = 0

try:
    while True:

        corLida = sensorCorEsquerdo.color

        if corLida == branco or corLida == preto:
            andarSensorEsquerdo()

        if corLida == azul:
            if corAzul == "":
                cont += 1
                corAzul = SaberLado(azul)
            else:
                cont += 1
                Acao(corAzul)

        if corLida == verde:
            if corVerde == "":
                cont += 1
                corVerde = SaberLado(verde)
            else:
                cont += 1
                Acao(corVerde)

        if corLida == vermelho:
            if corVermelha == "":
                cont += 1
                corVermelha = SaberLado(vermelho)
            else:
                cont +=1
                Acao(corVermelha)

        if cont == 6:
            corVermelha = mudarDirecao(corVermelha)
            corVerde = mudarDirecao(corVerde)
            corAzul = mudarDirecao(corAzul)
            cont = 0

            for i in range(800):
                motorEsquerdo.run_forever(speed_sp=300)
                motorDireito.run_forever(speed_sp=-300)

        print("COnt: ", cont)

except KeyboardInterrupt:
    motorEsquerdo.stop()
    motorDireito.stop()
