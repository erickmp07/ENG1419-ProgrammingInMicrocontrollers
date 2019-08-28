# importação de bibliotecas
from gpiozero import LED
from gpiozero import Button
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
from lirc import init, nextcode
from flask import Flask, redirect, render_template
from py_irsend.irsend import *
from json import load
import threading

# criação do servidor
app = Flask(__name__)

lista_de_canais = load(open('templates/canais.json', encoding="UTF-8"))



# definição de funções das páginas
@app.route("/")
def funcao_da_pagina_inicio():
    return render_template("principal.html", lista_de_canais = lista_de_canais)

@app.route("/power")
def mostrar_pagina_liga_desliga():
    send_once("aquario", ["KEY_POWER"])
    return redirect("/")

@app.route("/aumentaVolume")
def mostrar_pagina_aumentaVolume():
    send_once("aquario", ["KEY_VOLUMEUP"])
    
    return redirect("/")

@app.route("/diminuiVolume")
def mostrar_pagina_diminuiVolume():
    send_once("aquario", ["KEY_VOLUMEDOWN"])
    
    return redirect("/")

@app.route("/mudo")
def mostrar_pagina_volumeMudo():
    send_once("aquario", ["KEY_MUTE"])
    
    return redirect("/")

@app.route("/canal/<string:canal>")
def imprimir_canal(canal):
    lista_comandos = ["KEY_0", "KEY_1", "KEY_2", "KEY_3", "KEY_4", "KEY_5", "KEY_6", "KEY_7", "KEY_8", "KEY_9"]
    canais = []
    for numero in canal:
        canais.append(lista_comandos[int(numero)])
        
    canais.append("KEY_OK")
    send_once("aquario", canais)
    
    return redirect("/")

@app.route("/dormir/<int:tempo>")
def sleepTime(tempo):
    timer = threading.Timer(tempo, mostrar_pagina_liga_desliga) 
    timer.start()
    
    return redirect("/")

# rode o servidor


app.run(port=5000)