from json import load
from turtle import *

# Copie as funções da Implementação aqui
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

# Implemente a função abaixo
def desenha_bandeira(dicionario_do_pais):
    elementos = dicionario_do_pais['elementos']
    for elemento in elementos:
        if (elemento['tipo'] == 'retângulo'):
            desenha_retangulo(elemento['x'], elemento['y'], elemento['comprimento'], elemento['altura'], elemento['cor'])
        
        elif (elemento['tipo'] == 'círculo'):
            desenha_circulo(elemento['x'], elemento['y'], elemento['raio'], elemento['cor'])
            
        elif (elemento['tipo'] == 'polígono'):
            desenha_poligono(elemento['pontos'], elemento['cor'])
        
        else:
            write('Erro: Bandeira não encontrada.')
        
    return

dicionarios_de_paises = load(open('paises.json', encoding="UTF-8"))
desenha_bandeira(dicionarios_de_paises[0])


# Ao clicar na tela, solicitar o nome de um país, busque-o na lista de dicionários de países e desenhe-o.
def escolherBandeira(x, y):
    definirPontoInicial(x, y)
    bandeira = textinput('Seleção de bandeira','Digite o nome de uma bandeira:')
    
    for pais in dicionarios_de_paises:
        if (pais['nome'] != bandeira):
            continue
        
        desenha_bandeira(pais)
        break

onscreenclick(escolherBandeira)



# Por fim, adicione uma nova bandeira no arquivo JSON e teste seu desenho.