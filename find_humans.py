import numpy as np
import cv2 as cv

webcam = cv.VideoCapture(0)

while(1):
    _, frame = webcam.read()
    frame = cv.resize(frame, None, fx=.75,fy=.75, interpolation=cv.INTER_AREA)
    cv.imshow("Window", frame)
    key = cv.waitKey(1)
    if(key == 27):
        cv.destroyAllWindows()
        break