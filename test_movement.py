import control_robot
import maestro
import time


bot = maestro.Controller()

bot.setAccel(0,60)
bot.setSpeed(0, 10)
bot.setTarget(0, 6000)

bot.setTarget(2, 7000)
# bot.setTarget(0, 7000)

time.sleep(5)

bot.setTarget(0, 6000)
bot.setTarget(2, 6000)
bot.close()
# robot = control_robot.robot()
# for i in range(10):
# robot.right_forward()
# robot.right()
# robot.right_forward()
# robot.right()
    # print("Loop " , i)
    # robot.waistRight()

# robot.stop()