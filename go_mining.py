
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

robot_control.setAccel(0,60)
robot_control.setSpeed(0, 10)
robot_control.setTarget(0, 6000)
class ctrl_methods():
    def __init__(self) -> None:
        self.method_num = 0
            
    def control_methods(self):
        ret = "not done"
        if(self.method_num ==0):
            ret = goto_area.goto_mine(color, "blue")
        elif(self.method_num ==1):
            ret = goto_area.goto_mine(color, "orange")
        else:
            raise Exception("Done!")
        if(ret == "done"):
            method_num +=1
ctrlr = ctrl_methods()
try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        color = np.asanyarray(color_frame.get_data())
        # goto_mine(color, line_color)
        ctrlr.control_methods()
        cv2.imshow('RealSense', color)



finally:
    robot_control.setAccel(0,60)
    robot_control.setSpeed(0, 10)
    robot_control.setTarget(0, 6000)
    robot_control.setTarget(2, 6000)
    # Stop streaming
    pipeline.stop()