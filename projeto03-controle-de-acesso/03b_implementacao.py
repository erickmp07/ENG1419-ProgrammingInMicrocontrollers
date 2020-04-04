# importação de bibliotecas
from extra.redefinir_banco import redefinir_banco
from pymongo import MongoClient
from Adafruit_CharLCD import Adafruit_CharLCD as LCD
from lirc import init, nextcode
from time import sleep

init("aula", blocking=False)

# a linha abaixo apaga todo o banco e reinsere os moradores
redefinir_banco()

# parâmetros iniciais do banco
cliente = MongoClient("localhost", 27017)
banco = cliente["projeto03"]
colecao = banco["moradores"]


# definição de funções
def validar_apartamento(numeroApartamento):
    busca = {"apartamento" : numeroApartamento}
    apartamento = colecao.find_one(busca)
    return apartamento != None

def retornar_nome_do_morador(numeroApartamento, senha):
    busca = {"apartamento" : numeroApartamento, "senha" : senha}
    morador = colecao.find_one(busca)
    if (morador == None):
        return None
    
    return morador["nome"]

def coletar_digitos(mensagem):
    lcd.clear()
    lcd.message(mensagem + "\n")
    resultado = ""
    while True:
        codigos = nextcode()
        if (codigos != []):
            tecla = codigos[0]
            
            
            if (tecla[-1] == "K"):
                return resultado
            lcd.message("*")   
            resultado = resultado + tecla[-1]
            
    return resultado

# criação de componentes
lcd = LCD(2,3,4,5,6,7,16,2)

# loop infinito
while True:
    apartamento = coletar_digitos("Digite o apto:")
    ehValido = validar_apartamento(apartamento)
    if (ehValido == False):
        lcd.clear()
        lcd.message("Apartamento\ninválido!")
        sleep(1)
        continue
    
    senha = coletar_digitos("Digite a senha:")
    morador = retornar_nome_do_morador(apartamento, senha)
    
    lcd.clear()
    if (morador == None):
        lcd.message("Acesso negado")
    else:
        lcd.message("Bem-vindo(a)\n" + morador)
        
    sleep(1)