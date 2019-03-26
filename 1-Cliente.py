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

    while sensorCorEsquerdo != preto:
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
        if sensorCorEsquerdo == verde:
            while sensorCorDireito!= verde:
                motorDireito.run_forever(speed_sp=100)
                motorEsquerdo.run_forever(speed_sp=30)
                if sensorCorDireito == verde:
                    break
            while sensorCorDireito != vermelho:
                motorDireito.run_forever(speed_sp=100)
                motorEsquerdo.run_forever(speed_sp=30)

            while sensorCorDireito != azul:
                motorDireito.run_forever(speed_sp=100)


            seguirFrente(azul)
            break

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
    offset = 28

    constProp = 50
    erro = offset - sensorInfraEsquerdo.value()

    giro = constProp * erro
    if sensorCorEsquerdo == preto:
        motorEsquerdo.run_forever(speed_sp=funcao_saturacao(500 - giro))
        motorDireito.run_forever(speed_sp=funcao_saturacao(500 + giro))
    else:
        motorEsquerdo.run_forever(speed_sp=funcao_saturacao(400 - giro))
        motorDireito.run_forever(speed_sp=funcao_saturacao(400 + giro))

def andarSensorDireito():
    offset = 29
    constProp = 50

    erro = offset - sensorInfraDireito.value()
    giro = erro * constProp

    motorEsquerdo.run_forever(speed_sp=funcao_saturacao(400 + giro))
    motorDireito.run_forever(speed_sp=funcao_saturacao(400 - giro))


def virarDireita():
    for i in range(500):
        andarSensorDireito()

def virarEsquerda():
    for i in range(600):
        andarSensorEsquerdo()


def alinhar(cor):

    global sensorCorEsquerdo, sensorCorDireito

    while sensorCorEsquerdo == cor or sensorCorDireito == cor:

        if sensorCorDireito != branco:
            motorDireito.run_forever(speed_sp=-80)
            motorEsquerdo.run_forever(speed_sp=80)

        if sensorCorEsquerdo != branco:
            motorEsquerdo.run_forever(speed_sp=-80)
            motorDireito.run_forever(speed_sp=80)

    # while True:
    #     motorDireito.stop()
    #     motorEsquerdo.stop()

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

    global sensorCorEsquerdo, sensorCorDireito

    listaDeCor = []

    for i in range(20):
        motorEsquerdo.run_forever(speed_sp=100)
        motorDireito.run_forever(speed_sp=100)
        listaDeCor.append(sensorCorEsquerdo)

    return moda(listaDeCor)


def SaberLado(cor):

    global sensorCorEsquerdo, sensorCorDireito

    contCor = 0
    contCorTotal = 0

    coresIndesejadas = [7, 6, 1, 0, 4]

    ultimaCOR = 0

    while True:
        corLida = sensorCorEsquerdo
        andarSensorEsquerdo()

        if ultimaCOR == corLida and corLida != preto:
            if verificarCor() == ultimaCOR:
                return saberGiro(contCorTotal)

        if corLida != cor and corLida not in coresIndesejadas:
            if verificarCor() == corLida:
                return saberGiro(contCorTotal)

        while corLida == cor:
            andarSensorEsquerdo()
            corLida = sensorCorEsquerdo
            contCor += 1
            ultimaCOR = cor

        if contCor > 1:
            contCorTotal += 1
            contCor = 0

        while corLida == preto or corLida == semCor:
            andarSensorEsquerdo()
            ultimaCOR = preto
            corLida = sensorCorEsquerdo


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
    client.subscribe([ ("topic/sensor/color1", 0), ("topic/sensor/color2", 0)])

def on_disconnect(client, userdata, rc=0):
    client.loop_stop()

def on_message(client, userdata, msg):
    global sensorCorEsquerdo, sensorCorDireito

    if msg.topic == "topic/sensor/color1":
        sensorCorEsquerdo = int(msg.payload)
    if msg.topic == "topic/sensor/color2":
        sensorCorDireito = int(msg.payload)

client = mqtt.Client()
client.connect("169.254.166.54", 1883, 60)


motorEsquerdo = LargeMotor('outA')
motorDireito = LargeMotor('outB')
motorTampa = LargeMotor('outC')


giroscopio = GyroSensor('in1')
ultrassonico = UltrasonicSensor('in2')


sensorInfraEsquerdo = InfraredSensor("in3")
sensorInfraDireito = InfraredSensor("in4")


semCor, preto, azul, verde, vermelho, branco = 0, 1, 2, 3, 5, 6

sensorCorEsquerdo = ColorSensor.COLOR_WHITE
sensorCorDireito = ColorSensor.COLOR_WHITE


def main():

    global sensorCorEsquerdo, sensorCorDireito

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

            print ()

            corLida = sensorCorEsquerdo

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
        motorTampa.stop()

if __name__ == '__main__':
    main()
