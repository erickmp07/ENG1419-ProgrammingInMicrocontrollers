# importação de bibliotecas
from Adafruit_CharLCD import Adafruit_CharLCD as LCD
from gpiozero import Button, LED, Buzzer
from os import system
from datetime import datetime
from time import sleep
from requests import post, get


# Mata todos os aplicativos "mplayer" e "arecord"
system("killall mplayer")
system("killall arecord")


# parâmetros iniciais do Telegram
chave = "891540592:AAGoSlJqM082CEdnFlnyWECJAd0qi5rTO84"
id_da_conversa = "39485402"
endereco_base = "https://api.telegram.org/bot" + chave
endereco_mensagem = endereco_base + "/sendMessage"
endereco_foto = endereco_base + "/sendPhoto"
endereco_updates = endereco_base + '/getUpdates'

# definição de funções
def ligar_campainha():
    buzzer.on()
    
def enviar_mensagem():
    buzzer.off()
    
    print("Enviando mensagem...\n")
    dados = {"chat_id": id_da_conversa, "text": "Tem alguém na porta!"}
    resposta = post(endereco_mensagem, json=dados)
    print("Mensagem enviada!\n")
    
    agora = datetime.now()
    hora = agora.strftime("%H:%M:%S")
    nome_arq = 'foto_' + hora + '.jpg'
    
    system("fswebcam --resolution 640x480 --skip 10 " + nome_arq)
    
    foto = {'photo': open(nome_arq, 'rb')}
    dados = {'chat_id': id_da_conversa}
    post(endereco_foto, data=dados, files=foto)
    

# criação de componentes
botao1 = Button(11)
botao2 = Button(12)

buzzer = Buzzer(16)

led1 = LED(21)

botao1.when_pressed = ligar_campainha
botao1.when_released = enviar_mensagem

botao2.when_pressed = led1.off

# loop infinito
ultimo_id = -1

while True:
    dados = {'offset': ultimo_id + 1}
    updates = get(endereco_updates, json=dados).json()
    
    if updates['ok']:
        result = updates['result']
        
        for r in result:
            texto = r['message']['text']
            if texto == 'Abrir':
                led1.on()
            elif texto == 'Alarme':
                buzzer.beep(n=5, on_time=0.05, off_time=0.1)
        
        if result != []:
            ultimo_id = result[-1]['update_id']
