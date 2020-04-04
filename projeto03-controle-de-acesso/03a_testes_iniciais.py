# importação de bibliotecas
from gpiozero import Buzzer
from gpiozero import Button
from gpiozero import LED
from gpiozero import DistanceSensor
from Adafruit_CharLCD import Adafruit_CharLCD as LCD
from pymongo import MongoClient
from datetime import datetime
cliente=MongoClient("localhost",27017)
banco=cliente["Medidas"]
colecao=banco["itens"]

lcd=LCD(2,3,4,5,6,7,16,2)

led=LED(21)

sensor=DistanceSensor(trigger=17,echo=18)
sensor.threshold_distance=0.10

campainha=Buzzer(16)

botao1=Button(11)
botao2=Button(12)

# definição de funções
def tocaCampainha():
    campainha.beep(n=1,on_time=0.5)
def distance():
    led.blink(n=2)
def ex3():
    d=100*sensor.distance
    lcd.clear()
    lcd.message("%.1f cm" %d)
    documento={"distancia": d, "data/hora": datetime.now()}
    colecao.insert(documento)

# criação de componentes
botao1.when_pressed=tocaCampainha
botao2.when_pressed=ex3
sensor.when_in_range=distance
sensor.when_out_of_range=distance

