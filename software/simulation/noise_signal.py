from random import random
import types

class pitot:
    def __init__(self,  location, signal_iter = None):
        self._location = location
        self.signal_iter = signal_iter

    @property
    def location(self):
        return self._x, self._y

    @property
    def signal(self):
        return next(self.signal_iter)


class noise_maker:
    def init(self, pitots):
        self._pitots = pitots
        
    def get(self, pos):
        



if __name__ == "__main__":
    ptest = pitot((1,1))
    print(ptest.signal)