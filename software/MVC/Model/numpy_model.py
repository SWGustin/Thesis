import math 
import numpy as np
import json
import os

class ArPEl:
    """
    This creates the np array representing the current firing state and handling functions.
    """
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

        self._geometry = [(0,0)]
        # get corners of basic wing1
        tip_offset = self._span*math.tan(math.radians(self._sweep_angle))
        self._geometry.append((self._span, tip_offset))
        self._geometry.append((self._span,self._geometry[1][1]+self._tip_chord))
        self._geometry.append((0,self._root_chord))

        #establish the state vector for a PEl
        state_vector = np.dtype([('thrust','c8'), ('initialized', '?'), ('power', 'f4'), ('frequency', 'u1'),('no_of_pels', 'u1')])

        # build an np.array of state vectors
        max_span = self._span//2
        max_chord = max(self._root_chord, tip_offset + self._tip_chord)
        no_of_rows = math.floor((max_chord)/(self._pel_width + self._pel_sep))
        no_of_columns = math.floor((max_span - self._pel_sep)/(self._pel_width + self._pel_sep)) 
        self._state_array =np.zeros((no_of_rows,no_of_columns), dtype = state_vector)

        #initialize all cells that fit

    @property
    def geometry(self):
        return self._geometry
        
    #TODO: add unadded setters and calculate array of pels   

    def __repr__(self):
        print('the wing geometry is as follows: \n'
            f'span = {self._span};  '
            f'root chord = {self._root_chord};  '
            f'tip chord = {self._tip_chord};  '
            f'leading edge sweep angle = {self._sweep_angle}')
        print('---------------------------')
        print('the Plasma Element geometry is as follows: \n'
            f'pel width= {self._pel_width};  '
            f'space between = {self._pel_sep}')
        print('---------------------------')
        print('the resulting Array of Plasma Elements has dimensions:\n'
            f'overall span in PEls = {self._state_array.shape[1]};   '
            f'overall chord in PEls = {self._state_array.shape[0]}')
        print('---------------------------') 
        print('The following is the vector lengths of firing vector for PEls')
        print(abs(self._state_array['thrust']))
        print('\nThe following is the initialization states of PEls')
        print(self._state_array['initialized'])
        return ''        

    def getPower(self, vals):
        x,y = vals
        return abs(self._state_array[x,y]['thrust'])
    
    def setPower(self, vars):
        x, y, _power = vars
        mult = max(min(_power/self.getPower((x, y)), 1), 0)
        self._state_array[x,y]['thrust'] *= mult

    def getDirection(self, vals):
        x, y = vals
        return round(np.angle(self._state_array[x,y]['thrust'], True),4)

    def __getitem__(self, vals):
        try:
            x, y, attribute = vals
        except ValueError:
            x, y = vals
            attribute = None

        if attribute is None:
            return self._state_array[x, y]
        elif attribute in self._state_array.dtype.names:
            return self._state_array[x,y][attribute]
        elif isinstance(attribute, number):
            return self._stat_array[x,y,attribute]
        else:
            raise ValueError(f'{attribute} was not a valid index')

    def __setitem__(self,vars, val):
        try:
            x, y, attribute= vars
            self._state_array[x,y][attribute] = val
        except ValueError:
            x, y = vars
            if not isinstance(val, self._state_array.dtype):
                raise ValueError
            self._state_array[x,y] = val


#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#---------------------------                                               ----------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

test = ArPEl('config.json')


# test = ArPEl(base_chord = 20, tip_chord = 15, span = 100, leading_angle = 2,
#             no_of_switches = 3, pel_width = 2, pel_seperation = 1)


print(test)
# print(test[1,1,'thrust'])
# test[(1,1,'thrust')] = 1+1j
# print(test[1,1,'initialized'])
# print(test.getDirection((1,1)))
# print(test[1,1,'thrust'])
# test[1,1,'thrust'] = -1 + 1j
# print(test[1,1,'thrust'])
# test.getPower((1,1))
# test.setPower((1,1,1.01))
# print(test[1,1,'thrust'])