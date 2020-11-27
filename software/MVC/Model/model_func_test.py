import parts
import ArPEl

test_LVE = parts.LVE()

print(test_LVE.dutyCycle)
test_LVE.dutyCycle = 100
assert test_LVE.dutyCycle is 100

test_LVE.dutyCycle = 101
assert test_LVE.dutyCycle is 100

test_LVE.dutyCycle = -1
assert test_LVE.dutyCycle is 0

test_LVE.frequency = 100000
assert test_LVE.frequency == 100000
assert test_LVE.dutyCycle is 0

print("-------------------")
print("passed all LVE tests")

try:
    test_PEL = parts.PEL(2)
except(parts.BasisVectorError):
    print("pass minimum LVE test")

test_PEL = parts.PEL(3)
assert len(test_PEL.LVEs) == 3

assert test_PEL.LVEs[2].frequency == 0
assert test_PEL.LVEs[1].dutyCycle == 0

print("-------------------")
print("passed all PEl tests")



arpel_test = ArPEl.ArPEl()

arpel_test.geometry = (10,7,50,5)

print(arpel_test.geometry)