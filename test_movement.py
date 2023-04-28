import control_robot

robot = control_robot.robot()
for i in range(4):
    robot.right()
    # print("Loop " , i)
    # robot.waistRight()

robot.stop()