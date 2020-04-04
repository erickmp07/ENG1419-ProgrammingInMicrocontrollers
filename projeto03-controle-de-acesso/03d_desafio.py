from extra.redefinir_banco import redefinir_banco
from pymongo import MongoClient, ASCENDING, DESCENDING
from Adafruit_CharLCD import Adafruit_CharLCD as LCD
from lirc import init, nextcode
from time import sleep
from gpiozero import Buzzer
from gpiozero import Button
from gpiozero import DistanceSensor
from datetime import datetime, timedelta

campainha=Buzzer(16)

sensor=DistanceSensor(trigger=17, echo=18)

init("aula", blocking=False)

# a linha abaixo apaga todo o banco e reinsere os moradores
#redefinir_banco()

# parâmetros iniciais do banco
cliente = MongoClient("localhost", 27017)
banco = cliente["projeto03"]
colecao = banco["moradores"]
colecaolog= banco["log"]
tentativas = banco["logTentativas"]

# definição de funções
def validar_apartamento(numeroApartamento):
    busca = {"apartamento" : numeroApartamento}
    apartamento = colecao.find_one(busca)
    
    busca = {"apartamento": numeroApartamento}
    ordenacao = [ ["data", DESCENDING] ]
    
    ultimaTentativa = tentativas.find_one(busca, sort=ordenacao)
    if (ultimaTentativa != None):
        numTentativas = ultimaTentativa["tentativas"]
        if (numTentativas > 2):
            dataTentativa = ultimaTentativa["data"]
            delta = ((dataTentativa + timedelta(seconds=15 * (numTentativas - 2))) - datetime.now()).total_seconds()
            if (delta > 0):
                return delta
    
    return apartamento != None

def retornar_nome_do_morador(numeroApartamento, senha):
    busca = {"apartamento" : numeroApartamento, "senha" : senha}
    morador = colecao.find_one(busca)
    if (morador == None):
        busca = {"apartamento": numeroApartamento}
        ordenacao = [ ["data", DESCENDING] ]
        
        ultimaTentativa = tentativas.find_one(busca, sort=ordenacao)
        if (ultimaTentativa == None):
            documento = {"data" : datetime.now(), "apartamento" : numeroApartamento, "tentativas" : 1 }
        else:
            documento = {"data" : datetime.now(), "apartamento" : numeroApartamento, "tentativas" : ultimaTentativa["tentativas"] + 1 }
            
        tentativas.insert(documento)
        
        return None
    
    documento = {"data" : datetime.now(), "apartamento" : numeroApartamento, "tentativas" : 0}
    tentativas.insert(documento)
                     
    return morador["nome"]

def coletar_digitos(mensagem):
    lcd.clear()
    lcd.message(mensagem + "\n")
    resultado = ""
    while True:
        codigos = nextcode()
        if (codigos != []):
            tecla = codigos[0]
            campainha.beep(n=1,on_time=0.2)
            
            
            if (tecla[-1] == "K"):
                return resultado
            lcd.message("*")
            resultado = resultado + tecla[-1]
            
    return resultado

def entrada():
    apartamento = coletar_digitos("Digite o apto:")
    ehValido = validar_apartamento(apartamento)
            
    if (ehValido == False):
        lcd.clear()
        lcd.message("Apartamento\ninválido!")
    elif (ehValido == True):
        senha = coletar_digitos("Digite a senha:")
        morador = retornar_nome_do_morador(apartamento, senha)

        lcd.clear()
        if (morador == None):
            lcd.message("Acesso negado")
            campainha.beep(n=3,on_time=0.2,off_time=0.1)
        else:
            lcd.message("Bem-vindo(a)\n" + morador)
        documento={"Apt": apartamento, "Data/Hora" : datetime.now(),"nome" : morador}
        colecaolog.insert(documento)
    else:
        lcd.clear()
        lcd.message("Bloqueado por\n" + str(ehValido) + " segundos!")
        
    sleep(1)
    lcd.clear()

def dados():
    apt= coletar_digitos("Digite o apto:")
    busca = {"Apt": apt}
    ordenacao = [ ["Data/Hora", DESCENDING] ]
    lista= list( colecaolog.find(busca, sort=ordenacao) )
    for item in lista:
        if (item["nome"]==None):    
            print(item["Data/Hora"].strftime("%d/%m (%H:%M)")+ ": SENHA INCORRETA")
        else:
            print(item["Data/Hora"].strftime("%d/%m (%H:%M)")+": " + item["nome"])
            
        
# criação de componentes
lcd = LCD(2,3,4,5,6,7,16,2)
sensor.threshold_distance=0.2
sensor.when_in_range=entrada
botao1=Button(11)
botao1.when_pressed=dados

# loop infinito


