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