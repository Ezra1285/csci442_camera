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
import maestro
import tkinter as tk
import numpy as np
import cv2
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
profile = pipeline.start(config)
time.sleep(3)
frames = pipeline.wait_for_frames()
depth_frame = frames.get_depth_frame()
color_frame = frames.get_color_frame()
color = np.asanyarray(color_frame.get_data())
# bbox = (287, 23, 86, 320)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
# print("Depth Scale is: " , depth_scale)


# We will be removing the background of objects more than
#  clipping_distance_in_meters meters away
# clipping_distance_in_meters = 1 #1 meter
# clipping_distance = clipping_distance_in_meters / depth_scale

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

# Uncomment the line below to select a different bounding box
# bbox = cv2.selectROI(color, False)

# Initialize tracker with first frame and bounding box
robot_controll = maestro.Controller()
robot_controll.setAccel(0,60)
robot_controll.setSpeed(0, 10)
robot_controll.setTarget(0, 6000)


counter = 0
motor_value = 6000
try:
    while True:
        
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        color = np.asanyarray(color_frame.get_data())
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap)) 
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        counter += 1
        key = cv2.waitKey(1)
        
        if(key == 27):
            break
        

finally:
    # Stop streaming
    robot_controll.setTarget(0, 6000)
    robot_controll.close()
    pipeline.stop()