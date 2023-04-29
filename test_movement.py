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
count = 0
while True:
    robot.spinInCircle()
    time.sleep(1)
    if(count == 10):
         break
    count +=1

robot.stop()