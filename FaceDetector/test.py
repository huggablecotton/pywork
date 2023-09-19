import cv2

def videoDetector(cam, cascade):
    cap = cv2.VideoCapture(cam)

    while True:
        ret, img = cap.read()

        if ret:
            # Check if the image is empty (has valid size)
            if not img.size:
                print("Image is empty. Skipping.")
                continue

            # Resize the image
            img_resized = cv2.resize(img, dsize=None, fx=1.0, fy=1.0)

            # Rest of the face detection and processing code goes here

            # Display the resized image
            cv2.imshow('Resized Image', img_resized)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Replace '0' with the appropriate camera index
videoDetector(0, cascade)  # assuming 'cascade' is defined elsewhere in your code
