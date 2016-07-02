# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 15:36:25 2016

@author: Philip
"""

from linear import fourPathGeneric1
import numpy.random
from numpy import array, reshape

numIter = 1
badNets = []
z23 = reshape(array([0,1,1]),[1,3])
z3 = reshape(array([0,0,1]),[1,3])
z1 = reshape(array([1,0,0]),[3,1])
z12 = reshape(array([1,1,0]),[3,1])

numpy.random.seed(1)
for i in range(numIter):
    a = numpy.random.random([8])**3
    permute = numpy.random.permutation([0,1,2,3])
    try :
        testNet = fourPathGeneric1(a,[0,1,2,3],permute)
        MTAM = testNet.MTAM()
        testVals = array([z23@MTAM@z1,z3@MTAM@z12])
        if sum(testVals<0)>0 : # if either is negative, we lack monotonicity
            badNets.append({'a': a, 'net':testNet, 'permute':permute, 'err':None})
    except Exception as err:
        badNets.append({'a': a, 'net':None, 'err':err, 'permute':permute})
    
XAXT = testNet.Y@testNet.A@testNet.Y.T 