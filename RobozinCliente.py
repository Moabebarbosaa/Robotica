#!/usr/bin/env python3
from ev3dev.ev3 import *
import paho.mqtt.client as mqtt
from time import sleep

# def funcao_saturacao(v):
#     if v > 1000:
#         return 1000
#     elif v < -1000:
#         return -1000
#     else:
#         return v
#
#
# def andarSensorEsquerdo():
#     offset = 28
#
#     constProp = 30
#     erro = offset - sensorInfraEsquerdo.value()
#
#     giro = erro * constProp
#
#     motorEsquerdo.run_forever(speed_sp=funcao_saturacao(250 - giro))
#     motorDireito.run_forever(speed_sp=funcao_saturacao(250 + giro))
#
#
# def andarSensorDireito():
#     offset = 28
#     constProp = 30
#
#     erro = offset - sensorInfraDireito.value()
#     giro = erro * constProp
#
#     motorEsquerdo.run_forever(speed_sp=funcao_saturacao(200 + giro))
#     motorDireito.run_forever(speed_sp=funcao_saturacao(200 - giro))
#
#
# def virarDireita():
#     for i in range(1200):
#         andarSensorDireito()
#
#
# def virarEsquerda():
#     for i in range(600):
#         andarSensorEsquerdo()
#
#
# def alinhar(cor):
#     while sensorCorDireito.value() == cor:
#         if sensorCorDireito.color == cor:
#             motorDireito.run_forever(speed_sp=-100)
#             motorEsquerdo.run_forever(speed_sp=50)
#
#         if sensorCorEsquerdo.color == cor:
#             motorEsquerdo.run_forever(speed_sp=-100)
#             motorDireito.run_forever(speed_sp=50)
#
#     while sensorCorEsquerdo.value() == cor:
#         if sensorCorDireito.color == cor:
#             motorDireito.run_forever(speed_sp=-100)
#             motorEsquerdo.run_forever(speed_sp=50)
#
#         if sensorCorEsquerdo.color == cor:
#             motorEsquerdo.run_forever(speed_sp=-100)
#             motorDireito.run_forever(speed_sp=50)
#
#
# def seguirFrente(cor):
#     print("Seguir em frente!")
#     alinhar(cor)
#     for i in range(900):
#         motorEsquerdo.run_forever(speed_sp=300)
#         motorDireito.run_forever(speed_sp=300)
#
#
# def saberGiro(cont):
#     if cont == 1:
#         return "Esquerda"
#     elif cont == 2:
#         return "Seguir"
#     elif cont == 3:
#         return "Direita"
#
#
# def moda(l):
#     repeticoes = 0
#     valor = 0
#     for i in range(len(l)):
#         aparicoes = l.count(l[i])
#         if aparicoes > repeticoes:
#             repeticoes = aparicoes
#             valor = l[i]
#
#     return valor
#
#
# def verificarCor():
#     listaDeCor = []
#
#     for i in range(20):
#         motorEsquerdo.run_forever(speed_sp=100)
#         motorDireito.run_forever(speed_sp=100)
#         listaDeCor.append(sensorCorEsquerdo.color)
#
#     return moda(listaDeCor)
#
#
# def SaberLado(cor):
#     contCor = 0
#     contCorTotal = 0
#
#     coresIndesejadas = [7, 6, 1, 0, 4]
#
#     ultimaCOR = 0
#
#     global constanteGiroscopio
#
#     while True:
#         corLida = sensorCorEsquerdo.color
#         andarSensorEsquerdo()
#
#         if ultimaCOR == corLida:
#             if verificarCor() == ultimaCOR:
#                 return saberGiro(contCorTotal)
#
#         if corLida != cor and corLida not in coresIndesejadas:
#             if verificarCor() == corLida:
#                 return saberGiro(contCorTotal)
#
#         while (corLida == cor):
#             andarSensorEsquerdo()
#             corLida = sensorCorEsquerdo.color
#             contCor += 1
#             ultimaCOR = cor
#
#         if contCor > 1:
#             contCorTotal += 1
#             contCor = 0
#
#         while corLida == preto or corLida == semCor:
#             andarSensorEsquerdo()
#             ultimaCOR = preto
#             corLida = sensorCorEsquerdo.color
#
#
# def Acao(acao, cor):
#     if acao == "Seguir":
#         seguirFrente(cor)
#     elif acao == "Direita":
#         virarDireita()
#     elif acao == "Esquerda":
#         virarEsquerda()

def on_connect(client, userdata, flags, rc):
    client.subscribe([("topic/teste", 0)])

def on_disconnect(client, userdata, rc=0):
    client.loop_stop()

def on_message(client, userdata, msg):
    global ultra

    if msg.topic == "topic/teste":
        ultra = bool(msg.payload)


client = mqtt.Client()
client.connect("169.254.67.197", 1883, 60)





# motorEsquerdo = LargeMotor('outA')
# motorDireito = LargeMotor('outB')
motorBoneco = LargeMotor('outB')

# sensorInfraEsquerdo = InfraredSensor("in1")
# sensorInfraDireito = InfraredSensor("in3")
#
# sensorCorEsquerdo = ColorSensor("in2")
# sensorCorDireito = ColorSensor("in4")
# sensorCorEsquerdo.mode = 'COL-COLOR'
# sensorCorDireito.mode = 'COL-COLOR'

semCor, preto, azul, verde, vermelho, branco = 0, 1, 2, 3, 5, 6

indo_voltando = True

ultra = False

contCoresAzul = 0
primeiraCorLida = 0

def andar():
    global ultra
    for i in range(100):
        motorBoneco.run_forever(speed_sp=200)
    for i in range(100):
        motorBoneco.run_forever(speed_sp=-200)
    ultra = False
    motorBoneco.stop()

def main():

    global ultra
    corVermelha = ""
    corVerde = ""
    corAzul = ""

    cont = 0

    try:
        client.on_connect = on_connect
        client.on_message = on_message
        client.loop_start()


        while True:
        #
        #     corLida = sensorCorEsquerdo.color
        #
        #     if corLida == branco or corLida == preto:
        #         andarSensorEsquerdo()
        #
        #     if corLida == azul:
        #         if corAzul == "":
        #             cont += 1
        #             corAzul = SaberLado(azul)
        #         else:
        #             cont += 1
        #             Acao(corAzul, azul)
        #
        #     if corLida == verde:
        #         if corVerde == "":
        #             corVerde = SaberLado(verde)
        #             cont += 1
        #         else:
        #             cont += 1
        #             Acao(corVerde, verde)
        #
        #     if corLida == vermelho:
        #         if corVermelha == "":
        #             cont += 1
        #             corVermelha = SaberLado(vermelho)
        #         else:
        #             cont += 1
        #             Acao(corVermelha, vermelho)
        #
        #     if contCoresAzul == 7:
        #         print("FINAL")
        #         for i in range(600):
        #             motorEsquerdo.run_forever(speed_sp=200)
        #             motorDireito.run_forever(speed_sp=200)
            print(ultra)
            if ultra == True:
                andar()



            # sleep(1)




    except KeyboardInterrupt:
        # motorEsquerdo.stop()
        # motorDireito.stop()
        motorBoneco.stop()

if __name__ == '__main__':
    main()
