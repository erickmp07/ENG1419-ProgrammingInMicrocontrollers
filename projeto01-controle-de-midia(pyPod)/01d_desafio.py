# COMECE COPIANDO AQUI O SEU CÓDIGO DO APERFEIÇOAMENTO
# DEPOIS FAÇA OS NOVOS RECURSOS# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS
# importação de bibliotecas
from os import system
from gpiozero import LED, Button
from Adafruit_CharLCD import Adafruit_CharLCD
from mplayer import Player
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
import math
import random

# para de tocar músicas que tenham ficado tocando da vez passada
system("killall mplayer")


# definição de funções
def tocarPausarMusica():
    player.pause();
    definirStatusPlayer();
    
def definirStatusPlayer():
    if (player.paused):
        led1.blink();
    else:
        led1.on();

def avancarMusica():
    if (player.speed != 2):
        player.pt_step(1);
        
    player.speed = 1;
    global inicio;
    global fim;
    inicio = 0;
    fim = 16;
    
def acelerarMusica():
    player.speed = 2;
    
def voltarFaixa():
    if(player.time_pos < 2):
        player.pt_step(-1)
    else:
        player.time_pos = 0
        
    global inicio;
    global fim;
    inicio = 0;
    fim = 16;
    

def exibirFaixa():
    metadados = player.metadata
    if(metadados == None):
        return;
    
    faixa = player.metadata["Title"]
    lcd.clear()
    lcd.message(faixa[inicio:fim])
    minutos = math.trunc(player.time_pos / 60);
    segundos = player.time_pos % 60;
    tempoTotalMin = math.trunc(player.length / 60);
    tempoTotalSec = player.length % 60;
    lcd.message("\n" +
                '{:02.0f}:{:02.0f}'.format(minutos, segundos) +
                " de " +
                '{:02.0f}:{:02.0f}'.format(tempoTotalMin, tempoTotalSec))
    rolarTexto(len(faixa));
    
def rolarTexto(tamanhoFaixa):
    if (tamanhoFaixa < 16):
        return;
    
    global inicio;
    global fim;
    
    inicio +=1;
    fim += 1;
        
    if (inicio > tamanhoFaixa):
        inicio = 0;
        fim = 16;

def gerarPlaylist():
    file = open("playlist.txt", "r")
    newPlaylist = file.read().split("\n")
    random.shuffle(newPlaylist)
    newFile = open("novaPlaylist.txt", "w")
    for musica in newPlaylist:
        if(len(musica) > 0):
            newFile.write(musica + "\n")
			
	file.close();
	newFile.close();

# criação de componentes
player = Player();
player.volume = 30;
gerarPlaylist();
player.loadlist("novaPlaylist.txt");
player.volume = 30;
botao1 = Button(11);
botao2 = Button(12);
botao3 = Button(13);
led1 = LED(21);
led3 = LED(23);
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2);

player.pause()
led1.blink()

botao2.when_pressed = tocarPausarMusica;
botao3.when_held = acelerarMusica;
botao3.when_released = avancarMusica;
botao1.when_pressed = voltarFaixa;

inicio = 0;
fim = 16;

# loop infinito
while True:
    exibirFaixa()
    sleep(0.5);


