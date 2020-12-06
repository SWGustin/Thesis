import os
import json
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import MVC.Model.object_model as model
import MVC.View.viewer as view
import time


t1 = time.time()

tarpel = model.ArPel('config.json')
print(f'built test arpel in: {time.time()-t1} seconds')
t2 =time.time()
tview = view.Display(tarpel)

print(tarpel[1])
print(tarpel[1,2])