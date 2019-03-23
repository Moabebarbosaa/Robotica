#!/usr/bin/env python3
from ev3dev.ev3 import *
import paho.mqtt.client as mqtt

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
                motorEsquerdo.run_forever(speed_sp=30)
                if sensorCorDireito.value() == verde:
                    break
            while sensorCorDireito.value() != vermelho:
                motorDireito.run_forever(speed_sp=100)
                motorEsquerdo.run_forever(speed_sp=30)

            while sensorCorDireito.value() != azul:
                motorDireito.run_forever(speed_sp=100)


            seguirFrente(azul)


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
    offset = 31

    constProp = 50
    erro = offset - sensorInfraEsquerdo.value()

    giro = constProp * erro

    if ultra == True:
        levantaMotorBoneco()

    if sensorCorEsquerdo.value() == preto:
        motorEsquerdo.run_forever(speed_sp=funcao_saturacao(300 - giro))
        motorDireito.run_forever(speed_sp=funcao_saturacao(300 + giro))
    else:
        motorEsquerdo.run_forever(speed_sp=funcao_saturacao(400 - giro))
        motorDireito.run_forever(speed_sp=funcao_saturacao(400 + giro))

def andarSensorDireito():
    offset = 28
    constProp = 50

    erro = offset - sensorInfraDireito.value()
    giro = erro * constProp

    motorEsquerdo.run_forever(speed_sp=funcao_saturacao(400 + giro))
    motorDireito.run_forever(speed_sp=funcao_saturacao(400 - giro))


def virarDireita():
    for i in range(1000):
        andarSensorDireito()

def virarEsquerda():
    for i in range(600):
        andarSensorEsquerdo()

def alinhar(cor):
    while sensorCorEsquerdo.value() == cor:
        print(11111)
        if sensorCorDireito.value() != branco:
            motorDireito.run_forever(speed_sp=-100)
            motorEsquerdo.run_forever(speed_sp=50)

        if sensorCorEsquerdo.value() != branco:
            motorEsquerdo.run_forever(speed_sp=-100)
            motorDireito.run_forever(speed_sp=50)

    while sensorCorDireito.value() == cor:
        print(2222222)
        if sensorCorDireito.value() != branco:
            motorDireito.run_forever(speed_sp=-100)
            motorEsquerdo.run_forever(speed_sp=50)

        if sensorCorEsquerdo.value() != branco:
            motorEsquerdo.run_forever(speed_sp=-100)
            motorDireito.run_forever(speed_sp=50)

def seguirFrente(cor):
    print("Seguir em frente!")

    for i in range(150):
        motorEsquerdo.run_forever(speed_sp=-300)
        motorDireito.run_forever(speed_sp=-300)

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

def levantaMotorBoneco():
    global ultra
    for i in range(100):
        motorBoneco.run_forever(speed_sp=200)
    for i in range(300):
        motorBoneco.run_forever(speed_sp=-200)
    ultra = False
    motorBoneco.stop()

def on_connect(client, userdata, flags, rc):
    client.subscribe([("topic/teste", 0)])

def on_disconnect(client, userdata, rc=0):
    client.loop_stop()

def on_message(client, userdata, msg):
    global ultra

    if msg.topic == "topic/teste":
        ultra = bool(msg.payload)

client = mqtt.Client()
client.connect("169.254.113.121", 1883, 60)

motorEsquerdo = LargeMotor('outA')
motorDireito = LargeMotor('outB')
motorBoneco = LargeMotor('outD')

sensorInfraEsquerdo = InfraredSensor("in1")
sensorInfraDireito = InfraredSensor("in3")

sensorCorEsquerdo = ColorSensor("in2")
sensorCorDireito = ColorSensor("in4")
sensorCorEsquerdo.mode = 'COL-COLOR'
sensorCorDireito.mode = 'COL-COLOR'

semCor, preto, azul, verde, vermelho, branco = 0, 1, 2, 3, 5, 6

indo_voltando = True

ultra = False

def main():

    global ultra
    global indo_voltando

    corVermelha = ""
    corVerde = ""
    corAzul = ""

    contCores = 0

    try:

        client.on_connect = on_connect
        client.on_message = on_message
        client.loop_start()

        while True:

            print(ultra)


            corLida = sensorCorEsquerdo.color

            print("Cor verde: ", corVerde)
            print("Cor vermelha: ", corVermelha)
            print("Cor azul: ", corAzul)


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
        motorBoneco.stop()

if __name__ == '__main__':
    main()
