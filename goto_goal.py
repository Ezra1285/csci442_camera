import cv2
import control_robot
import pyrealsense2 as rs
import numpy as np
import control_robot

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

    robot = control_robot.robot()
    try:
        robot.headFullyLeft()
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue
            color_image = np.asanyarray(color_frame.get_data())    

            robot.headRight()
            # if(firstBoxFound and not color_found):
            #     color_found = handleColor(color_image) 
            
            # #  TODO: Return this color and make it work with baiden main program
            # if(color_found):
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