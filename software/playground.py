import numpy as np


a = 1 + 1j
b = 1

print(np.real(a)*np.real(b)+np.imag(a)*np.imag(b))

b1 = 1+0j
b2 = 0.5 - 0.87j
b3 = -0.5 - 0.87j

t = .717+.717j

BVs= [b1,b2,b3]
Angles = [0,120,240]

thrust_angle = np.degrees(np.angle(t))%180
#use angles array

print(thrust_angle)
i = 0
while i < len(BVs) and np.angle(BVs[i+1])%180 < np.angle(t)%180:
    i+=1
bv = [[np.real(BVs[i]),np.real(BVs[i+1])],
        [np.imag(BVs[i]),np.imag(BVs[i+1])]]

print(np.linalg.inv(bv))

print(bv)

#bvs = [BVs[i] for i in range(len(BVs)-1) if np.angle(BVs[i+1])%180 > np.angle(t)%180 and np.angle(BVs[i])%180<np.angle(t)%180] 