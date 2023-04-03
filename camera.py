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
tracker = cv2.TrackerKCF_create()
bbox = (287, 23, 86, 320)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)


# We will be removing the background of objects more than
#  clipping_distance_in_meters meters away
clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

# Uncomment the line below to select a different bounding box
bbox = cv2.selectROI(color, False)

# Initialize tracker with first frame and bounding box
ok = tracker.init(color, bbox)

is_start_distance = True

# win = tk.Tk()
# keys = keyboardControl.KeyControl(win)
robot_controll = maestro.Controller()
robot_controll.setAccel(0,10)
robot_controll.setSpeed(0, 10)
robot_controll.setTarget(0, 6000)
# robot_controll.setRange(0,1, 100)


# win.bind('<Up>', robot_controll.arrow)
# win.bind('<Left>', robot_controll.arrow)
# win.bind('<Down>', robot_controll.arrow)
# win.bind('<Right>', robot_controll.arrow)
# win.bind('<space>', robot_controll.arrow)
# win.bind('<z>', keys.waist)
# win.bind('<c>', keys.waist)
# win.bind('<w>', keys.head)
# win.bind('<s>', keys.head)
# win.bind('<a>', keys.head)
# win.bind('<d>', keys.head)
# win.mainloop()
# keys = keyboardControl.KeyControl(win)    
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

        blank = np.zeros_like(images)
        
        images = np.vstack((images,blank))

        images = cv2.resize(images, (int(images.shape[1]*.5), int(images.shape[0]*.5)), fx=.1, fy=.1)
        # Show images
        ok, bbox = tracker.update(color)
        
        images = cv2.rectangle(images, (320,400), (325, 410), (0, 0, 255), -1) #Red rectangle
        if ok:
            # Tracking success
            p1 = (int(bbox[0]/2), int(bbox[1]/2))
            p2 = (int((bbox[0] + bbox[2])/2), int((bbox[1] + bbox[3])/2))
            cv2.rectangle(images, (p1),(p2), (255,0,0), 2, 1)
            
            curr_depth = depth_frame.get_distance(int((bbox[0]) + .5*bbox[2]), int(bbox[1] + .5*bbox[3]))
            if(is_start_distance):
                start_depth = curr_depth
                is_start_distance = False
            #  Check is distance is closer or further and the move foward or back
            if(start_depth > curr_depth):
                # Foward
                print("FOWARDDDD")
                if(motor_value > 700):
                    motor_value = 7000
                else:
                    motor_value += 500
                # robot_controll.motors += 200
                # if(robot_controll.motors > 7900):
                #     robot_controll.motors = 7900
                # robot_controll.tango.setTarget(1, robot_controll.motors)
            else:
                # back
                print("BACKKKK")
                if(motor_value < 6000):
                    motor_value = 6000
                else:
                    motor_value -= 500
                # robot_controll.motors -= 200
                # if(robot_controll.motors < 1510):
                #     robot_controll.motors = 1510
                # robot_controll.tango.setTarget(1, robot_controll.motors)
            robot_controll.setTarget(0, motor_value)
            print(curr_depth)
            blue_start_x = int(300 - (curr_depth*10))
            blue_start_y = int(380 - (curr_depth*10))
            images = cv2.rectangle(images, (blue_start_x,blue_start_y), (blue_start_x+55,blue_start_y+1), (255, 0, 0), -1) #Blue rectangle

            
        else :
            # Tracking failure
            cv2.putText(images, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv2.putText(images, 'KCF' + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     
        # Display FPS on frame
        #cv2.putText(color, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        counter += 1
        key = cv2.waitKey(1)
        
        if(key == 27):
            break
        

finally:
    # Stop streaming
    robot_controll.close()
    pipeline.stop()