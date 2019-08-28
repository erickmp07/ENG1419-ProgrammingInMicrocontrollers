# importação de bibliotecas
from gpiozero import LED
from gpiozero import Button
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
from lirc import init, nextcode

# definição de funções
def acendeLEDs():
    for led in leds:
        led.on()
        
def apagaLEDs():
    for led in leds:
        led.off()
        
def select_led(position):
    global selected_led
    lcd.clear()
    lcd.message("LED " + str(position + 1) + "\nselecionado")
    selected_led = position
    
def toggle_selected_led():
    leds[selected_led].toggle()

# criação de componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
button1 = Button(11)
button2 = Button(12)

button1.when_pressed = acendeLEDs
button2.when_pressed = apagaLEDs

lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

init("aula", blocking=False)

keys_dict = {"KEY_1": 0, "KEY_2": 1, "KEY_3": 2, "KEY_4": 3, "KEY_5": 4}
selected_led = None

# loop infinito
while True:
    lista_com_codigo = nextcode()
    if lista_com_codigo != []:
        codigo = lista_com_codigo[0]
        if codigo in keys_dict:
            select_led(keys_dict[codigo])
        if codigo == "KEY_OK" and selected_led != None:
            toggle_selected_led()
        if codigo == "KEY_UP" and selected_led != None:
            if selected_led + 1 <= 4:
                select_led(selected_led + 1)
        if codigo == "KEY_DOWN" and selected_led != None:
            if selected_led - 1 >= 0:
                select_led(selected_led - 1)
        
    sleep(0.2)