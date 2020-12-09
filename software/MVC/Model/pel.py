
import os
import numpy as np
import time

class BasisVectorError(Exception):
    pass

from .switch import Switch 


class PEL:
    conversion_matrices = dict()

    @classmethod
    def calc_BVs(PEL, no_switches, primary_dir):
        _basis_angles = [((360/no_switches * i) + primary_dir)%360 for i in range(no_switches)]
        return [(np.cos(np.radians(x)),np.sin(np.radians(x))) for x in _basis_angles]
    
    @classmethod
    def calc_Conversion_matrix(PEL, V1,V2):
        bv = [[V1[0], V2[0]],[V1[1], V2[1]]]
        return np.linalg.inv(bv)

    @classmethod
    def addConversionMatrix(PEL, no_switches, primary_dir):
        outer_key = (no_switches, primary_dir)
        if outer_key in PEL.conversion_matrices.keys():
            return
        inner_vals = []#this needs to be an array of conversion matrices
        BVs = PEL.calc_BVs(no_switches, primary_dir)
        for i in range(no_switches):
            v1= BVs[i]
            v2 = BVs[((i+1)%no_switches)]
            inner_vals.append(PEL.calc_Conversion_matrix(v1,v2))
        
        PEL.conversion_matrices[outer_key] = inner_vals

    def __init__(self, ID, noOfSwitches, totalWidth, primaryDirection = 0):
        if noOfSwitches < 3:
            raise BasisVectorError("The minimum number of Low Voltage Elements for a additively closed space is 3")
        self._noOfSwitches = noOfSwitches
        self._thrust = 0+0j
        self._primaryDirection = primaryDirection
        self._frequency = 100
        self._rad_per_switch = np.round(2*np.pi/self._noOfSwitches,6)
        self._switches = [Switch() for _ in range(self._noOfSwitches)]
        self._total_width = totalWidth
        self._ID = ID
        PEL.addConversionMatrix(self._noOfSwitches,self._primaryDirection)

    def __repr__(self):
        return str(self._thrust)

    @property
    def ID(self):
        return self._ID

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, Hz):
        self._frequency = max(0,Hz)

    @property
    def thrust(self):
        return self._thrust
    
    @thrust.setter
    def thrust(self, val):
        correction = abs(val)
        if correction > 1:
            val /= correction
        self._thrust = val
        thrust_hash = int((np.angle(val)%6.283185)//self._rad_per_switch)
        convert = PEL.conversion_matrices[(self._noOfSwitches, self._primaryDirection)][thrust_hash]
        local_thrust = np.matmul(convert, [self._thrust.real,self._thrust.imag])
        #this is for safety (forces thrust < 1) but is slow because linalg.norm is non trivial
        #local_thrust /= max(np.linalg.norm(local_thrust),1)
        for s, t in zip(self._switches, local_thrust):
            s.dutyCycle = t

    @property
    def switches(self):
        return self._switches

    @property
    def width(self):
        return self._total_width 