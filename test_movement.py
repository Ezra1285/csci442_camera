import control_robot
import maestro
import time


# bot = maestro.Controller()

# bot.setAccel(0,60)
# bot.setSpeed(0, 10)
# bot.setTarget(0, 6000)

# bot.setTarget(2, 7000)
# bot.setTarget(0, 7000)

# time.sleep(5)

# bot.setTarget(0, 6000)
# bot.setTarget(2, 6000)
# bot.close()

robot = control_robot.robot()
robot.spinInCircle()
time.sleep(5)
# for i in range(8):
#     robot.waistRight()

robot.stop()