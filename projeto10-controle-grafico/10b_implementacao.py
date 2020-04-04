from serial import Serial
from threading import Thread
from extra.tello import Tello
from time import sleep
from cv2 import *
from traceback import format_exc
from threading import Timer

timerBateria = None
timerCoordDim = None
timerVariacao = None
ponto_atual = 0


def calcularVariacao():
    global ponto_atual
    drone.goto(int(variacaoX[ponto_atual]), int(variacaoY[ponto_atual]), 0, 40)
    ponto_atual += 1
    if ponto_atual >= tamanhoLista:
        ponto_atual = 0 
    #for i in range(tamanhoLista):
    #    drone.goto(variacaoX[i], variacaoY[i], 0, 40)

    global timerVariacao
    timerVariacao = Timer(5.0, calcularVariacao)
    timerVariacao.start()

def pararCalculoVariacao():
    global timerVariacao
    if timerVariacao != None:
        timerVariacao.cancel()
        timerVariacao = None
    
def enviarInfoBateria():
    estados = drone.state
    texto = "bateria " + str(estados["bat"]) + "\n"
    meu_serial.write(texto.encode("UTF-8"))
    global timerBateria
    timerBateria = Timer(5.0, enviarInfoBateria)
    timerBateria.start()
    
def enviarCoordenadasDimensoes():
    if imagem is None:
        return
    
    alturaCV2 = imagem.shape[0]
    comprimentoCV2 = imagem.shape[1]
    
    xMap = (xMaior * 200) / comprimentoCV2
    yMap = (yMaior * 150) / alturaCV2
    comprimentoMap = (comprimentoMaior * 200) / comprimentoCV2
    alturaMap = (alturaMaior * 150) / alturaCV2
   
    texto = "retangulo %03d %03d %03d %03d\n"%(xMap,yMap,comprimentoMap,alturaMap)
    meu_serial.write(texto.encode("UTF-8"))
    
    global timerCoordDim
    timerCoordDim = Timer(1.0, enviarCoordenadasDimensoes)
    timerCoordDim.start()
    
def serial():
    global variacaoX
    global variacaoY
    global tamanhoLista
    global ponto_atual
    
    while True:
        if meu_serial != None:
            texto_recebido = meu_serial.readline().decode().strip()
            if texto_recebido != "":
                print(texto_recebido)

            if texto_recebido == "decolar":
                pararCalculoVariacao()
                drone.takeoff()
            elif texto_recebido == "pousar":
                pararCalculoVariacao()
                drone.land()
            elif texto_recebido == "esquerda":
                pararCalculoVariacao()
                drone.rc(40, 0, 0, 0)
            elif texto_recebido == "frente":
                pararCalculoVariacao()
                drone.rc(0, 40, 0, 0)
            elif texto_recebido == "direita":
                pararCalculoVariacao()
                drone.rc(-40, 0, 0, 0)
            elif texto_recebido == "parar":
                pararCalculoVariacao()
                drone.rc(0, 0, 0, 0)
            elif "trajeto" in texto_recebido:
                coordenadas = texto_recebido.split(" ")
                
                i = 0
                valoresX = []
                valoresY = []
                ponto_atual = 0
                
                fatorProporcao = 40 / 100
                
                for coordenada in coordenadas:
                    if i == 0:
                        i = i + 1
                        continue
                    if i % 2 == 1:
                        valoresX.append(int(coordenada) * fatorProporcao)
                    else:
                        valoresY.append(int(coordenada) * fatorProporcao)
                    i = i + 1
                variacaoX = []
#                xRef = valoresX[0]
#                for x in valoresX:
#                    if x == valoresX[0]:
#                        continue
#                    variacaoX.append(x - xRef)
#                    xRef = x
#                variacaoX.append(valoresX[0] - xRef)
                
                for k in range(len(valoresX)):
                    if k == 0:
                        x_primeiro = valoresX[k]
                    else:
                        variacaoX.append(valoresX[k] - valoresX[k-1])
                variacaoX.append(x_primeiro - valoresX[k])
                
                variacaoY = []
#                yRef = valoresY[0]
#                for y in valoresY:
#                    if y == valoresY[0]:
#                        continue
#                    variacaoY.append(y - yRef)
#                    yRef = y
#                variacaoY.append(valoresY[0] - yRef)
                for k in range(len(valoresY)):
                    if k == 0:
                        y_primeiro = valoresY[k]
                    else:
                        variacaoY.append(valoresY[k] - valoresY[k-1])
                variacaoY.append(y_primeiro - valoresY[k])
                    
                tamanhoLista = len(variacaoX)
                calcularVariacao()
                
                print(variacaoX, variacaoY)
                
        sleep(0.1)

#meu_serial = None
meu_serial = Serial("COM35", baudrate=9600, timeout=0.1)
print("Serial: ok")

thread = Thread(target=serial)
thread.daemon = True
thread.start()

imagem = None

timerCoordDim = Timer(1.0, enviarCoordenadasDimensoes)
timerCoordDim.start()

drone = Tello("TELLO-C7AC08", test_mode=False)
#drone = Tello("TELLO-D023AE", test_mode=True)
drone.inicia_cmds()

xMaior = 0
yMaior = 0
comprimentoMaior = 0
alturaMaior = 0
areaMaior = 0

stream = VideoCapture(0)
imagem = drone.current_image

sleep(5)
print("[INFO] - Drone pronto")
    
enviarInfoBateria()

try:
    while True:
        _, imagem = stream.read()
        imagem = drone.current_image
        if imagem is not None:    
            imagem_hsv = cvtColor(imagem, COLOR_BGR2HSV)
            light_orange = (0, 60, 60)
            dark_orange = (7, 255, 255)
            mascara = inRange(imagem_hsv, light_orange, dark_orange)
            
            contornos,_ = findContours(mascara, RETR_TREE, CHAIN_APPROX_SIMPLE)
            
            xMaior = 0
            yMaior = 0
            comprimentoMaior = 0
            alturaMaior = 0
            areaMaior = 0
            
            for contorno in contornos:
                x, y, comprimento, altura = boundingRect(contorno)
                area = comprimento * altura
                if area > 2000 and area > areaMaior:
                    xMaior = x
                    yMaior = y
                    comprimentoMaior = comprimento
                    alturaMaior = altura
                    areaMaior = area
                
            rectangle(imagem, pt1=(xMaior,yMaior), pt2=(xMaior+comprimentoMaior,yMaior+alturaMaior), color=(57,255,20), thickness=3)
                
            imshow("Minha Janela", imagem)
            if waitKey(1) & 0xFF == ord("q"):
                break
            
    stream.release()
    destroyAllWindows()

        

except:
    if meu_serial != None:
        meu_serial.close()
    print("FIM!")
    print(format_exc())
    drone.land()
   