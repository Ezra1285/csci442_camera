import cv2
import control_robot
import pyrealsense2 as rs
import numpy as np
import control_robot
import time

# #  Red thresh
# red_lower = np.array([136, 87, 111], np.uint8)
# red_upper = np.array([180, 255, 255], np.uint8)
# #  Green thresh
# green_lower = np.array([49, 60, 128], np.uint8)
# green_upper = np.array([86, 255, 255], np.uint8)
# # yellow
# yellow_lower = np.array([20, 102, 91], np.uint8)
# yellow_upper = np.array([52, 255, 255], np.uint8)

green_lower = np.array([27, 91, 106], np.uint8) 
green_upper = np.array([88, 173, 197], np.uint8) 

kernel = np.ones((5, 5), "uint8")
color_found = ""
robot = control_robot.robot()

def handleColor(color_image):
    global color_found
    # global robot
    hsvFrame = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
    # # For red color
    # red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    # red_mask = cv2.dilate(red_mask, kernel)
    # res_red = cv2.bitwise_and(color_image, color_image, mask = red_mask)
    # contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if(area > 3200):
    #         robot.stopSpin()
    #         print("pink")
    #         color_found = "pink"
    #         x, y, w, h = cv2.boundingRect(contour)
    #         color_image = cv2.rectangle(color_image, (x, y), 
    #                                 (x + w, y + h), 
    #                                 (0, 0, 255), 2)
            
    #         cv2.putText(color_image, "Pink Colour", (x, y),
    #                     cv2.FONT_HERSHEY_SIMPLEX, 1.0,
    #                     (0, 0, 255))
    #         return color_found, False   

    #  For green
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
    # green_mask = cv2.dilate(green_mask, kernel)
    # res_green = cv2.bitwise_and(color_image, color_image, mask = green_mask)
    contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 3200):
            print("AREA is ", area)
            robot.stopSpin()
            color_found = "green"
            print("green")
            x, y, w, h = cv2.boundingRect(contour)
            color_image = cv2.rectangle(color_image, (x, y), 
                                       (x + w, y + h),
                                       (0, 255, 0), 2)
              
            cv2.putText(color_image, "Green Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        1.0, (0, 255, 0))
            # return color_found, False
    
    #  For yellow
    # yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)
    # yellow_mask = cv2.dilate(yellow_mask, kernel)
    # res_yellow = cv2.bitwise_and(color_image, color_image, mask = yellow_mask)
    # contours, hierarchy = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if(area > 3200):
    #         robot.stopSpin()
    #         print("Yellow")
    #         color_found = "yellow"
    #         x, y, w, h = cv2.boundingRect(contour)
    #         color_image = cv2.rectangle(color_image, (x, y),
    #                                    (x + w, y + h),
    #                                    (255, 0, 0), 2)
              
    #         cv2.putText(color_image, "Yellow Colour", (x, y),
    #                     cv2.FONT_HERSHEY_SIMPLEX,
    #                     1.0, (255, 0, 0))
    #         return color_found, False        
    return color_found, True

def findColor():
    #======================================
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
#====================================== 
    needToFindColor = True
    global color_found
    count = 0
    # global robot
    try:
        robot.startSpin()
        while True:
            frames = pipeline.wait_for_frames()
            if(count < 25):
                count += 1
                continue
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue
            color_image = np.asanyarray(color_frame.get_data())    

            if(needToFindColor):
                # color_found, needToFindColor = handleColor(color_image) 
                handleColor(color_image) 
            
            # if(not needToFindColor):
            #     robot.move_forward()
            #     time.sleep(1)
            #     robot.stop()
            #     return color_found

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
        

findColor()