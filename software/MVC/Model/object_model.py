import os
import json 
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
    def __init__(self, noOfSwitches, totalWidth, primaryDirection = 0):
        if noOfSwitches < 3:
            raise BasisVectorError("The minimum number of Low Voltage Elements for a additively closed space is 3")
        self._noOfSwitches = noOfSwitches
        self._totalWidth = totalWidth
        self._angle = 0
        self._dutyCycle = 0
        self._primaryDirection = primaryDirection
        self._Switches = [Switch() for _ in range(self._noOfSwitches)]
        self._basis_vectors = [(360/self._noOfSwitches * i) + self._primaryDirection for i in range(self._noOfSwitches)]
    
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


class ArPel:
    def __init__(self, config_file_name):
        config_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + '\\' + config_file_name
        with open(config_path, 'r') as f:
            data = json.load(f)
        self._span = data['wing_geometry']['span']/2
        self._root_chord = data['wing_geometry']['root_chord']
        self._tip_chord = data['wing_geometry']['tip_chord']
        self._sweep_angle = data['wing_geometry']['sweep_angle']
        self._pel_width = data['pel_geometry']['overall_width']
        self._pel_sep = data['pel_geometry']['seperation']
        self._pel_cardinality = data['pel_geometry']['number_of_switches']
        self._cardinal_offset = data['pel_geometry']['primary_direction']

        self._geometry = [(0,0)]
        # get corners of basic wing1
        tip_offset = self._span*math.tan(math.radians(self._sweep_angle))
        self._geometry.append((self._span, tip_offset))
        self._geometry.append((self._span,self._geometry[1][1]+self._tip_chord))
        self._geometry.append((0,self._root_chord))

        # build an np.array of state vectors
        max_span = self._span//2
        max_chord = max(self._root_chord, tip_offset + self._tip_chord)
        no_of_rows = math.floor((max_chord)/(self._pel_width + self._pel_sep))
        no_of_columns = math.floor((max_span - self._pel_sep)/(self._pel_width + self._pel_sep)) 
        self._state_array = [[PEL(self._pel_cardinality,self._pel_width, self._cardinal_offset) 
                            for _ in range(no_of_columns)] for x in range(no_of_rows)]


test = ArPel('config.json')