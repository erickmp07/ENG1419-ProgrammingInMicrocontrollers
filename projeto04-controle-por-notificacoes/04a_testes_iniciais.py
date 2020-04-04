# importação de bibliotecas
from Adafruit_CharLCD import Adafruit_CharLCD as LCD
from gpiozero import Button, LED
from os import system
from datetime import datetime
from time import sleep
from requests import post

# parâmetros iniciais do Telegram
chave = "891540592:AAGoSlJqM082CEdnFlnyWECJAd0qi5rTO84"
id_da_conversa = "39485402"
endereco_base = "https://api.telegram.org/bot" + chave
endereco = endereco_base + "/sendMessage"


# definição de funções
def iniciarGravacao():
    lcd.message("Gravando...")
    system("arecord --duration 5 --format cd 4a.wav")
    lcd.clear()
    
def tirarFotos():
    for i in range(5):
        data = datetime.now()
        led1.blink(n=1, on_time=0.3)
        system("fswebcam --resolution 640x480 --skip 10 foto-" + data.strftime("%H:%M:%S") + ".jpg")
        sleep(0.5)
        
def enviarMensagem():
    print("Enviando mensagem...\n")
    dados = {"chat_id": id_da_conversa, "text": "Hello World!"}
    resposta = post(endereco, json=dados)
    print("Mensagem enviada!\n")

# criação de componentes
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
lcd = LCD(2,3,4,5,6,7,16,2)
led1 = LED(21)

botao1.when_pressed = iniciarGravacao
botao2.when_pressed = tirarFotos
botao3.when_pressed = enviarMensagem