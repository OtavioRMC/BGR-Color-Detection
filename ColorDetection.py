from utils import get_limits
import cv2
from threading import Thread
"""
Define the resolution of the frame bellow:
"""

USR_WIDTH = 1920
USR_HEIGTH = 1080
class VideoStream:
    def __init__(self,src=0):
        self.stream = cv2.VideoCapture(src)
        self.ret, self.frame = self.stream.read()
        self.thread.daemon = True
        self.thread.start()
    def update(self):
        while(True):
            self.ret, self.frame = self.stream.read()
    def read(self):
        return self.frame
    

colors = {
    'red': [0, 0, 255],
    'green': [0, 255, 0],
    'blue': [255, 0, 0],
}

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame_heigt, frame_width = frame.shape[:2]

    if frame is not None:
        frame = cv2.resize(frame,(USR_WIDTH,USR_HEIGTH))
    else:
        print("Error while resizing the frame")

    ############ ROI DEFINITION ###################
    roi_size = 200
    roi_top = int(frame_heigt - roi_size / 2)
    roi_bottom = int(frame_heigt + roi_size / 2)
    roi_left = int(frame_width - roi_size / 2)
    roi_rigth = int(frame_width + roi_size / 2)
    ##############################################

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for color_name, color in colors.items():
        lowerLimit, upperLimit = get_limits(color=color)

        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    
        # Operações Morfológicas para reduzir o ruído.
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.rectangle(frame,(roi_left,roi_top),(roi_rigth,roi_bottom),(0,233,255),2)
        cv2.putText(frame, "Detection Area", (roi_left - 12,roi_top - 10), cv2.FONT_HERSHEY_SIMPLEX,1,(0,233,255),2)
        
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                x, y, w, h = cv2.boundingRect(contour)
                center_x = x + w / 2
                center_y = y + h / 2

                if roi_left < center_x < roi_rigth and roi_top < center_y < roi_bottom:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.imshow('frame', frame)

    # Tecla para parar a execução do código
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()