# importação de bibliotecas
from gpiozero import LED, Button, LightSensor
from flask import Flask


# criação do servidor
app = Flask(__name__)

@app.route("/luz/<int:led>/<string:modo>")


# definição de funções das páginas
@app.route("/luz/<int:led>/<string:modo>")
def muda(led,modo):
    if modo == "on":
        leds[led-1].on()
    if modo == "off":
        leds[led-1].off()
    return ("ok")

def toggle():
    leds[0].toggle()
def toggle1():
    leds[1].toggle()
def toggle2():
    leds[2].toggle()
def toggle3():
    leds[3].toggle()
# criação dos componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]
botoes[0].when_pressed=toggle
botoes[1].when_pressed=toggle1
botoes[2].when_pressed=toggle2
botoes[3].when_pressed=toggle3
sensorLuz=LightSensor(8)
sensorLuz.when_dark=leds[4].on
sensorLuz.when_light=leds[4].off


# rode o servidor
app.run(port=5000)