# importação de bibliotecas
from os import system
from gpiozero import LED, Button
from Adafruit_CharLCD import Adafruit_CharLCD
from mplayer import Player
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD


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

def proxFaixa():
    player.pt_step(1)
    
def voltarFaixa():
    if(player.time_pos < 2):
        player.pt_step(-1)
    else:
        player.time_pos = 0

def exibirFaixa():
    metadados = player.metadata
    if(metadados):
        faixa = player.metadata["Title"]
        lcd.clear()
        lcd.message(faixa)

# criação de componentes
player = Player();
player.volume = 30;
player.loadlist("playlist.txt");
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
botao3.when_pressed = proxFaixa;
botao1.when_pressed = voltarFaixa;

# loop infinito
while True:
    exibirFaixa()
    sleep(0.5);
