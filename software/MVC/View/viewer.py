import os
import json
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

class Display:
    
    def __init__(self, arpel=None):
        geometry = arpel.geometry
        geometry.append(geometry[0])
        fig, ax = plt.subplots(1,1)
        xs, ys = zip(*geometry)
        plt.plot(xs,ys)
        pel_locs = []
        for row in range(arpel.no_of_rows):

            for col in range(arpel.no_of_columns):
                y = arpel.root_chord - (arpel.setback + (row)*(arpel.pel_width + arpel.pel_sep) \
                    + arpel.pel_width/2)
                if arpel.state_array[row][col]:
                    x = arpel.pel_sep + arpel.pel_width/2 + \
                        col*(arpel.pel_width + arpel.pel_sep)
                    pel_locs.append((x,y))

        #dummy initial thrusts
        u = 0
        v = 1
        #put thrusts on screen
        xs, ys = zip(*pel_locs)
        Q = ax.quiver(xs, ys, u ,v , pivot='mid', color='r', units='inches')


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

##quick test codes
if __name__ == '__main__':
    config_file_name = 'config.json'
    config_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + '\\' + config_file_name
