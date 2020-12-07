# put the code to run a demo of it all in here

from matplotlib import pyplot as plt
from matplotlib import animation
import MVC.Model.object_model as model
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
tcont.display.animate()
tcont.display.show()
