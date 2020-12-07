import os
import json 
import numpy as np
import time

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
        return [(np.cos(np.radians(x)),np.sin(np.radians(x))) for x in _basis_angles]
    
    @classmethod
    def calc_Conversion_matrix(PEL, V1,V2):
        bv = [[V1[0], V2[0]],[V1[1], V2[1]]]
        return np.linalg.inv(bv)

    @classmethod
    def addConversionMatrix(PEL, no_switches, primary_dir):
        outer_key = (no_switches, primary_dir)
        if outer_key in PEL.conversion_matrices.keys():
            return
        inner_vals = []#this needs to be an array of conversion matrices
        BVs = PEL.calc_BVs(no_switches, primary_dir)
        for i in range(no_switches):
            v1= BVs[i]
            v2 = BVs[((i+1)%no_switches)]
            inner_vals.append(PEL.calc_Conversion_matrix(v1,v2))
        
        PEL.conversion_matrices[outer_key] = inner_vals

    def __init__(self, ID, noOfSwitches, totalWidth, primaryDirection = 0):
        if noOfSwitches < 3:
            raise BasisVectorError("The minimum number of Low Voltage Elements for a additively closed space is 3")
        self._noOfSwitches = noOfSwitches
        self._thrust = 0+0j
        self._primaryDirection = primaryDirection
        self._initialized = True
        self._frequency = 100
        self._switches = [Switch() for _ in range(self._noOfSwitches)]
        self._total_width = totalWidth
        self._ID = ID
        PEL.addConversionMatrix(self._noOfSwitches,self._primaryDirection)

    def __repr__(self):
        return str(self._thrust)

    @property
    def ID(self):
        return self._ID

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
        thrust_hash = int((np.degrees(np.angle(val))%360)//(360/self._noOfSwitches))
        convert = PEL.conversion_matrices[(self._noOfSwitches, self._primaryDirection)][thrust_hash]
        local_thrust = np.matmul(convert, [self._thrust.real,self._thrust.imag])
        local_thrust = local_thrust/np.linalg.norm(local_thrust)*correction
        for s, t in zip(self._switches, local_thrust):
            s.dutyCycle = t

    @property
    def switches(self):
        return self._switches

class ArPel:
    def __init__(self, config_file_name):
        config_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  
        config_path = '\\'.join(config_path.split('\\')[:-1]) + '\\config\\' + config_file_name
        with open(config_path, 'r') as f:
            data = json.load(f)
        
        self._current_row = 0
        self._current_col = -1

        _tip_chord = data['wing_geometry']['tip_chord']
        _sweep_angle = data['wing_geometry']['sweep_angle']
        _pel_cardinality = data['pel_geometry']['number_of_switches']
        _cardinal_offset = data['pel_geometry']['primary_direction']
        self._span = data['wing_geometry']['span']/2
        self._root_chord = data['wing_geometry']['root_chord']
        self._pel_width = data['pel_geometry']['overall_width']
        self._pel_sep = data['pel_geometry']['seperation']

        self._set_back = data['wing_geometry']['set_back']

        self._geometry = [(0,self._root_chord)]
        # get corners of basic wing
        tip_offset = self._span*np.tan(np.radians(_sweep_angle))
        self._geometry.append((self._span, self._root_chord - tip_offset))
        self._geometry.append((self._span,self._geometry[1][1]-_tip_chord))
        self._geometry.append((0,0))

        # build an array of PELs
        _max_chord = max(self._root_chord, tip_offset + _tip_chord)
        self._no_of_rows = int(np.floor((_max_chord)/(self._pel_width + self._pel_sep)))
        self._no_of_columns = int(np.floor((self._span - self._pel_sep)/(self._pel_width + self._pel_sep)))
        
        #create matrix of PELs
        self._state_array = []
        tan_trailing_angle = (self._root_chord - tip_offset - _tip_chord )/self._span
        tan_leading_angle = np.tan(np.radians(_sweep_angle))
        #initialize elements that are in bounds
        row_set_back = self._set_back - self._pel_sep - self._pel_width
        self._no_of_pels = 0
        for rn in range(self._no_of_rows):
            row = []
            row_set_back += self._pel_sep + self._pel_width
            width = -self._pel_width
            for _ in range(self._no_of_columns):
                width += self._pel_width + self._pel_sep
                if ((tan_leading_angle * width < row_set_back) \
                    and ((width * tan_trailing_angle) < \
                    self.root_chord - row_set_back - self._pel_width)):
                        row.append(PEL(self._no_of_pels, _pel_cardinality, self._pel_width, _cardinal_offset))
                        self._no_of_pels +=1
            self.state_array.append(row)

        for row in self._state_array[::-1]:
            if not any(row):
                del(row)

    def __getitem__(self, indx):
            x,y = indx
            return self.state_array[y][x]
            
    def __iter__(self):
        return self

    def __next__(self):
        try:
            self._current_col += 1
            return self.state_array[self._current_row][self._current_col]
        except IndexError:
            try:
                self._current_row += 1
                self._current_col = 0
                return self.state_array[self._current_row][self._current_col] 
            except IndexError:
                self._current_row = 0
                self._current_col = -1
                raise StopIteration

    @property
    def state_array(self):
        return self._state_array

    @property
    def pel_width(self):
        return self._pel_width

    @property
    def root_chord(self):
        return self._root_chord

    @property
    def pel_sep(self):
        return self._pel_sep

    @property
    def setback(self):
        return self._set_back
    
    @property
    def geometry(self):
        return self._geometry
        
    @property
    def span(self):
        return self._span

    @property
    def no_of_rows(self):
        return self._no_of_rows

    @property
    def no_of_columns(self):
        return self._no_of_columns

    def __repr__(self):
        print("The array has initialized element:")
        for i in self._state_array:
            for p in i:
                if p:
                    print(p.initialized, end = ' ')
                else:
                    print('    ', end = ' ')
            print('')
        print()
        print("Thrust vectors are as follows")
        for i in self._state_array:
            for j in i:
                if j :
                    print(j, end = ' ')
            print()
        return ''

    def get(self, var):
        x, y = var
        return self._state_array[y][x]


##quick test codes

if __name__ == '__main__':

    t = time.time()
    test = ArPel('config.json')
    t2 = time.time()
    print(test)
    print(f'max number of pels is : {test.no_of_rows*test.no_of_columns}')
    print(f'built arpel in {t2-t} seconds')
    print(PEL.conversion_matrices)