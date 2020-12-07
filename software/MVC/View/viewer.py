import os
import json
import numpy as np
from time import time
from matplotlib import pyplot as plt
from matplotlib import animation, patches
from random import random

class Display:

    def __init__(self, arpel=None):
        plt.ion() TODO: figure this out
        self.arpel =    arpel
        geometry = arpel.geometry
        geometry.append(geometry[0])
        xs, ys = zip(*geometry)
        self.fig, ax = plt.subplots(1,1)
        plt.plot(xs,ys)
        pel_locs = []
        y, x = arpel.root_chord - arpel.setback + arpel.pel_width/2, 0 
        #arpel.pel_sep - arpel.pel_width/2
        for row in arpel.state_array:
            y -= arpel.pel_width + arpel.pel_sep
            for pel in row:
                if pel:
                    x += arpel.pel_width + arpel.pel_sep
                    pel_locs.append((x,y))
                    ax.add_patch(patches.Rectangle((x-pel.width/2,y-pel.width/2), pel.width, 
                        pel.width, fc = 'none', ec = 'b', lw = 1))
            x = 0
        #dummy initial thrusts
        u, v = zip(*[(pel.thrust.real, pel.thrust.imag) for pel in arpel])
        # put thrusts on screen
        xs, ys = zip(*pel_locs)
        self.Q = ax.quiver(xs, ys, u, v, pivot='tail', color='r', units='inches', scale = 3)
        plt.plot(xs, ys, 'bx')
        plt.gca().set_aspect('equal', adjustable='box')

        
    def update(self):
        U, V = zip(*[(pel.thrust.real, pel.thrust.imag) for pel in self.arpel])
        self.Q.set_UVC(U,V)
        return self.Q,

    def animate(self):
        self.update()
#        anim = animation.FuncAnimation(self.fig, self._animate_helper, fargs=(self.Q, self.arpel),
#                               interval=50, blit=False)
        plt.plot()

    def show(self):
        plt.show()