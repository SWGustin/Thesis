import math 

class BasisVectorError(Exception):
    pass

class Switch:
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

class PEL:
    def __init__(self,noOfSwitches, totalWidth, primaryDirection = 0):
        if noOfSwitches < 3:
            raise BasisVectorError("The minimum number of Low Voltage Elements for a additively complete space is 3")
        self._noOfSwitches = noOfSwitches
        self._totalWidth = totalWidth
        self._angle = 0
        self._dutyCycle = 0
        self._primaryDirection = primaryDirection
        self._Switches = [Switch() for _ in range(self._noOfSwitches)]
        self._cardinalDirections = [(360/self._noOfSwitches * i) + self._primaryDirection for i in range(self._noOfSwitches)]
    
    @property
    def noOfSwitches(self):
        return self._noOfSwitches

    @property
    def totalWidth(self):
        return self._totalWidth

    @property
    def primaryDirection(self):
        return self._primaryDirection

    @property
    def Switches(self):
        return self._Switches

    @property
    def cardinalDirections(self):
        return self._cardinalDirections

    @property
    def dutyCycle(self):
        return self._dutyCycle

    @dutyCycle.setter
    def dutyCycle(self, dc):
        self._dutyCycle = min(max(0,dc),100)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle % 360

        #TODO: updateto include handling of primary direction and for actioning PELS

class ArPEl:
    def __init__(self):
        self._base_chord = 0
        self._tip_chord = 0
        self._span = 0
        self._leading_angle = 0
        self._pel_spacing = float('inf')
        self._geometry = []
        self._pels = [[]]

    @property
    def geometry(self):
        return self._geometry

    # @geometry.setter
    # def geometry(self,points):
    #     self._geometry = [[(x,y) for x,y in point ]for point in points]
        
    @geometry.setter
    def geometry(self, values):
        try:
            base_chord, tip_chord, span, leading_angle = values
        except ValueError:
            raise ValueError("Pass all required values")
        self._geometry = [(0,0)]
        self._geometry.append((span, span*math.tan(math.radians(leading_angle))))
        self._geometry.append((span,self._geometry[1][1]+tip_chord))
        self._geometry.append((0,base_chord))

    #TODO: add unadded setters and calculate array of pels   