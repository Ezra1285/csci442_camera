import pyrealsense2 as rs
import numpy as np
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


def move_forward():
    print("forward")

def stop():
    print("stop")

def left_foward():
    print("left foward")

def right_forward():
    print("right forward")

def left():
    print("left")

def right():
    print("right")



try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convert color_frameimages to numpy arrays
        color = np.asanyarray(color_frame.get_data())
        #fix lighting      	
        # gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
        # gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        # blur = cv2.blur(gray, (30,30))
        # diff = cv2.absdiff(color, blur)
        diff = cv2.blur(color, (5,5))
        # thresh = cv2.inRange(diff, 100, 150)
        #start line following
        t_lower = 100  # Lower Threshold
        t_upper = 150  # Upper threshold

        # Applying the Canny Edge filter
        edge = cv2.Canny(diff, t_lower, t_upper)
        #find COG
        total = 0
        x=0
        y=0
        
        for i in range(50,480-50):
            for j in range(150, 640-150):
                if(edge[i,j] > 100):
                    x += i
                    y += j
                    total +=1
        if total == 0:
            total = 1
        yavg = x/total
        xavg = y/total
        cv2.rectangle(edge,(150,50),(640-150,430),(155,155,155),5)
        cv2.circle(edge, (int(xavg), int(yavg)), 15, (155,0,0), 10)
        cofy = int(((480-100)/2)+50) +150
        cofx = int(((640-300)/2)+125)
        cof = (cofx, cofy)
        cv2.circle(edge, cof, 10, (255,0,0), 5)
        cog = (xavg,yavg)

        
        #TODO
        #move towards COG
        xdif = cog[0] - cof[0]
        ydif = cog[1] - cof[1]

        if xdif <-10:
            if ydif >10:
                left_foward()
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

        cv2.imshow('RealSense', edge)
        key = cv2.waitKey(1)
        if(key == 27):
            break
        




finally:

    # Stop streaming
    pipeline.stop()