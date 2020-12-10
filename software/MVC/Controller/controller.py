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
    def flow_state(self):
        return self._model.state_array

    #open loop controller
    @flow_state.setter
    def flow(self, val):
        try:
            p, t = val
        except ValueError:
            t = val
            p = self._model
        for pel in p:
            pass

    def entrain(self, pels = None):
        try:
            for pel in pels:
                self._model[pel] = 0-1j
        except TypeError:
            for pel in self._model:
                pel.thrust = 0-1j

    


if __name__ == "__main__":
    test = Controller(1,2)
    test.flow = (1,2,3)