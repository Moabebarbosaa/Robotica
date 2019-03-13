#!/usr/bin/env python3
from ev3dev.ev3 import *


def sair_Quadrado():
    cont = 0
    while cont <= 4:
        posicao_motor_D = motorDireito.position
        posicao_motor_E = motorEsquerdo.position
        if cont == 0 or cont == 2 or cont == 4:
            qtd = 700
        elif cont == 1:
            qtd = 1000
        else:
            qtd = 500

        for i in range(qtd):
            if cont == 0 or cont == 2 or cont == 4:
                motorDireito.run_to_abs_pos(position_sp=posicao_motor_D - 600, speed_sp=100)
                motorEsquerdo.run_to_abs_pos(position_sp=posicao_motor_E + 600, speed_sp=100)
            elif cont == 1:
                motorEsquerdo.run_forever(speed_sp=300)
                motorDireito.run_forever(speed_sp=300)
            else:
                andarSensorEsquerdo(1)
        cont += 1

    while True:
        andarSensorEsquerdo(1)


def funcao_saturacao(v):
    if v > 1000:
        return 1000
    elif v < -1000:
        return -1000
    else:
        return v

def andarSensorEsquerdo(modo):
    if modo == 0:
        offset = 28
        constProp = 30

        erro = offset - sensorInfraEsquerdo.value()
        giro = erro * constProp

        motorEsquerdo.run_forever(speed_sp=funcao_saturacao(200 - giro))
        motorDireito.run_forever(speed_sp=funcao_saturacao(200 + giro))

    else:
        offset = 4
        constProp = 24

        erro = offset - sensorInfraEsquerdo.value()
        giro = erro * constProp

        if erro > 4:
            motorEsquerdo.run_forever(speed_sp=funcao_saturacao(100 + giro))
            motorDireito.run_forever(speed_sp=funcao_saturacao(1250 - giro))
        elif erro < 4:
            motorEsquerdo.run_forever(speed_sp=funcao_saturacao(200 + giro))
            motorDireito.run_forever(speed_sp=funcao_saturacao(200 - giro))
