import os
import json
import numpy as np
from time import time
from matplotlib import pyplot as plt
from matplotlib import animation
from random import random

class Display:
    
    @classmethod
    def animate(Display, num, Q, arpel, x, y):
        Q.set_UVC(U,V)

        return Q,

    def __init__(self, arpel=None):
        t1  = time()
        geometry = arpel.geometry
        geometry.append(geometry[0])
        fig, ax = plt.subplots(1,1)
        xs, ys = zip(*geometry)
        plt.plot(xs,ys)
        pel_locs = []
        y, x = arpel.root_chord - arpel.setback + arpel.pel_width/2,\
                arpel.pel_sep - arpel.pel_width/2
        for row in arpel.state_array:
            y -= arpel.pel_width + arpel.pel_sep
            for pel in row:
                if pel:
                    x += arpel.pel_width + arpel.pel_sep
                    pel_locs.append((x,y))
            x = 0
        #dummy initial thrusts
        # u, v = zip(*[(pel.thrust.real, pel.thrust.imag) \
        #     for row in arpel.state_array for pel in row if pel])

        u,v = 0,1

       # put thrusts on screen
        xs, ys = zip(*pel_locs)
        Q = ax.quiver(xs, ys, u ,v , pivot='mid', color='r', units='inches')
        plt.plot(xs, ys, 'bx')
        print(f'built test display in {time()-t1} seconds')

        anim = animation.FuncAnimation(fig, Display.animate, fargs=(Q, xs, ys),
                               interval=50, blit=False)
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
