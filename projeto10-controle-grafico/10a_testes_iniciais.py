from cv2 import *
stream = VideoCapture(0)
while True:
    _, imagem = stream.read()
    
    imagem_hsv = cvtColor(imagem, COLOR_BGR2HSV)
    light_orange = (0, 60, 60) # valores no espaço HSV
    dark_orange = (7, 255, 255) # valores no espaço HSV
    mascara = inRange(imagem_hsv, light_orange, dark_orange)
    mascara2 = bitwise_not(mascara)
    imagem2 = bitwise_and(imagem, imagem, mask=mascara)
    imagem3 = bitwise_and(imagem, imagem, mask=mascara2)
    imagem_pb = cvtColor(imagem3, COLOR_BGR2GRAY)
    imagem_pb = cvtColor(imagem_pb, COLOR_GRAY2BGR)
    imagem_combinada = addWeighted(imagem_pb, 1,imagem2, 1, 0)
    putText(imagem_combinada, "Cristiano Ronaldo", (60,100), color=(0,165,255),thickness=4, fontFace=FONT_HERSHEY_SIMPLEX, fontScale=2)
    imshow("Minha Janela Combinada", imagem_combinada)
    # mostra a imagem durante 1 milissegundo
    # e interrompe loop quando tecla q for pressionada
    if waitKey(1) & 0xFF == ord("q"):
        break
stream.release()
destroyAllWindows()