import control_robot

robot = control_robot.robot()
# for i in range(10):
robot.right_forward()
robot.right()
robot.right_forward()
robot.right()
    # print("Loop " , i)
    # robot.waistRight()

robot.stop()