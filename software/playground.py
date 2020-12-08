import timeit
import numpy as np

setup = '''import random
import MVC.Model.object_model as model
tarpl = model.ArPel('config.json')
'''

print(timeit.timeit("tarpl[0,0].thrust = 1+1j", setup = setup, number = 100000))

#timeit.timeit("tpel.thrust = 1+1j", setup = setup, number = 100)
print(2*np.pi)


