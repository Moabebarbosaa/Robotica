import random

velIdeal = 500

cont = 0

while (cont < 100):

    carga = random.randint(1,50)

    erro = velIdeal/carga
    velocidade = carga*erro

    print (velocidade)

    cont += 1
