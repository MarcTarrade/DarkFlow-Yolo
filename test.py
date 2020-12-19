#####################################
## Description: Test if darkflow is correctly installed
##
###########################
import cv2
from darkflow.net.build import TFNet
import numpy as np

# Options for YoLo
options = {
    'model': './cfg/yolo.cfg',
    'load': './bin/yolo.weights',
    'threshold': 0.2,
    'gpu': 0.0
}
# Instantion of Tensor Flow for object recognition
tfnet = TFNet(options)

# Set a first capture
cap = cv2.VideoCapture("sample_img/sample_dog.jpg")
# Set the resolution of the capture
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    ret, frame = cap.read()
    if ret:
        frame = np.asarray(frame)
        # Create a list of object results for the capture
        results = tfnet.return_predict(frame)

        for result in results:
            # Top left of the object detected
            top_x = result['topleft']['x']
            top_y = result['topleft']['y']
            # Bottom right of the object detected
            btm_x = result['bottomright']['x']
            btm_y = result['bottomright']['y']

            confidence = result['confidence']
            label = result['label'] + " " + str(round(confidence, 3))
            # Create a rectangle around the object
            frame = cv2.rectangle(frame, (top_x, top_y), (btm_x, btm_y), (255,0,0), 3)
            # Put the name of the object above it
            frame = cv2.putText(frame, label, (top_x, top_y-5), cv2.FONT_HERSHEY_COMPLEX , 1, (0, 230, 0), 1)

            # Display the capture
            cv2.imshow('frame',frame)
    # Stop the program        
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()