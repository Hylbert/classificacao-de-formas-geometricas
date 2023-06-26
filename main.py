# Importação de bibliotecas necessárias
import cv2
import numpy as np

#Conectar openCV à WebCam do PC
webcam = cv2.VideoCapture(0) #0 É a câmera padrão do computador

#Verifica se a conexão foi bem executada
if webcam.isOpened():
    print("Conectou!")
    validacao, frame = webcam.read() # pegar a informação da webcam

while validacao: #validacao só roda se conseguier ler a informação da webcam
    validacao, frame = webcam.read() # pegar a informação da webcam
    cv2.imshow('Webcam', frame)#mostra uma janela com a informação de 'frame'
    key = cv2.waitKey(1) #Faz a imagem esperar em ms e armazena a tecla que estamos apertando.
    if key == 27:
        break  #27 é a tecla ESC

webcam.release() #Finaliza  a conexão com a WebCam
cv2.destroyAllWindows()#Fechar a janela aberta com o imshow
