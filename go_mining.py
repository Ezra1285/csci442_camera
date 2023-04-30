
import pyrealsense2 as rs
import numpy as np
import maestro
import cv2
import control_robot
import line_crossing
import goto_area
robot_control = maestro.Controller()
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

robot_control.setAccel(0,60)
robot_control.setSpeed(0, 10)
robot_control.setTarget(0, 6000)
try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        color = np.asanyarray(color_frame.get_data())
        # goto_mine(color, line_color)
        goto_area.goto_mine(color, "blue")
        
        goto_area.goto_mine(color, "blue")
        
        cv2.imshow('RealSense', color)



finally:
    robot_control.setAccel(0,60)
    robot_control.setSpeed(0, 10)
    robot_control.setTarget(0, 6000)
    robot_control.setTarget(2, 6000)
    # Stop streaming
    pipeline.stop()