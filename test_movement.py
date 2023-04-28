import control_robot

robot = control_robot.robot()
for i in range(4):
    print("Loop " , i)
    robot.waistRight()

robot.stop()