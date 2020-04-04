# importação de bibliotecas
from gpiozero import MotionSensor, LED, Button, LightSensor, DistanceSensor
from threading import Timer
from requests import post

timer = None

chave = "tA7BhqaWgXPjVTWV-br2e"
evento = "botao1_pressed"
endereco = "https://maker.ifttt.com/trigger/" + evento + "/with/key/" + chave

# definição de funções
def acender_led1():
    print("Moveu")
    led1.on()
    led2.on()
    
    global timer
    if (timer != None):
        timer.cancel()
        timer = None
    
def apagar_leds():
    print("Inércia")
    led1.off()
    
    global timer
    timer = Timer(8.0, apagar_led2)
    timer.start()
    
def apagar_led2():
    print("Apagar led 2")
    led2.off()
    
def botao1_pressionado():
    dados = {"value1": sensorLuz.value * 100, "value2" : sensorDistancia.distance*100 }
    resultado = post(endereco, json=dados)
    print(resultado.text)


# criação de componentes
led1 = LED(21)
led2 = LED(22)
botao1 = Button(11)
sensorMovimento = MotionSensor(27)
sensorLuz = LightSensor(8)
sensorDistancia = DistanceSensor(trigger=17, echo=18)

sensorMovimento.when_motion = acender_led1
sensorMovimento.when_no_motion = apagar_leds

botao1.when_pressed = botao1_pressionado


# loop infinito
