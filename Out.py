def sair_Quadrado():
    posicao_motor_D = motorDireito.position
    posicao_motor_E = motorEsquerdo.position

    for i in range(700):
        motorDireito.run_to_abs_pos(position_sp=posicao_motor_D-600, speed_sp=100)
        motorEsquerdo.run_to_abs_pos(position_sp=posicao_motor_E+600, speed_sp=100)
    print("Rodou")
    posicao_motor_D = motorDireito.position
    posicao_motor_E = motorEsquerdo.position

    for i in range(1000):
        motorEsquerdo.run_forever(speed_sp=300)
        motorDireito.run_forever(speed_sp=300)

    print("Frente")
    posicao_motor_D = motorDireito.position
    posicao_motor_E = motorEsquerdo.position

    for i in range(550):
        motorDireito.run_to_abs_pos(position_sp=posicao_motor_D-600, speed_sp=100)
        motorEsquerdo.run_to_abs_pos(position_sp=posicao_motor_E+600, speed_sp=100)

    print("Rodou")
    posicao_motor_D = motorDireito.position
    posicao_motor_E = motorEsquerdo.position

    for i in range(500):
        andarSensoresquerdo()

    print("sensor")
    posicao_motor_D = motorDireito.position
    posicao_motor_E = motorEsquerdo.position

    for i in range(550):
        motorDireito.run_to_abs_pos(position_sp=posicao_motor_D - 600, speed_sp=100)
        motorEsquerdo.run_to_abs_pos(position_sp=posicao_motor_E + 600, speed_sp=100)

    print("Rodou")
    posicao_motor_D = motorDireito.position
    posicao_motor_E = motorEsquerdo.position

    while True:
        andarSensoresquerdo()

    print("Sensor")
    posicao_motor_D = motorDireito.position
    posicao_motor_E = motorEsquerdo.position


def funcao_saturacao(v):
    if v > 1000:
        return 1000
    elif v < -1000:
        return -1000
    else:
        return v

