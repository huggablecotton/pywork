
'''
    0 <------ pan left(pan++) ------- > 300   320 <------ pan right(pan--) ------------> 640
  0 +------------------------------------+-----+-----+------------------------------------+
    |                                    |     |     |                ^                   | 
    |                                    |     |     |                |                   | 
    |                                    |     |     |          tilt up(tilt--)           | 
    |                                    |     |     |                |                   | 
    |                                    |     |     |                v                   | 
220 +------------------------------------+-----+-----+------------------------------------+ 
    |                                    |     |     |                                    | 
    |                                    |     |     |                                    |  
240 +------------------------------------+-----+-----+------------------------------------+ 
    |                                    |     |     |                                    | 
    |                                    |     |     |                                    |  
260 +------------------------------------+-----+-----+------------------------------------+ 
    |                                    |     |     |                ^                   | 
    |                                    |     |     |                |                   | 
    |                                    |     |     |                                    | 
    |                                    |     |     |          tilt down(tilt++)         | 
    |                                    |     |     |                |                   | 
    |                                    |     |     |                v                   |  
480 +------------------------------------+-----+-----+------------------------------------+ 

'''

import cv2
import numpy as np
import serial

sp = serial.Serial('COM5', 9600, timeout = 1)

webcam = cv2.VideoCapture(0)

pos_x = pos_y = 90
_pos_x = _pos_y = 90

margin_x = 20
margin_y = 20

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

while webcam.isOpened():
    status, frame = webcam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100,100,120])
    upper_blue = np.array([150,255,255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    _, bin = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    
    largest_contour = None
    largest_area = 0    
    
    COLOR = (0, 255, 0)
    for cnt in contours:                # find largest blue object
        area = cv2.contourArea(cnt)
        if area > largest_area:
            largest_area = area
            largest_contour = cnt
            
     # draw bounding box with green line
    if largest_contour is not None:
        #area = cv2.contourArea(cnt)
        if largest_area > 500:  # draw only larger than 500
            x, y, width, height = cv2.boundingRect(largest_contour)       
            cv2.rectangle(frame, (x, y), (x + width, y + height), COLOR, 2)
            center_x = x + width//2
            center_y = y + height//2
            print("center: ( %s, %s )"%(center_x, center_y)) 
            
            if center_x < 320 - margin_x:
                print("pan left")
                if pos_x - 1 >= 0:
                    pos_x = pos_x - 1
                    _pos_x = pos_x
                else:
                    pos_x = 0
                    _pos_x = pos_x
                    
            elif center_x > 320 + margin_x:
                print("pan right")
                if pos_x + 1 <= 180:
                    pos_x = pos_x + 1
                    _pos_x = pos_x
                else:
                    pos_x = 180
                    _pos_x = pos_x   
            else:
                print("pan stop")
                pos_x = _pos_x
            
            
            
            if center_y < 240 - margin_y:
                print("tilt up")
                if pos_y - 1 >= 0:
                    pos_y = pos_y - 1
                    _pos_y = pos_y
                else:
                    pos_y = 0
                    _pos_y = pos_y
                    
            elif center_y > 240 + margin_y:
                print("tilt down")
                if pos_y + 1 <= 180:
                    pos_y = pos_y + 1
                    _pos_y = pos_y
                else:
                    pos_y = 180
                    _pos_y = pos_y
            else:
                print("tilt stop")
                pos_y = _pos_y
            
            
            tx_data = "pan" + str(pos_x) + '\n'
            sp.write(tx_data.encode())
            tilt_data = "tilt" + str(pos_y) + '\n'
            print(tx_data)
            print(tilt_data)
            
            sp.write(tilt_data.encode())
            
            
            
            
            
    cv2.imshow("VideoFrame",frame)       # show original frame
    '''
    cv2.imshow('blue', res)           # show applied blue mask
    cv2.imwrite("blue.png", res)
    cv2.imshow('Green', res1)          # show applied green mask
    cv2.imwrite("green.png", res1)
    cv2.imshow('red', res2)          # show applied red mask
    cv2.imwrite("red.png", res2)
    '''
    k = cv2.waitKey(100) & 0xFF
        
    if k == 27:
        break
   
        
#capture.release()
cv2.destroyAllWindows()