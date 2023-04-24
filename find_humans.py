import numpy as np
import cv2 as cv

webcam = cv.VideoCapture(0)

while(True):
    _, imageFrame = webcam.read()

    cv.imshow("Window", imageFrame)
    key = cv.waitKey(1)
    if(key == 27):
        break