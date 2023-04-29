import maestro

class robot:
    
    def __init__(self):
        self.robot_controll = maestro.Controller()
        self.robot_controll.setAccel(0,60)
        self.robot_controll.setSpeed(0, 10)
        self.robot_controll.setTarget(0, 6000)
        self.waist = 6000
        self.headTurn = 6000
        self.headTilt = 6000
        self.turn = 6000

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
        # self.turn -= 200
        # if(self.turn <2110):
        #     self.turn = 2110
        # print(self.turn)
        # self.robot_controll.setTarget(2, self.turn)
        self.robot_controll.setTarget(0, 6000)
        self.robot_controll.setTarget(2, 5000)
        print("right")

    #  handle waist movement
    def waistRight(self):
        self.waist += 200
        if(self.waist > 7900):
            self.waist = 7900
        print("waist ", self.waist)
        self.robot_controll.setTarget(2, self.waist)

    def waistLeft(self):
        self.waist -= 200
        if(self.waist < 1510):
            self.waist = 1510
        self.robot_controll.setTarget(2, self.waist)

    #  handle head movement(Working)
    def headRight(self):
        self.headTurn += 200
        if(self.headTurn > 7900):
            self.headTurn = 7900
        self.robot_controll.setTarget(3, self.headTurn)

    def headLeft(self):
        self.headTurn -= 200
        if(self.headTurn < 1510):
            self.headTurn = 1510
        self.robot_controll.setTarget(3, self.headTurn)

    def headUp(self):
        self.headTilt += 200
        if(self.headTilt > 7900):
            self.headTilt = 7900
        self.robot_controll.setTarget(4, self.headTilt)

    def headDown(self):
        self.headTilt -= 200
        if(self.headTilt < 1510):
            self.headTilt = 1510
        self.robot_controll.setTarget(4, self.headTilt)