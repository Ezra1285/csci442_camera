import pyrealsense2 as rs
import numpy as np
import maestro
import cv2
import control_robot
import time

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
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

def spinRobot():
    count = 0
    while True:
        robot.spinInCircle()
        time.sleep(1)
        if(count == 13):
            break
        count +=1

robot = control_robot.robot()
#  red thresh
red_lower = np.array([136, 87, 111], np.uint8)
red_upper = np.array([180, 255, 255], np.uint8)
isFirst = True
# hog = cv2.HOGDescriptor()
# hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        # Convert color_frameimages to numpy arrays
        color = np.asanyarray(color_frame.get_data())
        # diff = cv2.blur(color, (5,5))
            
        print("STart")            
        hsvFrame = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
        print("end")
        
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
        print("Mask done")
        kernel = np.ones((5, 5), "uint8")
      
        # For red color
        red_mask = cv2.dilate(red_mask, kernel)
        res_red = cv2.bitwise_and(color, color, mask = red_mask)

        contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                color = cv2.rectangle(color, (x, y), 
                                        (x + w, y + h), 
                                        (0, 0, 255), 2)
                
                cv2.putText(color, "Red Colour", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 0, 255)) 
        #start line following
        # t_lower = 100  # Lower Threshold
        # t_upper = 150  # Upper threshold

        # # # Applying the Canny Edge filter
        # edge = cv2.Canny(diff, t_lower, t_upper)
        # edge = edge[40:440,150:450]
        # rows, cols = np.where(edge == 255) # extract row and column numbers for each pixel

        #  First find a human
        
        #  We can set a timer that stops this loops just incase it cant find the ice
        #  ex) wait 1 min before breaking if ice is not found
        #  TODO - follow color finding artical
        #       - break out once color has been found
        # if(isFirst):
        #     spinRobot()
        #     isFirst = False    

        cv2.imshow('RealSense', color)
        # cv2.imshow('RealSense', edge)
        key = cv2.waitKey(1)
        if(key == 27):
            break
        
finally:
    robot.stop()
    robot.close()
    # Stop streaming
    pipeline.stop()


# webcam = cv.VideoCapture(0)

# while(1):
#     _, frame = webcam.read()
#     frame = cv.resize(frame, None, fx=.75,fy=.75, interpolation=cv.INTER_AREA)
#     cv.imshow("Window", frame)
#     key = cv.waitKey(1)
#     if(key == 27):
#         cv.destroyAllWindows()
#         break