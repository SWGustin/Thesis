# put the code to run a demo of it all in here

from matplotlib import pyplot as plt
from matplotlib import animation
import random
import MVC.Model.Arpel as model
import MVC.View.viewer as view
import MVC.Controller.controller as controller
import time

t1 = time.time()
_model = model.ArPel('config.json')
print(f'built test model in: {time.time()-t1} seconds')
t1 = time.time()
_view = view.Display(_model)
print(f'built test display in: {time.time()-t1} seconds')
t1 = time.time()
tcont = controller.Controller(_model, _view)
print(f'built test controller in: {time.time()-t1} seconds')

def set_thrust(pel):
    pel.thrust = complex((random.random()*2-1)/10, (random.random()*2-1)/10)

cntr,frames = 0,0
t1 = time.time()

while True:
    frames +=1
    t = time.time()
#    update pels etc

    list(map(set_thrust, _model))    
    _view.update()

    if t-t1 >= 5:
        print(f'framerate is: {frames/(t-t1):.2f}')
        print(f'{cntr/(time.time()-t1):.0f} pels per second!')
        t1 = time.time()
        cntr = 1
        frames = 0
        
