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

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

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
# bbox = (287, 23, 86, 320)
# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
#  Create an align object
align_to = rs.stream.color
align = rs.align(align_to)
# bbox = cv2.selectROI(color, False)
# Initialize tracker with first frame and bounding box
trackerNeedsInit = True
firstBoxFound = False
bbox = (287, 23, 86, 320)

try:
    robot.startSpin()
    # time.sleep(5)
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        # Convert color_frameimages to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        # color = np.asanyarray(color_frame.get_data())

        gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.5, 5)
            
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color.shape
        # diff = cv2.blur(color_image, (5,5))

         # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))

        blank = np.zeros_like(images)
        images = np.vstack((images,blank))

        hsvFrame = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)    
        kernel = np.ones((5, 5), "uint8")
        #  For face detection
        for (x,y,w,h) in faces:
            #  if faces exist then we stop the spin and init bbox and boolean vars
            robot.stopSpin()
            bbox = (x,y,w,h)
            firstBoxFound = True
            cv2.rectangle(color_image,(x,y),(x+w,y+h),(255,0,0),2)
            

        # For red color
        red_mask = cv2.dilate(red_mask, kernel)
        res_red = cv2.bitwise_and(color_image, color_image, mask = red_mask)
        #  possiable hack - have 3 programs one for each color
        #  then run the program bassed on color hunter chooses
        contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 2500):
                # robot.stopSpin()
                x, y, w, h = cv2.boundingRect(contour)
                # bbox = (x, y, w, h)
                # firstBoxFound = True
                color_image = cv2.rectangle(color_image, (x, y), 
                                        (x + w, y + h), 
                                        (0, 0, 255), 2)
                
                cv2.putText(color_image, "Red Colour", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 0, 255))
                break 

        #  TODO - start here refrencing the camera code
        #       -  finish getting the distance and go to 2 feet away if needed
        ok = False
        if(trackerNeedsInit and firstBoxFound):
            ok = tracker.init(color_image, bbox)
            trackerNeedsInit = False
        elif(not trackerNeedsInit):
            ok, bbox = tracker.update(color_image)
        
        images = cv2.rectangle(images, (320,400), (325, 410), (0, 0, 255), -1) #Red rectangle
        if ok:
            # Tracking success
            p1 = (int(bbox[0]/2), int(bbox[1]/2))
            p2 = (int((bbox[0] + bbox[2])/2), int((bbox[1] + bbox[3])/2))
            # cv2.rectangle(images, (p1),(p2), (255,0,0), 2, 1)
            curr_depth = depth_frame.get_distance(int((bbox[0]) + .5*bbox[2]), int(bbox[1] + .5*bbox[3]))
            print("Curr ", curr_depth)
            if(curr_depth > 2):
                print("Foward")
                robot.move_forward()
            else:
                print("Stopped")
                robot.stop()
        elif(not ok and firstBoxFound) :
            # Tracking failure
            cv2.putText(images, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            robot.stop()
            
        cv2.imshow('RealSense', color_image)
        # cv2.imshow('RealSense', edge)
        key = cv2.waitKey(1)
        if(key == 27):
            break
        
finally:
    robot.stop()
    robot.close()
    # Stop streaming
    pipeline.stop()
