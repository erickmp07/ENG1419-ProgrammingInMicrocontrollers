from turtle import *

def definirPontoInicial(x, y):
    penup()
    goto(x, y)
    pendown()
    
def desenha_retangulo(x, y, comprimento, altura, cor):
    definirPontoInicial(x, y)
    fillcolor(cor)
    begin_fill()
    forward(comprimento)
    right(90)
    forward(altura)
    right(90)
    forward(comprimento)
    right(90)
    forward(altura)
    right(90)
    end_fill()
    return
    
    
def desenha_circulo(x, y, raio, cor):
    definirPontoInicial(x, y - raio)
    fillcolor(cor)
    begin_fill()
    circle(raio)
    end_fill()
    return
    
    
def desenha_poligono(lista_pontos, cor):
    x = lista_pontos[0]['x']
    y = lista_pontos[0]['y']
    
    definirPontoInicial(x, y)
    
    fillcolor(cor)
    begin_fill()
    
    for ponto in lista_pontos:
        x = ponto['x']
        y = ponto['y']
        
        goto(x, y)
        
    end_fill()
        
    return
    
    
# Bandeira 1
desenha_retangulo(0,    0, 33.3, 60, 'blue')
desenha_retangulo(33.3, 0, 33.3, 60, 'white')
desenha_retangulo(66.6, 0, 33.3, 60, 'red')


# Bandeira 2
desenha_retangulo(0, 130, 100, 20, 'orange')
desenha_retangulo(0, 110, 100, 20, 'white')
desenha_retangulo(0, 90,  100, 20, 'green')
desenha_circulo(50, 100, 10, 'orange')

# Bandeira 3
desenha_retangulo(0, 260, 100, 60, 'green')
desenha_poligono([{'x':50, 'y':255}, {'x':5, 'y':230}, {'x':50, 'y':205}, {'x':95, 'y':230}], 'yellow')
desenha_circulo(50, 230, 13, 'blue')