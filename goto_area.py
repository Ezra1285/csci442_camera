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
    # print("forward")

def stop():
    # robot_control.setTarget(2, 6000)
    robot_control.setTarget(0, 6000)
    # print("stop")

def right_forward():
    robot_control.setTarget(0, 5100)
    robot_control.setTarget(2, 7100)
    # print("left foward")

def left_forward():
    robot_control.setTarget(0, 5100)
    robot_control.setTarget(2, 4900)
    # print("right forward")

def right():
    # robot_control.setTarget(0, 6000)
    robot_control.setTarget(2, 7100)
    # print("left")

def left():
    # robot_control.setTarget(0, 6000)
    robot_control.setTarget(2, 4900)
    # print("right")

lower_blue = np.array([70,140,170])
upper_blue = np.array([160,255,255])
lower_orange = np.array([7,120,232])
upper_orange = np.array([25,150,255])
red_lower = np.array([136, 87, 111])
red_upper = np.array([180, 255, 255])
# #  Green thresh
# green_lower = np.array([49, 60, 128], np.uint8)
# green_upper = np.array([86, 255, 255], np.uint8)
green_lower = np.array([27, 91, 106]) 
green_upper = np.array([88, 173, 197]) 
# yellow
yellow_lower = np.array([20, 102, 91])
yellow_upper = np.array([52, 255, 255])
# lower_blue = np.array([120,188,188])
# upper_blue = np.array([150,255,255])
# lower_orange = np.array([0,89,100])
# upper_orange = np.array([40,150,255])
        
def goto_mine(edge, line_color, spin_flag):
    cr.headstraight()
    if(spin_flag == False):
        # print(" start spining")
        
        cr.startSpin()
    edge = cv2.blur(edge,(7,7))
    edge = edge[40:,250:550]
    
    imghsv = cv2.cvtColor(edge, cv2.COLOR_BGR2HSV)
    if("blue" == line_color):
        # print("looking for blue")
        hsv_low = lower_blue
        hsv_high = upper_blue
        mask_blue = cv2.inRange(imghsv, lower_blue, upper_blue)
        contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # blurred = cv2.blur(mask_blue, (10,10))
    elif ("orange" == line_color):
        # print("looking for orange")
        hsv_low = lower_orange
        hsv_high = upper_orange
        mask_orange = cv2.inRange(imghsv, lower_orange, upper_orange)
        contours, _ = cv2.findContours(mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # blurred = cv2.blur(mask_orange, (5,5))
    elif ("pink" == line_color):
        # print("looking for orange")
        hsv_low = red_lower
        hsv_high = red_upper
        mask_red = cv2.inRange(imghsv, lower_orange, upper_orange)
        contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # blurred = cv2.blur(mask_red, (5,5))
    elif ("green" == line_color):
        # print("looking for orange")
        hsv_low = green_lower
        hsv_high = green_upper
        mask_green = cv2.inRange(imghsv, lower_orange, upper_orange)
        contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # blurred = cv2.blur(mask_green, (5,5))
    elif ("yellow" == line_color):
        # print("looking for orange")
        hsv_low = yellow_lower
        hsv_high = yellow_upper
        mask_yellow = cv2.inRange(imghsv, lower_orange, upper_orange)
        contours, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # blurred = cv2.blur(mask_yellow, (5,5))
    else:
        # print("no color")
        hsv_low = lower_blue
        hsv_high = upper_blue
    # contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total = 0
    x=0
    y=0
    if(not(len(contours) <1)):
            if(not spin_flag):
                time.sleep(1)
                cr.stopSpin()
                stop()
                time.sleep(2)
                spin_flag = True
    if(spin_flag):
        cr.headstraight()
        for i in contours:
            area = cv2.contourArea(i)
            if area >150:
                
                M = cv2.moments(i)
                if M['m00'] != 0:
                    
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    x += cx
                    y += cy
                    total +=1
                    cv2.drawContours(edge, [i], -1, (0, 255, 0), 2)
                    # cv2.circle(edge, (cx, cy), 7, (0, 0, 255), -1)
                    cv2.putText(edge, "center", (cx - 20, cy - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        if total == 0:
            total = 1
        yavg = int(x/total)
        xavg = int(y/total)
        cofy = int((330))
        cofx = int(150)
        cof = (cofx, cofy)
        # cv2.circle(edge, cof, 10, (255,0,0), 5)
        cog = (xavg,yavg)
        # cv2.circle(edge, cog, 10, (255,0,0), 5)

        xdif = cof[0] - cog[0]
        ydif = cof[1] - cog[1]
        # print("MOVING")
        
        if ydif >75:
            move_forward()
            if(x + y<1):
                move_forward()
                time.sleep(3)
                stop()
                if line_color == "blue":
                    print("entered mining area")
                elif line_color == "orange":
                    print("entered goal area")
                else:
                    print("GOOAALLLLL")
                return "done", spin_flag
        elif ydif <0:
            move_forward()
            time.sleep(3)
            stop()
            if line_color == "blue":
                print("entered mining area")
            elif line_color == "orange":
                print("entered goal area")
            else:
                print("GOOAALLLLL")
            return "done", spin_flag
        
        
        

        elif ydif > 0:
            move_forward()
        
        elif xdif <-30:
            if ydif >10:
                left_forward()
            else:
                right()
        elif xdif >30:
            if ydif > 10:
                right_forward()
            else:
                left()
        else:
            stop()
            # print("bad")
        if(x+y <1):
            move_forward()
            time.sleep(3)
            stop()
            if line_color == "blue":
                print("entered mining area")
            elif line_color == "orange":
                print("entered goal area")
            else:
                print("GOOAALLLLL")
            return "done", spin_flag
        # cv2.circle(edge, cof, 10, (255,0,0), 5)
        cv2.circle(edge, cog, 10, (255,0,0), 5)
    else:
        pass
        # print("spinning")
    
    cv2.imshow('RealSense', edge)
    cv2.waitKey(1)
    return "not done", spin_flag