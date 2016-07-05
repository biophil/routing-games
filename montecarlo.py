# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 15:36:25 2016

@author: Philip
"""

from linear import fourPathGeneric1
import numpy.random
from numpy import array, reshape

def loadNet(net) :
    global M
    global R
    global XAXT
    global XAXTi
    global n
    global X
    global Y
    global A
    global b
    M = net.M
    R = net.R
    XAXT = net.Y@net.A@net.Y.T 
    XAXTi = numpy.linalg.inv(XAXT)
    n = net.n
    X = net.X
    Y = net.Y
    A = net.A
    b = net.b


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
    
#XAXT = testNet.Y@testNet.A@testNet.Y.T 
#XAXTinv = numpy.linalg.inv(XAXT)

# these zt's correspond to CMC tolls:
zt1 = reshape(array([.9,.8,.7]),[3,1])
zt2 = reshape(array([.8,.7,.6]),[3,1])
zt3 = reshape(array([.99,.75,.51]),[3,1])
zt4 = reshape(array([.95,.75,.55]),[3,1])

zMC = reshape(array([.5,.5,.5]),[3,1])

# these zt's correspond to non-CMC tolls:
zt5 = reshape(array([.9,.8,.4]),[3,1])
zt6 = reshape(array([.99,.5,.01]),[3,1])
zt7 = reshape(array([.7,.6,.3]),[3,1])
zt8 = reshape(array([.6,.3,.2]),[3,1])