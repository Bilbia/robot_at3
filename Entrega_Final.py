import cv2
import numpy as np
import math
import auxiliar as aux

video1 = cv2.VideoCapture("video1.mp4")

while(True):
    # Capture frame-by-frame
    ret, frame = video1.read()
    
    if ret == False:
        print("Codigo de retorno FALSO - problema para capturar o frame")

    # Our operations on the frame come here
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    white = "#eb4034"
    white_1, white_2 = aux.ranges(white)
    mask_white = cv2.inRange(rgb, white_1, white_2)
    edges = cv2.Canny(gray,50,150,apertureSize = 3) 
    lines = cv2.HoughLines(edges,1,np.pi/180, 200) 
    
    for r,theta in lines[0]: 
        # Stores the value of cos(theta) in a 
        a = np.cos(theta) 
      
        # Stores the value of sin(theta) in b 
        b = np.sin(theta) 
          
        # x0 stores the value rcos(theta) 
        x0 = a*r 
          
        # y0 stores the value rsin(theta) 
        y0 = b*r 
          
        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta)) 
        x1 = int(x0 + 1000*(-b)) 
          
        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta)) 
        y1 = int(y0 + 1000*(a)) 
      
        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta)) 
        x2 = int(x0 - 1000*(-b)) 
          
        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta)) 
        y2 = int(y0 - 1000*(a)) 
          
        # cv2.line draws a line in img from the point(x1,y1) to (x2,y2). 
        # (0,0,255) denotes the colour of the line to be  
        #drawn. In this case, it is red.  
        cv2.line(gray,(x1,y1), (x2,y2), (0,0,255),2) 
          
    
    # Display the resulting frame
    # cv2.imshow('frame',frame)
    cv2.imshow('hsv', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
video1.release()
cv2.destroyAllWindows()

