import os
import json 
import numpy as np
import time
from .pel import PEL as PEL


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
                    self.root_chord - row_set_back - self.pel_sep - self._pel_width)):
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