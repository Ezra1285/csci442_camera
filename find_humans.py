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

#  red thresh
red_lower = np.array([136, 87, 111], np.uint8)
red_upper = np.array([180, 255, 255], np.uint8)

# Start streaming
profile = pipeline.start(config)
time.sleep(2)
robot = control_robot.robot()

#  Set up depth to find how far our person with ice is.
frames = pipeline.wait_for_frames()
depth_frame = frames.get_depth_frame()
color_frame = frames.get_color_frame()
color = np.asanyarray(color_frame.get_data())
tracker = cv2.TrackerKCF_create()
bbox = (287, 23, 86, 320)
# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
#  clipping_distance_in_meters meters away
clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale
#  Create an align object
align_to = rs.stream.color
align = rs.align(align_to)
bbox = cv2.selectROI(color, False)
# Initialize tracker with first frame and bounding box
ok = tracker.init(color, bbox)
is_start_distance = True


def findCurrDepth():
    pass

try:
    robot.startSpin()
    time.sleep(5)
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        # Convert color_frameimages to numpy arrays
        color = np.asanyarray(color_frame.get_data())
        # diff = cv2.blur(color, (5,5))
                        
        hsvFrame = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
        
        kernel = np.ones((5, 5), "uint8")

        # For red color
        red_mask = cv2.dilate(red_mask, kernel)
        res_red = cv2.bitwise_and(color, color, mask = red_mask)
        #  possiable hack - have 3 programs one for each color
        #  then run the program bassed on color hunter chooses
        contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 1100):
                robot.stopSpin()
                print("We found red")
                x, y, w, h = cv2.boundingRect(contour)
                color = cv2.rectangle(color, (x, y), 
                                        (x + w, y + h), 
                                        (0, 0, 255), 2)
                
                cv2.putText(color, "Red Colour", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 0, 255))
                break 
   
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