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
        self._thrust = 0+0j
        self._primaryDirection = primaryDirection
        self._Switches = [Switch() for _ in range(self._noOfSwitches)]
        self._basis_vectors = [(360/self._noOfSwitches * i) + self._primaryDirection for i in range(self._noOfSwitches)]
        self._thrust = 0+0j
        self._initialized = False

    def __repr__(self):
        return str(self._thrust)

    @property
    def initialized(self):
        return self._initialized

    @initialized.setter
    def initialized(self, val):
        self._initialized = val
        if not self._initialized:
            self._thrust = None

    @property
    def dutyCycle(self):
        return self._dutyCycle

    @dutyCycle.setter
    def dutyCycle(self, dc):
        self._dutyCycle = min(max(0,dc),100)

        #TODO: updateto include handling of primary direction and for actioning PELS


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
        # get corners of basic wing1
        tip_offset = _span*math.tan(math.radians(_sweep_angle))
        _geometry.append((_span, tip_offset))
        _geometry.append((_span,_geometry[1][1]+_tip_chord))
        _geometry.append((0,_root_chord))

        # build an np.array of state vectors
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

test = ArPel('config.json')
print(test)