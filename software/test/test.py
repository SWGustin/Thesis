import sys, os
pathadd = os.path.dirname(__file__)
pathadd = '\\'.join(pathadd.split('\\')[:-1])+'\\MVC\\'
print(pathadd)
sys.path.insert(1, pathadd)

from Model import object_model as model
from View import viewer
# from Controller import controller
# from collections import namedtuple

print(pathadd)
# test_Switch = parts.Switch()

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