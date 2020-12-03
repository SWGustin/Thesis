import os
import json 
import math 
import numpy as np

class BasisVectorError(Exception):
    pass

class Switch:
    def __init__(self):
        self._dutyCycle = 0
        self._frequency = 0
        self._basisVector = 0 + 0j

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
        self._basisVector = complex(x,y)

class PEL:
    def __init__(self, noOfSwitches, totalWidth, primaryDirection = 0):
        if noOfSwitches < 3:
            raise BasisVectorError("The minimum number of Low Voltage Elements for a additively closed space is 3")
        self._noOfSwitches = noOfSwitches
        self._thrust = 0+0j
        self._primaryDirection = primaryDirection
        self._initialized = False
        self._frequency = 100
        self._Switches = [Switch() for _ in range(self._noOfSwitches)]
        self._basis_angles = [((360/self._noOfSwitches * i) + self._primaryDirection)%360 for i in range(self._noOfSwitches)]
        self._basis_vectors = [(math.cos(math.radians(x)),math.sin(math.radians(x))) for x in self._basis_angles]
        
        #set complex basis vectors
        for s, bv in zip(self._Switches, self._basis_angles):
            s.frequency = self._frequency
            s.dutyCycle = 0
            s.basisVector = (math.cos(math.radians(bv)), math.sin(math.radians(bv))) 

    def __repr__(self):
        return str(self._thrust)

    @property
    def initialized(self):
        return self._initialized

    @initialized.setter
    def initialized(self, val):
        self._initialized = val
        if not self._initialized:
            self._thrust = -1

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, Hz):
        self._frequency = max(0,Hz)

    @property
    def thrust(self):
        return self._thrust
    
    @thrust.setter
    def thrust(self, val):
        correction = abs(val)
        if correction > 1:
            val = val / correction
            correction = 1
        self._thrust = val
    #this function must also action PELS
    #TODO: use a dictionary with vals from 1-> # of switches
    #hash those values and have the conversion matrices ready
    #use class attributes
        thrust_angle = np.degrees(np.angle(val))%180
        i = 0
        while i < len(self._basis_angles) and \
            (self._basis_angles[i+1] < np.angle(val)%180):
            i+=1
        print(self._basis_vectors)
        bv = [[self._basis_vectors[i][0], self._basis_vectors[i+1][0]],\
            [self._basis_vectors[i][1], self._basis_vectors[i+1][1]]]
        convert = np.linalg.inv(bv)
        local_thrust = np.matmul(convert, [np.real(self._thrust),np.imag(self._thrust)])
        local_thrust = local_thrust/np.linalg.norm(local_thrust)*correction
        for s, t in zip(self._Switches, local_thrust):
            s.dutyCycle = t


class ArPel:
    def __init__(self, config_file_name):
        config_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + '\\' + config_file_name
        with open(config_path, 'r') as f:
            data = json.load(f)
        
        _span = data['wing_geometry']['span']/2
        _root_chord = data['wing_geometry']['root_chord']
        _tip_chord = data['wing_geometry']['tip_chord']
        _sweep_angle = data['wing_geometry']['sweep_angle']
        _pel_width = data['pel_geometry']['overall_width']
        _pel_sep = data['pel_geometry']['seperation']
        _pel_cardinality = data['pel_geometry']['number_of_switches']
        _cardinal_offset = data['pel_geometry']['primary_direction']
        _set_back = data['wing_geometry']['set_back']

        _geometry = [(0,0)]
        # get corners of basic wing
        tip_offset = _span*math.tan(math.radians(_sweep_angle))
        _geometry.append((_span, tip_offset))
        _geometry.append((_span,_geometry[1][1]+_tip_chord))
        _geometry.append((0,_root_chord))

        # build an array of PELs
        _max_chord = max(_root_chord, tip_offset + _tip_chord)
        _no_of_rows = math.floor((_max_chord)/(_pel_width + _pel_sep))
        _no_of_columns = math.floor((_span - _pel_sep)/(_pel_width + _pel_sep)) 
        
        self._state_array = [[PEL(_pel_cardinality,_pel_width, _cardinal_offset)     
                            for _ in range(_no_of_columns)] for x in range(_no_of_rows)]

        _trailing_edge_sweep_angle = (tip_offset + _tip_chord - _root_chord)/_span
        
        #initialize elements that are in bounds
        for row in range(len(self._state_array)):
            row_set_back = row * (_pel_sep + _pel_width) + _set_back
            for col in range(len(self._state_array[0])):
                width = _pel_sep + col * (_pel_width + _pel_sep)
                self._state_array[row][col].initialized = \
                (math.tan(math.radians(_sweep_angle)) * width < row_set_back) \
                and _root_chord + width * _trailing_edge_sweep_angle > \
                row_set_back + _pel_width

        for row in self._state_array[::-1]:
            if not any(row):
                del(row)

    def __repr__(self):
        print("The array has initialized element:")
        for i in self._state_array:
            for p in i:
                print(p.initialized, end = ' ')
            print('')
        print()
        print("Thrust vectors are as follows")
        for i in self._state_array:
            print(i)
        return ''

    def get(self, var):
        x, y = var
        return self._state_array[y][x]


test = ArPel('config.json')
#print(test)
testt = test.get((1,1))
testt.thrust = 1+1j
#print(testt.thrust)
#print(abs(testt.thrust))

for i in testt._basis_angles:
    print(i)

for i in testt._Switches:
    print(i.basisVector)
    print(abs(i.basisVector))
