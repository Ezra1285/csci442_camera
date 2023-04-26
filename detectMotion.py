import cv2 as cv
import numpy as np

# min_h = max_h= min_s = max_s = min_v= max_v= 0

cap = cv.VideoCapture(0)
mouse = (0,0)
def mouseCall(evt, x, y, flags, pic):
    #print ("mouse Worked")
    
    if evt == cv.EVENT_LBUTTONDOWN:
            print (pic.shape, x, y)
            print("HSV: ",pic[x][y])

def minH(value):
    global min_h
    min_h = value
    
def maxH(value):
    global max_h
    max_h = value

def minS(value):
    global min_s
    min_s = value
    
def maxS(value):
    global max_s
    max_s = value

def minV(value):
    global min_v
    min_v = value
    
def maxV(value):
    global max_v
    max_v = value

cv.namedWindow("webcam", 1)
cv.namedWindow("thresh", 1)
cv.namedWindow("contours", 1)
ksize = (5, 5)
alpha = 1
beta = 2
dst = None
while True:
    ret, frame = cap.read()
    
    
    frame = cv.resize(frame, None, fx=.75,fy=.75, interpolation=cv.INTER_AREA)
    blank = np.zeros_like(frame)
    bright = cv.convertScaleAbs(frame, alpha, beta)
    blr = cv.blur(bright, ksize=ksize)
    if dst is None:
        dst = blr.copy().astype("float")
    cv.accumulateWeighted(blr,dst, .5)
    # convertScaleAbs to convert to correct type
    newdst = cv.convertScaleAbs(dst)

    new = cv.absdiff(blr, newdst)

    new = cv.cvtColor(new, cv.COLOR_BGR2GRAY)
    new = cv.threshold(new, 10, 255, cv.THRESH_BINARY)[1]
    new = cv.blur(new, ksize=ksize)
    new = cv.threshold(new, 100, 255, cv.THRESH_BINARY)[1]
    cv.imshow("thresh", new)
    
    # blank.fill()
    contours, hierarchy  = cv.findContours(new, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # hull = cv.convexHull(contours)
    minx= miny= maxx= maxy = 0
    for contour in contours:

        (x,y,w,h) = cv.boundingRect(contour)
        minx, maxx = min(x, minx), max(x+w, maxx)
        miny, maxy = min(y, miny), max(y+h, maxy)
        if w>40 and h> 40:
            cv.rectangle(frame, (x,y),(x+w,y +h),(0,0,255),1)
    cv.drawContours(blank, contours, -1, (0,255,0),len(contours))
    # cv.rectangle(blank, (x,y), cv.Scalar(0,255,255,0))
    cv.imshow("contours", blank)
    cv.imshow("webcam",frame)
    
    # cv.imshow('binary',thresh)
    c = cv.waitKey(1)
    if(c == 27):
        break

        

cap.release()
cv.destroyAllWindows()
