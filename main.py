# Importação de bibliotecas necessárias
import cv2
import pygame
import numpy as np

def encontrarForma(contorno):
    perimetro = cv2.arcLength(contorno, True)
    aproxDaForma = cv2.approxPolyDP(contorno, 0.04 * perimetro, True)
    lados = len(aproxDaForma)

    # Nome das forma de acordo com a aproximação
    if lados == 3:
        return 'Triangulo'
    elif lados == 4:
        return 'Retangulo'
    elif lados > 4:
        return 'Circulo'
    else:
        return 'Desconhecido'
    
def encontrarPoligono(imagem):
    # Converte imagem de rgb para hsv
    hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

    # Criar limites para a máscara
    baixos = np.array([45, 61, 138], dtype = np.uint8) #0 a 255
    altos = np.array([136, 255, 196], dtype = np.uint8) #0 a 255

    # Criar a máscara
    mascara = cv2.inRange(hsv, baixos, altos)
    kernel = np.ones((6, 6), np.uint8)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
    arestas = cv2.Canny(mascara, 1, 2)
    
    contornos, hierarquia = cv2.findContours(arestas, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area > 150:
            forma = encontrarForma(contorno)
            cv2.drawContours(imagem, [contorno], 0, (0, 0, 255), 2)
            x, y, _, _ = cv2.boundingRect(contorno)
            text_width, text_height = cv2.getTextSize(forma, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            text_x = x + int((_ - text_width) / 2)
            text_y = y + 30 + int((text_height + 10) / 2)
            cv2.putText(imagem, forma, (250, height - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            play_sound() #Emitir som (bip)

    return imagem

def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load('beep.wav')
    pygame.mixer.music.play()

def reproduzir_som():
    play_sound()

#Conectar openCV à WebCam do PC
webcam = cv2.VideoCapture(0) #0 É a câmera padrão do computador

forma_encontrada = False  # Variável para indicar se uma forma foi encontrada

while True:
    validacao, frame = webcam.read() # pegar a informação da webcam
    if not validacao: #validacao execunta enquantoconsegue ler a informação da webcam
        break  
    frame = encontrarPoligono(frame)
    height, width, _ = frame.shape
    cv2.putText(frame, "Pressione ESC para sair", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow('Webcam', frame) # Mostra uma janela com a informação de 'frame'
    key = cv2.waitKey(1) #Faz a imagem esperar em ms e armazena a tecla que estamos apertando.
    if key == 27:
        break  #27 é a tecla ESC

    # Verificar se uma forma foi encontrada e reproduzir o som
    if forma_encontrada:
        play_sound()
        forma_encontrada = False  # Redefinir a variável para False


webcam.release() # Finaliza  a conexão com a WebCam
cv2.destroyAllWindows()# Fechar a janela aberta com o imshow
