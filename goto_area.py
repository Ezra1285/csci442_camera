#things robot needs to do
#follow color
#   move head up
#cross color lines
#   move head down
#   
#find orientation
#   move head down
#   spin until it finds the orange
#   move towards orange
#   stop when at orange
#move across the field
#   spin until it finds blue
#   move towards blue
#   print when in mining area
import time
import pyrealsense2 as rs
import numpy as np
import maestro
import cv2
import control_robot

robot_control = maestro.Controller()

cr = control_robot.robot()

def move_forward():
    # robot_control.setTarget(2, 6000)
    robot_control.setTarget(0, 5200)
    print("forward")

def stop():
    # robot_control.setTarget(2, 6000)
    robot_control.setTarget(0, 6000)
    print("stop")

def right_forward():
    robot_control.setTarget(0, 5100)
    robot_control.setTarget(2, 7100)
    print("left foward")

def left_forward():
    robot_control.setTarget(0, 5100)
    robot_control.setTarget(2, 4900)
    print("right forward")

def right():
    # robot_control.setTarget(0, 6000)
    robot_control.setTarget(2, 7100)
    print("left")

def left():
    # robot_control.setTarget(0, 6000)
    robot_control.setTarget(2, 4900)
    # print("right")

lower_blue = np.array([80,188,188])
upper_blue = np.array([150,255,255])
lower_orange = np.array([0,89,202])
upper_orange = np.array([40,150,255])
# lower_blue = np.array([120,188,188])
# upper_blue = np.array([150,255,255])
# lower_orange = np.array([0,89,100])
# upper_orange = np.array([40,150,255])
        
def goto_mine(edge, line_color, spin_flag):
    if(spin_flag == False):
        print(" start spining")
        
        cr.startSpin()
    edge = edge[40:440,250:550]
    imghsv = cv2.cvtColor(edge, cv2.COLOR_BGR2HSV)
    if("blue" == line_color):
        print("looking for blue")
        hsv_low = lower_blue
        hsv_high = upper_blue


        mask_blue = cv2.inRange(imghsv, lower_blue, upper_blue)
        contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blurred = cv2.blur(mask_blue, (10,10))
    elif ("orange" == line_color):
        print("looking for orange")
        hsv_low = lower_orange
        hsv_high = upper_orange
        mask_orange = cv2.inRange(imghsv, lower_orange, upper_orange)
        blurred = cv2.blur(mask_orange, (10,10))
    else:
        print("no color")
        hsv_low = lower_blue
        hsv_high = upper_blue
    contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total = 0
    x=0
    y=0
    if(not(len(contours) <1)):
            if(not spin_flag):
                
                cr.stopSpin()
                stop()
                time.sleep(2)
                spin_flag = True
    if(spin_flag):
        cr.headDown()
        for i in contours:
            M = cv2.moments(i)
            if M['m00'] != 0:
                
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                x += cx
                y += cy
                total +=1
                cv2.drawContours(edge, [i], -1, (0, 255, 0), 2)
                cv2.circle(edge, (cx, cy), 7, (0, 0, 255), -1)
                cv2.putText(edge, "center", (cx - 20, cy - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        if total == 0:
            total = 1
        yavg = int(x/total)
        xavg = int(y/total)
        cofy = int((150))
        cofx = int(250)
        cof = (cofx, cofy)
        cv2.circle(edge, cof, 10, (255,0,0), 5)
        cog = (xavg,yavg)
        cv2.circle(edge, cog, 10, (255,0,0), 5)

        xdif = cof[0] - cog[0]
        ydif = cof[1] - cog[1]
        print("MOVING")
        if ydif <-50:
            stop()
            return "done", spin_flag
        elif xdif <-15:
            if ydif >10:
                left_forward()
            else:
                right()
        elif xdif >15:
            if ydif > 10:
                right_forward()
            else:
                left()

        elif ydif > 0:
            move_forward()
        else:
            stop()
            print("bad")
        # if(total <3):
        #     stop()
        #     return "done", spin_flag
        cv2.circle(edge, cof, 10, (255,0,0), 5)
        cv2.circle(edge, cog, 10, (255,0,0), 5)
    else:
        
        print("spinning")
    
    cv2.imshow('RealSense', edge)
    cv2.waitKey(1)
    return "not done", spin_flag