import maestro

class robot:
    
    def __init__(self):
        self.robot_controll = maestro.Controller()
        self.robot_controll.setAccel(0,60)
        self.robot_controll.setSpeed(0, 10)
        self.robot_controll.setTarget(0, 6000)
        self.waist = 6000

    # def stopRobot(self):
    #     self.robot_controll.setAccel(0,60)
    #     self.robot_controll.setSpeed(0, 10)
    #     self.robot_controll.setTarget(0, 6000)
    
    #  Handle body movement
    def move_forward(self):
        self.robot_controll.setTarget(2, 6000)
        self.robot_controll.setTarget(0, 5250)
        print("forward")

    def stop(self):
        self.robot_controll.setTarget(2, 6000)
        self.robot_controll.setTarget(0, 6000)
        print("stop")

    def right_forward(self):
        self.robot_controll.setTarget(0, 5200)
        self.robot_controll.setTarget(2, 7000)
        print("left foward")

    def left_forward(self):
        self.robot_controll.setTarget(0, 5200)
        self.robot_controll.setTarget(2, 5000)
        print("right forward")

    def right(self):
        self.robot_controll.setTarget(0, 6000)
        self.robot_controll.setTarget(2, 7000)
        print("left")

    def left(self):
        self.robot_controll.setTarget(0, 6000)
        self.robot_controll.setTarget(2, 5000)
        print("right")

    #  handle waist movement
    def waistRight(self):
        self.waist += 200
        if(self.body > 7900):
            self.body = 7900
        self.robot_controll.setTarget(0, self.waist)

    def waistRight(self):
        self.waist -= 200
        if(self.body < 1510):
            self.body = 1510
        self.robot_controll.setTarget(0, self.waist)