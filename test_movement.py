import control_robot
import maestro


bot = maestro.Controller()

bot.setAccel(0,60)
bot.setSpeed(0, 10)
bot.setTarget(0, 6000)

bot.setTarget(2, 6800)
# robot = control_robot.robot()
# for i in range(10):
# robot.right_forward()
# robot.right()
# robot.right_forward()
# robot.right()
    # print("Loop " , i)
    # robot.waistRight()

# robot.stop()