# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 09:05:47 2016

@author: Philip
"""

import numpy as np
from linear import Network
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

weird = np.array([[1,0,1,1,0,0,0,0],
                  [0,2,0,0,0,0,1,0],
                  [1,0,1,0,0,0,0,0],
                  [1,0,0,1,0,0,0,0],
                  [0,0,0,0,1,0,0,1],
                  [0,0,0,0,0,1,0,1],
                  [0,1,0,0,0,0,1,0],
                  [0,0,0,0,1,1,0,1]  ])
b = [0,1,1.1,1.2,2,2.1,2.2,3]

basicParallel = Network(np.diag(np.ones(8)),range(0,8))
t = Network(weird,b)

XAXT = t.Y@t.A@t.Y.T # this is the matrix that tells us which direction z moves
# (if all b(i+1)-b(i)=1)

try :
    Y = t.Y
    YT = t.Y.T
    M = t.M
    MT = M.T
    A = t.A
    dXb = np.diagflat(Y@t.b)
except AttributeError :
    print('didnt do it, because M never done got set')