import math 
import numpy as np

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

class ArPEl:
    """
    This creates the np array representing the current firing state and handling functions.
    """
    def __init__(self, *args, base_chord, tip_chord, span, leading_angle, no_of_switches, pel_width, pel_seperation):
        self._base_chord = base_chord
        self._tip_chord = tip_chord
        self._span = span
        self._leading_angle = leading_angle
        self._no_of_Switches = no_of_switches 
        self._pel_width = pel_width 
        self._pel_seperation = pel_seperation
        self._geometry = [(0,0)]
        self._pel = PEL(self._no_of_Switches,self._pel_width,0)

        # get corners of basic wing
        tip_offset = self._span*math.tan(math.radians(self._leading_angle))
        self._geometry.append((self._span, tip_offset))
        self._geometry.append((self._span,self._geometry[1][1]+self._tip_chord))
        self._geometry.append((0,self._base_chord))

        #establish the state vector for a PEl
        state_vector = np.dtype([('thrust','c8'), ('initialized', '?'), ('power', 'f4'), ('frequency', 'u1'),('no_of_pels', 'u1')])

        # build an np.array of state vectors
        max_span = self._span//2
        max_chord = max(self._base_chord, tip_offset + self._tip_chord)
        no_of_rows = math.floor((max_chord)/(self._pel_width+self._pel_seperation))
        no_of_columns = math.floor((max_span - self._pel_seperation)/(self._pel_width + self._pel_seperation)) 
        self._state_array =np.zeros((no_of_rows,no_of_columns), dtype = state_vector)
        self._state_array = np.rec.array(self._state_array)

        #initialize all cells that fit

    """
        The data stored in the state array is stored for each PEl in the 2D Array of PEls.  
        The stored data vectors is as follows
        [DC_x, DC_y, DC_z, Initialized, MAX_POWER, FREQUENCY, NUMBER OF PELS]
    """

    @property
    def geometry(self):
        return self._geometry
        
    #TODO: add unadded setters and calculate array of pels   

    def __repr__(self):
        print('the wing geometry is as follows: \n'
            f'span = {self._span};  '
            f'base chord = {self._base_chord};  '
            f'tip chord = {self._tip_chord};  '
            f'leading edge angle = {self._leading_angle}')
        print('---------------------------')
        print('the Plasma Element geometry is as follows: \n'
            f'pel width= {self._pel_width};  '
            f'space between = {self._pel_seperation}')
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

    def showInitialized(self):
        print(np.sqrt())

    @property
    def velocity(self):
        return abs(self._state_array[1,1]['thrust'])

    @velocity.setter
    def velocity(self, vars):
        (x, y, V_x,V_y) = vars
        self._state_array[x,y]['thrust'] = V_x + V_y*j 

    @property
    def Direction(self, x, y):
        return np.angle(self._state_array[x,y]['thrust'], True)

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


test = ArPEl(base_chord = 20, tip_chord = 15, span = 100, leading_angle = 2,
            no_of_switches = 3, pel_width = 2, pel_seperation = 1)

print(test)

print(test[1,1])
#print(test.getDirection(1,1))