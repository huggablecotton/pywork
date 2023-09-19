import cv2, time

webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

True

while webcam.isOpened():
    status, frame = webcam.read()   #리턴값이 두개 
    print(status)
    time.sleep(0.1)

    if status:
        cv2.imshow("test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()