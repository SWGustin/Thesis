import os
import MVC.Model.Arpel as model
import numba as nb
import numpy as np
import math
from random import random
from numba import jit, njit, cuda, vectorize
from timeit import timeit
from datetime import datetime

arpl = model.ArPel('config.json')

setpoints = np.zeros((10,10,4))



@vectorize(['int32(int32, int32)'], target = 'cuda')
def add_ufunc(x,y):
    return x+y


sz = 100000000
a = np.random.randint(1000,size = sz)
b = np.random.randint(1000, size = sz)

t1 = datetime.now()
add_ufunc(a,b)
t2 =datetime.now()
print(f'done in {t2-t1} seconds or {format(1/(t2-t1).total_seconds()*sz, "10.2E")} per second')

a_device = cuda.to_device(a)
b_device = cuda.to_device(b)

t1 = datetime.now()
add_ufunc(a,b)
t2 =datetime.now()
print(f'done in {t2-t1} seconds or {format(1/(t2-t1).total_seconds()*sz, "10.2E")} per second')


# threadsperblock = 32
# blocks_per_grid = (arpl.size + (threadsperblock-1))//threadsperblock

# go_fast[blocks_per_grid, threadsperblock](setpoints)

#go_fast(setpoints)
#print(setpoints)

# print('-------------')
# print(arpl)
# print('done')
 
# import sys, os
# pathadd = os.path.dirname(__file__)
# pathadd = '\\'.join(pathadd.split('\\')[:-1])+'\\MVC\\'
# print(pathadd)
# sys.path.insert(1, pathadd)

# from Model import object_model as model
# from View import viewer
# # from Controller import controller
# # from collections import namedtuple

# print(pathadd)
# # test_Switch = parts.Switch()

# print(test_Switch.dutyCycle)
# test_Switch.dutyCycle = 100
# assert test_Switch.dutyCycle == 100

# test_Switch.dutyCycle = 101
# assert test_Switch.dutyCycle == 100

# test_Switch.dutyCycle = -1
# assert test_Switch.dutyCycle == 0

# test_Switch.frequency = 100000
# assert test_Switch.frequency == 100000
# assert test_Switch.dutyCycle == 0

# print("-------------------")
# print("passed all Switch tests")

# try:
#     test_PEL = parts.PEL(2,1)
# except(parts.BasisVectorError):
#     print("pass minimum Switch test")

# test_PEL = parts.PEL(3,1)
# assert len(test_PEL.Switches) == 3

# assert test_PEL.Switches[2].frequency == 0
# assert test_PEL.Switches[1].dutyCycle == 0

# print("-------------------")
# print("passed all PEl tests")

# wing_geometry = namedtuple('wing_geometry', ['root_chord', 'tip_chord', 'span', 'leading_angle'])
# arpel_test = parts.ArPEl()
# wing = wing_geometry(10,7,5,5)
# arpel_test.geometry = wing

# print(arpel_test)