import os
import json 
import numpy as np
import time
#from .pel import PEL

class ArPel:

    conversion_matrices = dict()\

    @classmethod
    def calc_BVs(ArPel, no_switches, primary_dir):
        _basis_angles = [((360/no_switches * i) + primary_dir)%360 for i in range(no_switches)]
        return [(np.cos(np.radians(x)),np.sin(np.radians(x))) for x in _basis_angles]
    
    @classmethod
    def calc_Conversion_matrix(ArPel, V1,V2):
        bv = [[V1[0], V2[0]],[V1[1], V2[1]]]
        return np.linalg.inv(bv)

    @classmethod
    def addConversionMatrix(ArPel, no_switches, primary_dir):
        outer_key = (no_switches, primary_dir)
        if outer_key in ArPel.conversion_matrices.keys():
            return
        inner_vals = []#this needs to be an array of conversion matrices
        BVs = ArPel.calc_BVs(no_switches, primary_dir)
        for i in range(no_switches):
            v1= BVs[i]
            v2 = BVs[((i+1)%no_switches)]
            inner_vals.append(ArPel.calc_Conversion_matrix(v1,v2))
        
        ArPel.conversion_matrices[outer_key] = inner_vals

    def __init__(self, config_file_name):
        print('initializing ARPEL')
        config_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  
        config_path = '\\'.join(config_path.split('\\')[:-1]) + '\\config\\' + config_file_name
        with open(config_path, 'r') as f:
            data = json.load(f)
        self.itr = None
        self._current_row = -1

        _tip_chord = data['wing_geometry']['tip_chord']
        _sweep_angle = data['wing_geometry']['sweep_angle']
        _pel_cardinality = data['pel_geometry']['number_of_switches']
        _cardinal_offset = data['pel_geometry']['primary_direction']
        self._span = data['wing_geometry']['span']/2
        self._root_chord = data['wing_geometry']['root_chord']
        self._pel_width = data['pel_geometry']['overall_width']
        self._pel_sep = data['pel_geometry']['seperation']
        self._set_back = data['wing_geometry']['set_back']
        self._anchor_point = 0,self._set_back

        #handy vals to have
        tan_sweep = np.tan(np.radians(_sweep_angle))
        
        def getWidth(x, RHS = True):
            return self._pel_sep * x + self._pel_width * x +(1*RHS) 
        
        def getChord(y, trailing_edge = False):
            return (self._pel_width + self.pel_sep)*y + (self._pel_width * trailing_edge)
        
        # get corners of basic wing
        self._geometry = [(0,0)]
        tip_offset = self._span*tan_sweep
        self._geometry.append((self._span, -tip_offset))
        self._geometry.append((self._span,self._geometry[1][1]-_tip_chord))
        self._geometry.append((0,0))

        # build square thrust array boundaries
        _max_chord = max(self._root_chord, tip_offset + _tip_chord)
        self._no_of_rows = int(np.floor((_max_chord)/(self._pel_width + self._pel_sep)))
        self._no_of_columns = int(np.floor((self._span - self._pel_sep)/(self._pel_width + self._pel_sep)))
        
        tan_trailing_sweep = (self._root_chord - (tip_offset + _tip_chord))/self._span

        #create a numpy array init to 2
        self._state_array = np.ones((self._no_of_rows, self._no_of_columns, _pel_cardinality + 1))*2
        self._no_of_pels = 0

        #set valid elemetns to 0.f
        for y in range(self._no_of_rows):
            row_y = getChord(y)
            for x in range(self._no_of_columns):
                if getWidth(x) * tan_sweep-self._set_back < row_y and self._root_chord - getWidth(x) * tan_trailing_sweep > row_y:
                    self._state_array[y,x] = 0.0
                    self._no_of_pels +=1

    def __getitem__(self, indx):
        x,y = indx
        return self.state_array[y][x]

    def __setitem__(self,indx, value):
        x,y = indx
        if self.state_array[y][x][0] != 2:
            self.state_array[y][x][0] = value

            
    def __iter__(self):
        return self

    def __next__(self):
        try:
            nxt = next(self.itr)
            if nxt != 2:
                return nxt
            else: 
                raise StopIteration 
        except (StopIteration, TypeError):
            try:
                self._current_row += 1
                self.itr = iter(self.state_array[self._current_row])
                nxt = 2
                while nxt == 2:
                    nxt = next(self.itr)
                return nxt
            except (StopIteration, IndexError):
                self._current_row = -1
                raise StopIteration

    def __repr__(self):
        print("Thrust vectors are as follows")
        for i in self._state_array:
            for j in i:
                if j[0] != 2 :
                    print(j[0], end = '\t')
                else: 
                    print('\t', end = '')
            print()
        return ''

    def update(self, thrust_array):
        pass

    @property
    def size(self):
        return self._no_of_pels

    @property
    def no_of_pels(self):
        return self._no_of_pels

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

    def get(self, var):
        x, y = var
        return self._state_array[y][x]


if __name__ == "__main__":
    tarpl = ArPel('config.json')
