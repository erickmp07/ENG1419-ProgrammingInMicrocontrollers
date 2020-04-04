# importação de bibliotecas
from Adafruit_CharLCD import Adafruit_CharLCD as LCD
from gpiozero import Button, LED, Buzzer, DistanceSensor
from os import system
from datetime import datetime, timedelta
from time import sleep
from requests import post, get
from subprocess import Popen
from urllib.request import urlretrieve
from mplayer import Player
import time

aplicativo = None
horaChegada = datetime.now()


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
endereco_voz = endereco_base + "/sendVoice"
endereco_get_file = endereco_base + "/getFile"

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
    
def enviar_audio():
    dados = {"chat_id": id_da_conversa}
    arquivo = {"voice": open("audio.ogg", "rb")}
    resposta = post(endereco, data=dados, files=arquivo)
    
def iniciar_gravacao():
    global aplicativo
    comando = ["arecord", "--duration", "30", "--format", "cd", "audio.wav"]
    aplicativo = Popen(comando)

def parar_gravacao():
    global aplicativo
    if aplicativo != None:
        aplicativo.terminate()
        aplicativo = None
        
    system("opusenc audio.wav audio.ogg")
    dados = {"chat_id": id_da_conversa}
    arquivo = {"voice": open("audio.ogg", "rb")}
    resposta = post(endereco_voz, data=dados, files=arquivo)
    
def pessoa_porta():
    global horaChegada
    horaChegada = datetime.now()
    print("In range")
    
def pessoa_saiu():
    global horaChegada
    print("Out of range")
    if (datetime.now() - horaChegada >= timedelta(seconds=10)):
        dados = {"chat_id": id_da_conversa, "text": "Pessoa saiu!"}
        resposta = post(endereco_mensagem, json=dados)
    

# criação de componentes
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
buzzer = Buzzer(16)

led1 = LED(21)

player = Player()

sensor = DistanceSensor(trigger=17, echo=18)
sensor.threshold_distance = 0.2

botao1.when_pressed = ligar_campainha
botao1.when_released = enviar_mensagem

botao2.when_pressed = led1.off

botao3.when_pressed = iniciar_gravacao
botao3.when_released = parar_gravacao

sensor.when_in_range = pessoa_porta
sensor.when_out_of_range = pessoa_saiu

# loop infinito
ultimo_id = -1

while True:
    dados = {'offset': ultimo_id + 1}
    updates = get(endereco_updates, json=dados).json()
    
    if updates['ok']:
        result = updates['result']
        
        for r in result:
            mensagem = r["message"]
            if ("text" in mensagem):
                texto = mensagem['text']
                if texto == 'Abrir':
                    led1.on()
                elif texto == 'Alarme':
                    buzzer.beep(n=5, on_time=0.05, off_time=0.1)
            elif ("voice" in mensagem):
                id_do_arquivo = mensagem["voice"]["file_id"]
                dados = {"file_id": id_do_arquivo}
                resposta = get(endereco_get_file, json=dados)
                dicionario = resposta.json()
                final_do_link = dicionario["result"]["file_path"]
                link_do_arquivo = "https://api.telegram.org/file/bot" + chave + "/" + final_do_link
                arquivo_de_destino = "audio-chat.ogg"
                urlretrieve(link_do_arquivo, arquivo_de_destino)
                player.loadfile(arquivo_de_destino)
        
        if result != []:
            ultimo_id = result[-1]['update_id']

