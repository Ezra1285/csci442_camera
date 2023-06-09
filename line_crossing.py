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

import pyrealsense2 as rs
import numpy as np
import maestro
import cv2
import control_robot
# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    # print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

def crop_center(img,cropx,cropy):
    y,x = img.shape
    startx = x//2-(cropx//2)
    starty = y//2-(cropy//2)    
    return img[starty:starty+cropy,startx:startx+cropx]

def move_forward():
    robot_controll.setTarget(2, 6000)
    robot_controll.setTarget(0, 5250)
    print("forward")

def stop():
    robot_controll.setTarget(2, 6000)
    robot_controll.setTarget(0, 6000)
    print("stop")

def right_forward():
    robot_controll.setTarget(0, 5200)
    robot_controll.setTarget(2, 7000)
    print("left foward")

def left_forward():
    robot_controll.setTarget(0, 5200)
    robot_controll.setTarget(2, 5000)
    print("right forward")

def right():
    robot_controll.setTarget(0, 6000)
    robot_controll.setTarget(2, 7000)
    print("left")

def left():
    robot_controll.setTarget(0, 6000)
    robot_controll.setTarget(2, 5000)
    print("right")

robot_controll = maestro.Controller()
robot_controll.setAccel(0,60)
robot_controll.setSpeed(0, 10)
robot_controll.setTarget(0, 6000)

cr = control_robot.robot()
spin_flag = False
cr.startSpin()
try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        # Convert color_frameimages to numpy arrays
        color = np.asanyarray(color_frame.get_data())
        # print("color")
        #fix lighting      	
        # gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
        # gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        # blur = cv2.blur(gray, (30,30))
        # diff = cv2.absdiff(color, blur)
        # diff = cv2.blur(color, (5,5))
        edge = color
        # print("blur")
        edge = edge[40:440,150:450]
        # gray = gray[40:440,150:450]
        # Read image
        # Set up the detector with default parameters.
        # Grayscale
        # Find Canny edges
        imghsv = cv2.cvtColor(edge, cv2.COLOR_BGR2HSV)
        # lower_blue = np.array([80,188,188])
        # upper_blue = np.array([150,255,255])
        # mask_blue = cv2.inRange(imghsv, lower_blue, upper_blue)
        # contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        lower_orange = np.array([0,89,202])
        upper_orange = np.array([40,150,255])
        mask_orange = cv2.inRange(imghsv, lower_orange, upper_orange)
        blurred = cv2.blur(mask_orange, (5,5))
        contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        total = 0
        x=0
        y=0
        if(not(len(contours) <2)):
            cr.stopSpin()
            spin_flag = True
        if(spin_flag):
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
        # cv2.drawContours(edge, contours, -1, (0, 255, 0), 1)
        
            if total == 0:
                total = 1
            yavg = int(x/total)
            xavg = int(y/total)
            cofy = int((150+450)/2)
            cofx = int(150)
            cof = (cofx, cofy)
            cv2.circle(edge, cof, 10, (255,0,0), 5)
            cog = (xavg,yavg)
            cv2.circle(edge, cog, 10, (255,0,0), 5)
            
            #TODO
            #move towards COG
            xdif = cof[0] - cog[0]
            ydif = cof[1] - cog[1]
            if ydif <0:
                stop()
            elif xdif <-10:
                if ydif >10:
                    left_forward()
                else:
                    right()
            elif xdif >10:
                if ydif > 10:
                    right_forward()
                else:
                    left()

            elif ydif > 0:
                move_forward()
            else:
                stop()
            if(total <3):
                stop()
        cv2.imshow('RealSense', edge)
        key = cv2.waitKey(1)
        if(key == 27):
            break
        




finally:
    robot_controll.setAccel(0,60)
    robot_controll.setSpeed(0, 10)
    robot_controll.setTarget(0, 6000)
    robot_controll.setTarget(2, 6000)
    # Stop streaming
    pipeline.stop()