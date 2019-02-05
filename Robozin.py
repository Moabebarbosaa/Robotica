#!/usr/bin/env python3
from ev3dev.ev3 import *

def moda(l):
    repeticoes = 0
    valor = 0
    for i in range(len(l)):
        aparicoes = l.count(l[i])
        if aparicoes > repeticoes:
            repeticoes = aparicoes
            valor = l[i]

    return valor

def virarDireita(motorA, motorB):
    for i in range(700):
        motorA.run_forever(speed_sp=200)
        motorB.run_forever(speed_sp=200)

    for i in range(500):
        motorA.run_forever(speed_sp=200)
        motorB.run_forever(speed_sp=-200)

    for i in range(500):
        motorA.run_forever(speed_sp=200)
        motorB.run_forever(speed_sp=200)

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

def saberCor():

    return 0

def funcao_saturacao(v):
    if v > 1000:
        return 1000
    elif v < -1000:
        return -1000
    else:
        return v

motorA = LargeMotor('outA')
motorB = LargeMotor('outB')

sensorInfra = InfraredSensor("in1")
sensorCor = ColorSensor("in2")
MODE_COL_COLOR = 'COL-COLOR'

semCor, preto, azul, verde, vermelho, branco = 0, 1, 2, 3, 5, 6

corVermelha = "Esquerda"
corVerde = "Direita"
corAzul = "Seguir"

offset = 28
constProp = 30

qtdQueViraEsquerda = 0
achouACor = False

listaCor = [-1]
cont = 0
try:
    while True:
        erro = offset - sensorInfra.value()
        giro = erro * constProp

        corLida = sensorCor.color
        motorA.run_forever(speed_sp=funcao_saturacao(170 - giro))
        motorB.run_forever(speed_sp=funcao_saturacao(170 + giro))

        print("MODA: ", moda(listaCor))
#       print(sensorCor.color)

        # Tratamento de transição de cores
        
        if cont < 10 and corLida != 6:
            listaCor.append(corLida)
            print (listaCor)
            cont += 1

        elif cont >= 10:
            if moda(listaCor) != verde and moda(listaCor) != preto and moda(listaCor) != branco and moda(listaCor) != semCor:
                print("-------------------------------ENTREI AQUI 1------------------------")
                achouACor = True

                if qtdQueViraEsquerda == 1:
                    corVerde = "Esquerda"
                    print("-------------------------------ENTREI AQUI 6------------------------")
                elif qtdQueViraEsquerda == 2:
                    corVerde = "Frente"
                    print("-------------------------------ENTREI AQUI 7------------------------")
                elif qtdQueViraEsquerda == 3:
                    corVerde = "Direita"
                    print("-------------------------------ENTREI AQUI 8------------------------")
                listaCor = [-1]

            elif moda(listaCor) == verde and achouACor == False:
                print ("-------------------------------ENTREI AQUI 2------------------------")
                print("cor: ", sensorCor.color)
                virarEsquerda(motorA, motorB)
                qtdQueViraEsquerda += 1
                listaCor = [-1]


            if moda(listaCor) == verde and corVerde == "Esquerda" and achouACor == True:
                print("-------------------------------ENTREI AQUI 3------------------------")
                virarEsquerda(motorA, motorB)
                listaCor = [-1]
            if moda(listaCor) == verde and corVerde == "Direita" and achouACor == True:
                print("-------------------------------ENTREI AQUI 4------------------------")
                virarDireita(motorA, motorB)
                listaCor = [-1]
            if moda(listaCor) == verde and corVerde == "Frente" and achouACor == True:
                print("-------------------------------ENTREI AQUI 5------------------------")
                seguirFrente(motorA, motorB)
                listaCor = [-1]
            cont = 0
        elif corLida == 6:
            listaCor = [-1]
          #  print("Achou cor: " + str(achouACor)+ " Cor lida: "+ str(corLida) + "Sensor infra: "+ str(sensorInfra.value()))

except KeyboardInterrupt:
    motorA.stop()
    motorB.stop()
