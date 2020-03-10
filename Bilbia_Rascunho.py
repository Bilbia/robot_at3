#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import time

cap = cv2.VideoCapture("video1.mp4")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

lower = 0
upper = 1

white_1_hsv = np.array([0, 0, 78], dtype=np.uint8)
white1 = np.array([200, 200, 200], dtype=np.uint8)
white_2_hsv = np.array([0, 0, 100], dtype=np.uint8)
white2 = np.array([255, 255, 255], dtype=np.uint8)

while(True):
#     # Capture frame-by-frame
    
    ret, frame = cap.read()
    mask_white = cv2.inRange(frame, white1, white2)
    
    # Our operations on the frame come here
    # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # white_1_rgb = np.array([200, 200, 200])
    # white_2_rgb = np.array([255, 255, 255])

    
     

    
    if ret == False:
        print("Codigo de retorno FALSO - problema para capturar o frame")

    # img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # white1 = [(255, 255, 255),]
    # white2 = [(200, 200, 200)]
    # mask = cv2.inRange(img_hsv, white1, white2)
    blur = cv2.GaussianBlur(mask_white, (5,5),0)

    edges = cv2.Canny(blur,50,150)
    
    lines = cv2.HoughLines(edges,1,np.pi/180, 150)

    lista_m = []
    lista_h = []

    linhas_d_m = []
    linhas_d_x1 = []
    linhas_d_x2 = []
    linhas_d_y1 = []
    linhas_d_y2 = []

    linhas_e_m = []
    linhas_e_x1 = []
    linhas_e_x2 = []
    linhas_e_y1 = []
    linhas_e_y2 = []

    xis = []
    yis = []

    for x in range(0, len(lines)):    
        for rho, theta in lines[x]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            m = (y2 - y1)/(x2 - x1)
            
            h = y1 - m*x1

            lista_h.append(h)
            lista_m.append(m)

            #direita
            if m>0.3 and m<2:
                linhas_d_m.append(m)
                linhas_d_x1.append(x1)
                linhas_d_x2.append(x2)
                linhas_d_y1.append(y1)
                linhas_d_y2.append(y2)


            #esquerda
            elif m<-0.2 and m>-2:
                linhas_e_m.append(m)
                linhas_e_x1.append(x1)
                linhas_e_x2.append(x2)
                linhas_e_y1.append(y1)
                linhas_e_y2.append(y2)
            
            else:
                lista_m.remove(m) 


            
        
    if len(lista_m) > 1 and lista_m[0] != lista_m[1]:
        x_i = (lista_h[1] - lista_h[0])/(lista_m[0] - lista_m[1])
        y_i = lista_m[0] * x_i + lista_h[0]
        x_i = int(x_i)
        y_i = int(y_i)
        xis.append(x_i)
        yis.append(y_i)

    # if len(lista_m) > 1:
    #     for m in range((len(lista_m)-1)):
    #         if lista_m[m] != lista_m[m+1]:
    #             x_i = int((lista_h[m+1] - lista_h[m])/(lista_m[m] - lista_m[m+1]))
    #             y_i = int(lista_m[m]*x_i + lista_h[m])
    #             xis.append(x_i)
    #             yis.append(y_i)
            
    
    if lista_m[0] - lista_m[1] > 0.4:
        xi = int(np.mean(xis))
        yi = int(np.mean(yis))
        cv2.circle(frame, (xi, yi), 1, (0,255,0), 5)

 

    
    
    #linha direita
    if len(linhas_d_m)>1:
                x1_media = int(np.mean(linhas_d_x1))
                x2_media = int(np.mean(linhas_d_x2))
                y1_media = int(np.mean(linhas_d_y1))
                y2_media = int(np.mean(linhas_d_y2))
                cv2.line(frame,(x1_media,y1_media), (x2_media,y2_media), (50,0,255),2) 
    
    #linha esquerda
    if len(linhas_e_m)>1:
                x1_media = int(np.mean(linhas_e_x1))
                x2_media = int(np.mean(linhas_e_x2))
                y1_media = int(np.mean(linhas_e_y1))
                y2_media = int(np.mean(linhas_e_y2))
                cv2.line(frame,(x1_media,y1_media), (x2_media,y2_media), (50,0,255),2) 



    
    # quebrarvelocidade em 4
    
    cv2.imshow("Vídeo", frame)
    # cv2.imshow("Máscara", edges)

    # ver posicao 0, colocar em variavel, acessar variavel
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
