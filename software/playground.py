import numpy as np

b1 = 1+0j
b2 = 0.5 - 0.87j
b3 = -0.5 - 0.87j

t = .717+.717j

BVs= [b1,b2,b3]
Angles = [0,120,240]

thrust_angle = np.degrees(np.angle(t))%180
#use angles array

i = 0
while i < len(BVs) and np.angle(BVs[i+1])%180 < np.angle(t)%180:
    i+=1
bv = [[np.real(BVs[i]),np.real(BVs[i+1])],
        [np.imag(BVs[i]),np.imag(BVs[i+1])]]

convert = np.linalg.inv(bv)
x= np.matmul(convert,[1,1])
nrm = np.linalg.norm(x)
x = x/nrm

