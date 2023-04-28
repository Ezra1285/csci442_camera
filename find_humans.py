import pyrealsense2 as rs
import numpy as np
import maestro
import cv2

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

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        # Convert color_frameimages to numpy arrays
        color = np.asanyarray(color_frame.get_data())
        diff = cv2.blur(color, (5,5))
            
        #start line following
        t_lower = 100  # Lower Threshold
        t_upper = 150  # Upper threshold

        # # Applying the Canny Edge filter
        edge = cv2.Canny(diff, t_lower, t_upper)
        edge = edge[40:440,150:450]
        rows, cols = np.where(edge == 255) # extract row and column numbers for each pixel

        #  First find a human
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        (humans, _) = hog.detectMultiScale(color, winStride=(10, 10),
        padding=(32, 32), scale=1.1)


            
        cv2.imshow('RealSense', color)
        # cv2.imshow('RealSense', edge)
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


# webcam = cv.VideoCapture(0)

# while(1):
#     _, frame = webcam.read()
#     frame = cv.resize(frame, None, fx=.75,fy=.75, interpolation=cv.INTER_AREA)
#     cv.imshow("Window", frame)
#     key = cv.waitKey(1)
#     if(key == 27):
#         cv.destroyAllWindows()
#         break