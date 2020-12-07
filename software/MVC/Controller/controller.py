import numbers

class Controller:
    def __init__(self, model, display):
        self._model = model
        self._disp = display

    @property
    def model(self):
        return self._model

    @property
    def display(self):
        return self._disp

    @property
    def flow(self):
        return self._model.state_array

    @flow.setter
    def flow(self, val):
        if isinstance(val, numbers.Number):
            for pel in self._model:
                pel.thrust = val