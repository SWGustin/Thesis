import os
import json
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import MVC.Model.object_model as model

config_file_name = 'config.json'
config_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + '\\MVC\\View\\' + config_file_name

with open(config_path, 'r') as f:
    reader = json.load(f)

geometry = reader['wing_geometry']    
print(geometry)
corners = [(0,0)]
tip_setback = -int(geometry['span'] / 2 * np.sin(np.radians(geometry['sweep_angle'])))
corners.append([geometry['span'] / 2, tip_setback])
corners.append([geometry['span'] / 2, tip_setback-geometry['tip_chord']])
corners.append([0,-geometry['root_chord']])

print(corners)

apel = model.ArPel('config.json')

coord = corners
coord.append(coord[0]) #repeat the first point to create a 'closed loop'

xs, ys = zip(*coord) #create lists of x and y values

plt.figure()
plt.plot(xs,ys) 
plt.show() # if you need...


X, Y = np.mgrid[:2*np.pi:10j,:2*np.pi:5j]
U = np.cos(X)
V = np.sin(Y)

fig, ax = plt.subplots(1,1)
Q = ax.quiver(X, Y, U, V, pivot='mid', color='r', units='inches')

ax.set_xlim(-1, 7)
ax.set_ylim(-1, 7)

def update_quiver(num, Q, X, Y):
    """updates the horizontal and vertical vector components by a
    fixed increment on each frame
    """

    U = np.cos(X + num*0.1)
    V = np.sin(Y + num*0.1)

    Q.set_UVC(U,V)

    return Q,

# you need to set blit=False, or the first set of arrows never gets
# cleared on subsequent frames
anim = animation.FuncAnimation(fig, update_quiver, fargs=(Q, X, Y),
                               interval=50, blit=False)
fig.tight_layout()
plt.show()