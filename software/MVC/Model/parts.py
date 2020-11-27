class LVE:
    def __init__(self):
        self.dutyCycle = 0
        self.frequency = 0

    @property
    def dutyCycle(self):
        return self.dutyCycle
    
    @DutyCycle.setter
    def dutyCycle(self, DC):
        self.dutyCycle = max(min(0, DC), 100)

    @property
    def frequency(self):
        return self.frequency

    @Frequency.setter
    def frequency(self, Hz):
        self.frequency = Hz


class PEL:
    def __init__(self,noOfLVE):
        self.noOfLVE = noOfLVE
        self.dutyCycle = 0
        self.angle = 0
        self.primaryDirection = 0
        LVEs = [LVE() for _ in range(self.noOfLVE)]

    @property
    def dutyCycle(self):
        return self.dutyCycle

    @dutyCycle.setter
    def dutyCycle(self, dc):
        self.dutyCycle = min(max(100,dc),0)

    @property
    def noOfLVE(self):
        return self.noOfLVE

    @noOfLVE.setter
    def noOfLVE(self, noOfLVE):
        self.noOfLVE = noOfLVE

    @property
    def angle(self):
        return self.angle

    @angle.setter
    def angle(self, angle):
        self.angle = angle % 360
    
    @property
    def primaryDirection(self):
        return self.primaryDirection
    
    @primaryDirection.setter
    def primaryDirection(self, pd):
        self.primaryDirection = pd % 360