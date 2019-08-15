from turtle import *

# Parte 1: desenhe o retângulo no topo
penup()
goto(-50, 200)
pendown()
forward(100)
right(90)
forward(50)
right(90)
forward(100)
right(90)
forward(50)
right(90)


# Parte 2: desenhe o triângulo equilátero à direita
penup()
goto(200, 0)
setheading(0)
pendown()

forward(100)
setheading(120)
forward(100)
setheading(240)
forward(100)



# Parte 3: desenhe o círculo na parte debaixo
penup()
goto(0, -200)
setheading(0)
pendown()

circle(60)


# Parte 4: desenhe a espiral na esquerda
penup()
goto(-200, 0)
setheading(0)
pendown()

for i in range(1, 100):

    forward(i * 3.1415 / 25)
    left(36 / 5)
    

# Parte 5: ao clicar em um ponto da tela, desenhe um texto com o valor das coordenadas x e y

def imprime_coordenadas(x, y):
    penup()
    goto(x, y)
    write("x = " + str(x) + ", y = " + str(y))
    
onscreenclick(imprime_coordenadas)