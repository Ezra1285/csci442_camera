import control_robot

robot = control_robot.robot()
for i in range(10):
    robot.right_forward()
    # print("Loop " , i)
    # robot.waistRight()

robot.stop()