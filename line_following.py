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
    robot_controll.setTarget(0, 5000)
    print("forward")

def stop():
    robot_controll.setTarget(2, 6000)
    robot_controll.setTarget(0, 6000)
    print("stop")

def left_forward():
    robot_controll.setTarget(0, 5200)
    robot_controll.setTarget(2, 7000)
    print("left foward")

def right_forward():
    robot_controll.setTarget(0, 5200)
    robot_controll.setTarget(2, 5000)
    print("right forward")

def left():
    robot_controll.setTarget(0, 6000)
    robot_controll.setTarget(2, 7000)
    print("left")

def right():
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
        print("color")
        #fix lighting      	
        # gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
        # gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        # blur = cv2.blur(gray, (30,30))
        # diff = cv2.absdiff(color, blur)
        diff = cv2.blur(color, (5,5))
        print("blur")
        # thresh = cv2.inRange(diff, 100, 150)
        #start line following
        t_lower = 100  # Lower Threshold
        t_upper = 150  # Upper threshold

        # Applying the Canny Edge filter
        print("edge")
        edge = cv2.Canny(diff, t_lower, t_upper)
        #find COG
        total = 0
        x=0
        y=0
        print("loop")
 
        crop_center(edge,100,450)
        edge = edge[60:420,100:400]
        rows, cols = np.where(edge == 255) # extract row and column numbers for each pixel

        # rows, cols = transform.xy(edge.transform, rows, cols)
        # np.set_printoptions(threshold=12000)
        # for i in range(100,480-100):
        #     for j in range(180, 640-180):
        #         print(edge[i,j])
        #         if(edge[i,j] > 100):
        #             x += i
        #             y += j
        #             total +=1
        #         pass
        x = rows.sum()
        y = cols.sum()
        print(x)
        print(y)
        total = rows.size
        print(total)
        if total == 0:
            total = 1
        yavg = x/total
        xavg = y/total
        cv2.rectangle(edge,(180,100),(640-10,480-100),(155,155,155),5)
        cv2.circle(edge, (int(xavg), int(yavg)), 15, (155,0,0), 10)
        cofy = int((420-60)/2)
        cofx = int(((300)/2))
        cof = (cofx, cofy)
        cv2.circle(edge, cof, 10, (255,0,0), 5)
        cog = (xavg,yavg)

        
        #TODO
        #move towards COG
        xdif = cof[0] - cog[0]
        ydif = cof[1] - cog[1]
        if ydif <0:
            stop()
        elif xdif <-35:
            if ydif >10:
                left_forward()
            else:
                right()
        elif xdif >35:
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