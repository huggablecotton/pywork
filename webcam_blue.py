import cv2, time
import numpy as np

webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

while webcam.isOpened():
    status, frame = webcam.read()   #리턴값이 두개 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#hsv 변환
    lower_blue = np.array([100,100,120])# range of blue
    upper_blue = np.array([150,255,255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)     # color range of blue
    res = cv2.bitwise_and(frame, frame, mask = mask)      # apply blue mask

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
            
    if largest_contour is not None:
     
        if largest_area > 500:  # draw only larger than 500
            x, y, width, height = cv2.boundingRect(largest_contour)       
            cv2.rectangle(frame, (x, y), (x + width, y + height), COLOR, 2)
            center_x = x + width//2 #
            center_y = y + height//2
            print("center: ( %s, %s )"%(center_x, center_y)) 
            
            
    cv2.imshow("VideoFrame",frame)       # show original frame
    # cv2.imshow('Blue', res)           # show applied blue mask
    # cv2.imwrite("blue.png", res)
    # cv2.imshow('Green', res1)          # show appliedgreen mask
    
    # cv2.imshow('red', res2)          # show applied red mask
    ''' '''
    
    #if status:
     #   cv2.imshow("blue", res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()