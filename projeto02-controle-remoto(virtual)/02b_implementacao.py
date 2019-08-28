# importação de bibliotecas
from gpiozero import LED
from gpiozero import Button
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
from lirc import init, nextcode
from flask import Flask, redirect
from py_irsend.irsend import *
import threading

# criação do servidor
app = Flask(__name__)



# definição de funções das páginas
@app.route("/inicio")
def funcao_da_pagina_inicio():
    return "Funcionou!"

@app.route("/power")
def mostrar_pagina_liga_desliga():
    send_once("aquario", ["KEY_POWER"])
    return "(Des)Ligando a TV"

@app.route("/aumentaVolume")
def mostrar_pagina_aumentaVolume():
    send_once("aquario", ["KEY_VOLUMEUP"])
    
    return "Aumentando o volume"

@app.route("/diminuiVolume")
def mostrar_pagina_diminuiVolume():
    send_once("aquario", ["KEY_VOLUMEDOWN"])
    
    return "Diminuindo o volume"

@app.route("/mudo")
def mostrar_pagina_volumeMudo():
    send_once("aquario", ["KEY_MUTE"])
    
    return "Acionando o modo mudo"

@app.route("/canal/<string:canal>")
def imprimir_canal(canal):
    lista_comandos = ["KEY_0", "KEY_1", "KEY_2", "KEY_3", "KEY_4", "KEY_5", "KEY_6", "KEY_7", "KEY_8", "KEY_9"]
    canais = []
    for numero in canal:
        canais.append(lista_comandos[int(numero)])
        
    canais.append("KEY_OK")
    send_once("aquario", canais)
    
    return canal

@app.route("/dormir/<int:tempo>")
def sleepTime(tempo):
    timer = threading.Timer(tempo, mostrar_pagina_liga_desliga) 
    timer.start()
    
    return "Desligando em " + str(tempo) + " segundos"

# rode o servidor
app.run(port=5000)