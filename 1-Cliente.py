#!/usr/bin/env python3
from time import sleep
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
            qtd = 400
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
            while sensorCorDireito.value() != verde:
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
            break

        else:
            andarSensoresquerdo()


def pegar_Boneco():
    # posicao_motor_D = motorDireito.position
    # posicao_motor_E = motorEsquerdo.position
    # motorEsquerdo.run_to_abs_pos(position_sp=posicao_motor_E - 150, speed_sp=200)
    # motorDireito.run_to_abs_pos(position_sp=posicao_motor_D - 150, speed_sp=200)
    cont = 0
    while cont <= 6:
        posicao_motor_D = motorDireito.position
        posicao_motor_E = motorEsquerdo.position
        if cont == 1 or cont == 5:
            qtd = 340
        elif cont == 2:
            qtd = 100
        elif cont == 4:
            qtd = 200

        if cont == 0:
            motorPorta.run_forever(speed_sp=-1000)
            sleep(2)
        elif cont == 1:
            motorDireito.run_to_abs_pos(position_sp=posicao_motor_D + 475, speed_sp=100)
            motorEsquerdo.run_to_abs_pos(position_sp=posicao_motor_E - 475, speed_sp=100)
            sleep(5)
        elif cont == 2:
            motorEsquerdo.run_to_abs_pos(position_sp=posicao_motor_E + 600, speed_sp=200)
            motorDireito.run_to_abs_pos(position_sp=posicao_motor_D + 600, speed_sp=200)
            sleep(2)
        elif cont == 3:
            motorPorta.run_forever(speed_sp=+1000)
            sleep(2)
        elif cont == 4:
            motorEsquerdo.run_to_abs_pos(position_sp=posicao_motor_E - 600, speed_sp=200)
            motorDireito.run_to_abs_pos(position_sp=posicao_motor_D - 600, speed_sp=200)
            sleep(2)
        elif cont == 5:
            motorDireito.run_to_abs_pos(position_sp=posicao_motor_D - 475, speed_sp=100)
            motorEsquerdo.run_to_abs_pos(position_sp=posicao_motor_E + 475, speed_sp=100)
            sleep(5)

        cont += 1


def andarSensoresquerdo():
    offset = 8
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
    global ultra

    offset = 28

    constProp = 50
    erro = offset - sensorInfraEsquerdo.value()

    giro = constProp * erro

    if sensorCorEsquerdo.value() == branco and sensorCorDireito.value() == branco and sensorInfraEsquerdo.value() < 22:
        andarSensorDireito()

    elif sensorCorEsquerdo.value() == preto:
        motorEsquerdo.run_forever(speed_sp=funcao_saturacao(500 - giro))
        motorDireito.run_forever(speed_sp=funcao_saturacao(500 + giro))

    else:
        motorEsquerdo.run_forever(speed_sp=funcao_saturacao(500 - giro))
        motorDireito.run_forever(speed_sp=funcao_saturacao(500 + giro))

def andarSensorDireito():
    offset = 29
    constProp = 50

    erro = offset - sensorInfraDireito.value()
    giro = erro * constProp

    motorEsquerdo.run_forever(speed_sp=funcao_saturacao(400 + giro))
    motorDireito.run_forever(speed_sp=funcao_saturacao(400 - giro))


def virarDireita():
    for i in range(400):
        andarSensorDireito()

def virarEsquerda():
    for i in range(400):
        andarSensorEsquerdo()


def alinhar(cor):

    while sensorCorEsquerdo.value() == cor or sensorCorDireito.value() == cor:

        if sensorCorDireito.value() != branco:
            motorDireito.run_forever(speed_sp=-80)
            motorEsquerdo.run_forever(speed_sp=80)

        if sensorCorEsquerdo.value() != branco:
            motorEsquerdo.run_forever(speed_sp=-80)
            motorDireito.run_forever(speed_sp=80)


def seguirFrente(cor):
    print("Seguir em frente!")

    alinhar(cor)
    for i in range(1000):
        motorDireito.run_forever(speed_sp=210)
        motorEsquerdo.run_forever(speed_sp=200)



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
        listaDeCor.append(sensorCorEsquerdo.value())

    return moda(listaDeCor)


def SaberLado(cor):

    contCor = 0
    contCorTotal = 0

    coresIndesejadas = [7, 6, 1, 0, 4]

    ultimaCOR = 0

    while True:
        corLida = sensorCorEsquerdo.value()
        andarSensorEsquerdo()

        if ultimaCOR == corLida and corLida != preto:
            if verificarCor() == ultimaCOR:
                return saberGiro(contCorTotal)

        if corLida != cor and corLida not in coresIndesejadas:
            if verificarCor() == corLida:
                return saberGiro(contCorTotal)

        while corLida == cor:
            andarSensorEsquerdo()
            corLida = sensorCorEsquerdo.value()
            contCor += 1
            ultimaCOR = cor

        if contCor > 1:
            contCorTotal += 1
            contCor = 0

        while corLida == preto or corLida == semCor:
            andarSensorEsquerdo()
            ultimaCOR = preto
            corLida = sensorCorEsquerdo.value()


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


def on_connect(client, userdata, flags, rc):
    client.subscribe([("topic/sensor/ultra", 0)])

def on_disconnect(client, userdata, rc=0):
    client.loop_stop()

def on_message(client, userdata, msg):
    global ultra

    if msg.topic == "topic/sensor/ultra":
        ultra = bool(msg.payload)


def main():

    global ultra

    indo_voltando = True

    corVermelha = ""
    corVerde = ""
    corAzul = ""

    contCores = 0

    try:
        client.on_connect = on_connect
        client.on_message = on_message
        client.loop_start()

        while True:
            # pegar_Boneco()
            # break
            corLida = sensorCorEsquerdo.value()

            print("ULTRA: ", ultra)

            print("Cor verde: ", corVerde)
            print("Cor vermelha: ", corVermelha)
            print("Cor azul: ", corAzul)
            print("Indo ou voltando: ", indo_voltando)
            print("Contador de Cores: ", contCores)

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
                    for i in range(100):
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
        motorPorta.stop()



client = mqtt.Client()
client.connect("169.254.214.223", 1883, 60)


motorEsquerdo = LargeMotor('outA')
motorDireito = LargeMotor('outC')
motorPorta = LargeMotor('outD')

ultra = False

sensorInfraEsquerdo = InfraredSensor("in1")
sensorInfraDireito = InfraredSensor("in2")

sensorCorEsquerdo = ColorSensor("in3")
sensorCorDireito = ColorSensor("in4")
sensorCorEsquerdo.mode = 'COL-COLOR'
sensorCorDireito.mode = 'COL-COLOR'

semCor, preto, azul, verde, vermelho, branco = 0, 1, 2, 3, 5, 6

if __name__ == '__main__':
    main()
