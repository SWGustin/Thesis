import os
import json
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

class Display:
    
    def __init__(self, arpel=None):
        geometry = arpel.geometry
        geometry.append(geometry[0])
        print(geometry)
        xs, ys = zip(*geometry)
        plt.plot(xs,ys) 
        plt.show()

#         self._arrowLength = config.maxArrowLength
#         self._arrowWidth = config.arrowWidth
#         self._onColour = config.onColour
#         self._offColour = config.offColour 
#         self._arpel = arpel

#     def _drawWing(self):
#         pass

#     def _drawPEl(self):
#         pass        

#     def update(self):
#         self.wn.update()

# if __name__ == '__main__':
#     config_file_name = 'config.json'
#     config_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + '\\' + config_file_name
