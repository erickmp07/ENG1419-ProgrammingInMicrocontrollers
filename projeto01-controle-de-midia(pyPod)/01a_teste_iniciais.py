# importação de bibliotecas
from gpiozero import LED, Button
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD

# definição de funções
def trocarEstadoLED1():
    led1.toggle();
    
def piscarEContarLED2():
    led2.blink(n = 4);
    contarBotao2Apertado();

def piscarLED3():
    led3.blink(on_time = 1.0, off_time = 3.0);
    
def contarBotao2Apertado():
    global qtd;
    qtd += 1;
    lcd.clear();
    lcd.message(str(qtd));
    
def acenderLED5():
    if (botao3.is_pressed and botao4.is_pressed):
        led5.on();
    else:
        led5.off();

# criação de componentes
led1 = LED(21);
led2 = LED(22);
led3 = LED(23);
led5 = LED(25);
botao1 = Button(11);
botao2 = Button(12);
botao3 = Button(13);
botao4 = Button(14);
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2);

botao1.when_pressed = trocarEstadoLED1;
botao2.when_pressed = piscarEContarLED2;
piscarLED3();

qtd = 0;

# loop infinito
while True:
    acenderLED5();
    sleep(0.2);