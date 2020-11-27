class LVE:
    def __init__(self):
        self._dutyCycle = 0
        self._frequency = 0
        self._basisVector = (0,0)

    @property
    def dutyCycle(self):
        return self._dutyCycle
    
    @dutyCycle.setter
    def dutyCycle(self, dc):
        self._dutyCycle = max(min(100, dc), 0)

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, Hz):
        self._frequency = Hz

    @property
    def basisVector(self):
        return self._basisVector

    @basisVector.setter
    def basisVector(self, vector):
        try:
            x,y = vector
        except ValueError:
            raise ValueError (f'{len(vector)} dimensions given of 2 expected')
        self._basisVector = vector

class BasisVectorError(Exception):
    pass

class PEL:
    def __init__(self,noOfLVE):
        if noOfLVE < 3:
            raise BasisVectorError("The minimum number of LVE for a additively complete space is 3")
        self._noOfLVE = noOfLVE
        self._side_length = float('inf')
        self._gap = float('inf')
        self._angle = 0
        self._dutyCycle = 0
        self._primaryDirection = 0
        self._LVEs = [LVE() for _ in range(self._noOfLVE)]
        
    @property
    def dutyCycle(self):
        return self._dutyCycle

    @dutyCycle.setter
    def dutyCycle(self, dc):
        self._dutyCycle = min(max(0,dc),100)

    @property
    def noOfLVE(self):
        return self._noOfLVE

    @noOfLVE.setter
    def noOfLVE(self, noOfLVE):
        self._noOfLVE = noOfLVE

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle % 360
        #TODO: updateto include handling of primary direction and for actioning PELS
    
    @property
    def primaryDirection(self):
        return self._primaryDirection
    
    @primaryDirection.setter
    def primaryDirection(self, pd):
        self._primaryDirection = pd % 360

    @property
    def LVEs(self):
        return self._LVEs

    #TODO: add properties and setter for un_added variables above
    