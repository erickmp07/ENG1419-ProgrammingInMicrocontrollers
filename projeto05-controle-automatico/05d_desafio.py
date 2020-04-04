# importação de bibliotecas
from gpiozero import LED, Button, LightSensor
from flask import Flask
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta
from threading import Timer
from requests import post

# criação do servidor
app = Flask(__name__)

cliente = MongoClient("localhost", 27017)
banco = cliente["estados"]
colecao = banco["estadosLEDs"]

timer = None

chave = "tA7BhqaWgXPjVTWV-br2e"
evento = "escrever_planilha"
endereco = "https://maker.ifttt.com/trigger/" + evento + "/with/key/" + chave


# definição de funções das páginas
def salvar_estados():
    dados = {"data": datetime.now(), "estadosLEDs": [leds[0].is_lit, leds[1].is_lit, leds[2].is_lit, leds[3].is_lit, leds[4].is_lit]}
    print(dados)
    colecao.insert(dados)


@app.route("/luz/<int:led>/<string:modo>")
def muda(led,modo):
    if modo == "on":
        leds[led-1].on()
    if modo == "off":
        leds[led-1].off()
    
    salvar_estados()
    return ("ok")

def toggle():
    leds[0].toggle()
    salvar_estados()
    
def toggle1():
    leds[1].toggle()
    salvar_estados()
    
def toggle2():
    leds[2].toggle()
    salvar_estados()
    
def toggle3():
    leds[3].toggle()
    salvar_estados()
    
def acender_led5():
    leds[4].on()
    salvar_estados()
    
def apagar_led5():
    leds[4].off()
    salvar_estados()

@app.route("/estados")
def buscar_ultimo_estado():
    ordenacao = [ ["data", DESCENDING] ]
    documento = colecao.find_one(sort=ordenacao)
    
    html = "<ul>"
    registro = documento["estadosLEDs"]
    i = 1
    for estado in registro:
        html = html + "<li>Luz " + str(i)
        if (estado == True):
            html = html + ": aceso </li>"
        else:
            html = html + ": apagado </li>"
            
        i = i + 1
        
    html = html + "</ul>"
    
    return html

def calcular_total_segundos(numeroLED, data):
    busca = {"data" : {"$gte" : data}}
    ordenacao = [ ["data", ASCENDING] ]
    documentos = list (colecao.find(busca, sort=ordenacao))
    
    busca = {"data" : {"$lt" : data}}
    ordenacao = [ ["data", DESCENDING] ]
    documento = colecao.find_one(busca, sort=ordenacao)
    
    total_segundos = 0
    
    dataBanco = None
    estadoLED = None
    novaData = None
    novoEstado = None
    
    # Trato data anterior à data de pesquisa
    if (documento != None):
            dataBanco = data
            estadoLED = documento["estadosLEDs"][numeroLED-1]
            novaData = dataBanco
            novoEstado = estadoLED
    
    for registro in documentos:
        # Trato só ter um registro desde 1 minuto atrás
        if (dataBanco == None):
            dataBanco = registro["data"]
            estadoLED = registro["estadosLEDs"][numeroLED-1]
            novaData = dataBanco
            novoEstado = estadoLED
            continue
        
        novaData = registro["data"]
        novoEstado = registro["estadosLEDs"][numeroLED-1]
        
        # Trato registros desde 1 minuto atrás
        if (estadoLED == True):
            total_segundos = total_segundos + (novaData - dataBanco).total_seconds()
        
        dataBanco = novaData
        estadoLED = novoEstado
        
    # Trato última referência de data (anterior pesquisa ou última entre 1 minuto
    if (novoEstado == True):
        total_segundos = total_segundos + (datetime.now() - novaData).total_seconds()
        
    return total_segundos

def calcular_tempo_aceso_leds():
    umMinutoAtras = (datetime.now() - timedelta(minutes=1))
    tempos = ""
    for i in range(1, 6):
        tempos = tempos + str(calcular_total_segundos(i, umMinutoAtras)) + "|||"
        
    dados = {"value1": str(umMinutoAtras), "value2" : tempos }
    print(dados)
    resultado = post(endereco, json=dados)
    print(resultado.text)
    
def timer_recorrente():
    calcular_tempo_aceso_leds()
    global timer
    timer = Timer(30, timer_recorrente)
    timer.start()
    
    
# criação dos componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]
botoes[0].when_pressed=toggle
botoes[1].when_pressed=toggle1
botoes[2].when_pressed=toggle2
botoes[3].when_pressed=toggle3
sensorLuz=LightSensor(8)
sensorLuz.when_dark=acender_led5
sensorLuz.when_light=apagar_led5


# rode o servidor
timer_recorrente()

app.run(port=5000)


timer_recorrente()
