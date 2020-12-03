import os
import json 
import math 
import numpy as np

class BasisVectorError(Exception):
    pass

class Switch:
    def __init__(self, *,freq = 1000, pow = 0):
        self._dutyCycle = pow
        self._frequency = freq
        #self._basisVector = 0 + 0j

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

    def __repr__(self):
        return f'(power, frequency) = ({self._dutyCycle}, {self._frequency})'


class PEL:
    conversion_matrices = dict()

    @classmethod
    def calc_BVs(PEL, no_switches, primary_dir):
        _basis_angles = [((360/no_switches * i) + primary_dir)%360 for i in range(no_switches)]
        return [(math.cos(math.radians(x)),math.sin(math.radians(x))) for x in _basis_angles]
    
    @classmethod
    def calc_Conversion_matrix(PEL, V1,V2):
        bv = [[V1[0], V2[0]],[V1[1], V2[1]]]
        return np.linalg.inv(bv)

    @classmethod
    def addConversionMatrix(PEL, no_switches, primary_dir):
        outer_key = (no_switches, primary_dir)
        if outer_key in PEL.conversion_matrices.keys():
            return
        inner_keys = list(range(no_switches))
        inner_vals = []#this needs to be an array of conversion matrices
        BVs = PEL.calc_BVs(no_switches, primary_dir)
        for i in inner_keys:
            v1= BVs[i]
            v2 = BVs[((i+1)%no_switches)]
            inner_vals.append(PEL.calc_Conversion_matrix(v1,v2))
        
        inner_dict = dict(zip(inner_keys,inner_vals))

        PEL.conversion_matrices[outer_key] = inner_dict            

    def __init__(self, noOfSwitches, totalWidth, primaryDirection = 0):
        if noOfSwitches < 3:
            raise BasisVectorError("The minimum number of Low Voltage Elements for a additively closed space is 3")
        self._noOfSwitches = noOfSwitches
        self._thrust = 0+0j
        self._primaryDirection = primaryDirection
        self._initialized = False
        self._frequency = 100
        self._Switches = [Switch() for _ in range(self._noOfSwitches)]
        PEL.addConversionMatrix(self._noOfSwitches,self._primaryDirection)
        

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
        thrust_hash = (np.degrees(np.angle(val))%360)//(360/self._noOfSwitches)
        convert = PEL.conversion_matrices[(self._noOfSwitches, self._primaryDirection)][thrust_hash]
        local_thrust = np.matmul(convert, [np.real(self._thrust),np.imag(self._thrust)])
        local_thrust = local_thrust/np.linalg.norm(local_thrust)*correction
        for s, t in zip(self._Switches, local_thrust):
            s.dutyCycle = t

        for s in self._Switches:
            print(s)


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

# for i in testt._basis_angles:
#     print(i)

# for i in testt._Switches:
#     print(i.basisVector)
#     print(abs(i.basisVector))

test = PEL(3,10)
print(PEL.conversion_matrices)
