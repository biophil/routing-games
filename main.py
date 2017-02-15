# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 09:05:47 2016

@author: Philip
"""

import numpy as np
from linear import Network,twoPathGeneric,threePathGeneric,fourPathGeneric1,Parallel
import numpy.linalg as la

#t = Network(np.diag([1,2,3,4]),[1,1.5,3,4.5])
#print(t.X)

#base = np.zeros([6,6])
#base[0:3,0:3] = np.diag(np.ones(3))
#base[0,0:3] = base[0,0:3] + np.ones(3)
#base[0:3,0] = base[0:3,0] + np.ones(3)
##base[1,0:2] = 2*np.ones(2)
##base[0,1] = 2
#base[3:6,3:6] = np.flipud(np.fliplr(base[0:3,0:3]))
#
#b = [0,.1,1.1,1.2,1.3,1.4]
#
#weird = np.array([[1,0,1,1,0,0,0,0],
#                  [0,2,0,0,0,0,1,0],
#                  [1,0,1,0,0,0,0,0],
#                  [1,0,0,1,0,0,0,0],
#                  [0,0,0,0,1,0,0,1],
#                  [0,0,0,0,0,1,0,1],
#                  [0,1,0,0,0,0,1,0],
#                  [0,0,0,0,1,1,0,1]  ])
#b = [0,1,1.1,1.2,2,2.1,2.2,3]
#
#basicParallel = Network(np.diag(np.ones(8)),range(0,8))
#t = Network(weird,b)
#
#XAXT = t.Y@t.A@t.Y.T # this is the matrix that tells us which direction z moves
## (if all b(i+1)-b(i)=1)
#
#try :
#    Y = t.Y
#    YT = t.Y.T
#    M = t.M
#    MT = M.T
#    A = t.A
#    dXb = np.diagflat(Y@t.b)
#except AttributeError :
#    print('didnt do it, because M never done got set')

## This is for examples created on 2/14/2017 p. 5:
    
three = threePathGeneric([1,1,1,0,0],[0,0.5,1])
four = fourPathGeneric1([1,1,1,0,0,0,0,0],[0,0.5,1,2])

gl = 0.2
gu = 4
z1 = 1/(1+gl)
z2 = 2*(1/(2*(1+gl))-1/(1+gu))
z3 = 1/(1+gu)

three.r = 1.5
four.r = 1.5
zhet = np.array([z1,z2,z3])
zzL3 = np.array([z1,z1])
zzL4 = np.array([z1,z1,z1])
zzU3 = np.array([z3,z3])
zzU4 = np.array([z3,z3,z3])
fhet = four.fz(zhet)
fhet2 = four.fz([z1,z3,z3])
fL3 = three.fz(zzL3)
fL4 = four.fz(zzL4)
fU3 = three.fz(zzU3)
fU4 = four.fz(zzU4)
fL = np.zeros([4,1])
fL[0:3] = fL3.copy()
fU = fU4.copy()
zopt3 = np.array([.5,.5])
zopt4 = np.array([.5]*3)
fopt3 = three.fz(zopt3)
fopt = np.zeros([4,1])
fopt[0:3] = fopt3.copy()


fE1 = fhet2.copy()
fE1[2] = 0
fE1[3] = 0
gE1 = fopt.copy()
gE1[2:] = np.zeros([2,1])
ftil = np.array([[.6288888888,.378888888,.008888888,0]]).T
Ctilftil = ftil[0]**2 + ftil[1]**2 + 0.5*ftil[1] + ftil[2]**2 + 1.24*ftil[2]
fmean = fL*(1-.522222222222)+fU*.522222222222