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

